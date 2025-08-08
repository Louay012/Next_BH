# coding: utf-8
"""
reco_produits.py

But :
- Charger un fichier xlsx contenant 4 feuilles: Clients, Contrarts, Opportunites, MApping_Produits
- Préparer les données
- Entraîner un modèle (LightGBM) pour recommander les produits
- Fournir une fonction recommander_produits(client_id, k=3)
"""

import pandas as pd
import numpy as np
import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import top_k_accuracy_score, accuracy_score
import lightgbm as lgb
import joblib
import warnings
warnings.filterwarnings("ignore")

# -------------------------
# CONFIG
# -------------------------
XLSX_PATH = "D:/fezaimohamedelamine/ia_genrative/BHAssurance/BD/Données_Assurance_S2.xlsx"
RANDOM_STATE = 42
MODEL_PATH = "lgb_reco_model.joblib"
PREPROCESS_PATH = "preprocess.joblib"

# -------------------------
# 1) CHARGER LES DONNÉES
# -------------------------
xls = pd.read_excel(XLSX_PATH, sheet_name=None)  # charge toutes les feuilles
# On suppose que les noms de feuilles existent comme mentionné
clients = xls.get('Clients')            # colonnes: ClientID, Nom, Prénom, CIN, DateNaissance, Sexe, SituationFamiliale, Profession, RevenusMensuels, Adresse, Email, Téléphone, WhatsApp
contrats = xls.get('Contrats')        # ContratID, ClientID, Branche, Produit, DateEffet, DateEcheance, StatutContrat, StatutPaiement, PrimeAnnuelle
opps = xls.get('Opportunités')         # OpportuniteID, ClientID, ProduitRecommandé, Argumentaire, Statut
map_prod = xls.get('Mapping_Produits') # Branche, Produit

# Basic safety checks
for df, name in [(clients, 'Clients'), (contrats, 'Contrats'), (opps, 'Opportunités'), (map_prod, 'Mapping_Produits')]:
    if df is None:
        raise ValueError(f"Feuille '{name}' introuvable dans {XLSX_PATH}.")

# -------------------------
# 2) PREPROCESSING & FEATURE ENGINEERING
# -------------------------
# Convertir les dates
def to_datetime_safe(s):
    try:
        return pd.to_datetime(s, errors='coerce')
    except:
        return pd.to_datetime(s, errors='coerce')
clients['DateNaissance'] = to_datetime_safe(clients.get('DateNaissance'))
contrats['DateEffet'] = to_datetime_safe(contrats.get('DateEffet'))
contrats['DateEcheance'] = to_datetime_safe(contrats.get('DateEcheance'))

# Age
today = pd.Timestamp.today().normalize()
clients['age'] = (today - clients['DateNaissance']).dt.days // 365
clients['age'] = clients['age'].fillna(-1).astype(int)

# Standardize revenus (numeric)
clients['RevenusMensuels'] = pd.to_numeric(clients['RevenusMensuels'], errors='coerce')

# Contracts features per client
# On considère les contrats valides (StatutContrat = 'Actif' ou autre) - si tu veux filtrer modifie la condition
contrats['is_active'] = contrats['StatutContrat'].fillna('').str.lower().isin(['actif','active','en cours','en_cours','true','1'])
# Nombre total de contrats
contrats_agg = contrats.groupby('ClientID').agg(
    n_contrats = ('ContratID','nunique'),
    n_active = ('is_active','sum'),
    avg_prime = ('PrimeAnnuelle', lambda s: pd.to_numeric(s, errors='coerce').mean()),
    last_contrat_date = ('DateEffet', 'max')
).reset_index()
contrats_agg['days_since_last_contrat'] = (today - contrats_agg['last_contrat_date']).dt.days.fillna(99999).astype(int)

# Produits historiques (one-hot top N)
top_products = contrats['Produit'].fillna('UNKNOWN').astype(str).value_counts().head(50).index.tolist()
def top_products_vector(df_contrats, top_list):
    df = df_contrats.copy()
    df['Produit'] = df['Produit'].fillna('UNKNOWN').astype(str)
    one_hot = df[df['Produit'].isin(top_list)].groupby('ClientID')['Produit'].agg(list).reset_index()
    # transform list into counts
    for p in top_list:
        one_hot[f'prod_hist_{p}'] = one_hot['Produit'].apply(lambda lst: lst.count(p) if isinstance(lst, list) else 0)
    # keep only necessary
    cols = ['ClientID'] + [f'prod_hist_{p}' for p in top_list]
    return one_hot[cols]

prod_hist = top_products_vector(contrats, top_products)

# Merge clients with contrat aggregates and product history
df = clients.merge(contrats_agg, left_on='ClientID', right_on='ClientID', how='left')
df = df.merge(prod_hist, on='ClientID', how='left')
df.fillna({c:0 for c in df.columns if c.startswith('prod_hist_')}, inplace=True)

# Fill NaNs for numeric aggregates
df['n_contrats'] = df['n_contrats'].fillna(0).astype(int)
df['n_active'] = df['n_active'].fillna(0).astype(int)
df['avg_prime'] = pd.to_numeric(df['avg_prime'], errors='coerce').fillna(0)

# Prepare labels: on va utiliser les **opportunités historiques** comme exemples supervisés.
# Si une opportunité a Statut = 'Gagné' ou 'Acceptee', on peut utiliser ProduitRecommandé comme produit réellement vendu.
opps['Statut'] = opps['Statut'].fillna('').str.lower()
# Considérons comme "target" toutes les opportunités fermées positivement (à adapter)
positive_status = ['gagné','accepté','acceptée','fermé_gagné','won','accepted','closed_won']
opps_train = opps[opps['Statut'].isin(positive_status)].copy()
opps_train['ProduitRecommandé'] = opps_train['ProduitRecommandé'].fillna('UNKNOWN').astype(str)

# Si pas d'opportunités positives, on peut aussi utiliser contrats passés: dernier produit du client
if opps_train.empty:
    print("Pas d'opportunités 'gagnées' trouvées ; on va créer des labels à partir du dernier produit du contrat.")
    last_prod = contrats.sort_values(['ClientID','DateEffet']).groupby('ClientID').tail(1)[['ClientID','Produit']].rename(columns={'Produit':'ProduitRecommandé'})
    opps_train = last_prod.copy()
    opps_train['Statut'] = 'inferred'

# Merge features with labels
data = df.merge(opps_train[['ClientID','ProduitRecommandé']], on='ClientID', how='inner')
# For reproducibility, drop clients without label (inner join above)
data = data.reset_index(drop=True)

# Label encode products (target)
products = data['ProduitRecommandé'].astype(str).unique().tolist()
products = sorted(products)  # determinism
prod_to_idx = {p:i for i,p in enumerate(products)}
idx_to_prod = {i:p for p,i in prod_to_idx.items()}
data['target'] = data['ProduitRecommandé'].map(prod_to_idx)

# -------------------------
# 3) FEATURES LIST
# -------------------------
# numerical and categorical columns from clients
num_cols = ['age','RevenusMensuels','n_contrats','n_active','avg_prime','days_since_last_contrat']
# add product history columns
prod_hist_cols = [c for c in data.columns if c.startswith('prod_hist_')]
num_cols += prod_hist_cols

cat_cols = ['Sexe','SituationFamiliale','Profession']  # adapt if other columns exist

# ensure columns exist
for c in cat_cols:
    if c not in data.columns:
        data[c] = 'UNKNOWN'

# Build X and y
X = data[num_cols + cat_cols]
y = data['target']

# -------------------------
# 4) PREPROCESSING PIPELINE
# -------------------------
numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('ohe', OneHotEncoder(handle_unknown='ignore', sparse_output=False))

])

preprocessor = ColumnTransformer(transformers=[
    ('num', numeric_transformer, num_cols),
    ('cat', categorical_transformer, cat_cols)
], remainder='drop')

# Fit-preprocess split
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y if len(np.unique(y))>1 else None)

X_train_prep = preprocessor.fit_transform(X_train)
X_val_prep = preprocessor.transform(X_val)

# -------------------------
# 5) ENTRAINER LIGHTGBM (multi-class)
# -------------------------
num_classes = len(products)
if num_classes < 2:
    raise ValueError("Pas assez de classes produits pour s'entraîner (moins de 2 produits).")

lgb_train = lgb.Dataset(X_train_prep, label=y_train)
lgb_val = lgb.Dataset(X_val_prep, label=y_val, reference=lgb_train)

params = {
    'objective': 'multiclass',
    'num_class': num_classes,
    'metric': 'multi_logloss',
    'verbosity': -1,
    'seed': RANDOM_STATE,
    'learning_rate': 0.05,
    'num_leaves': 31,
    'max_depth': -1,
}

print("Entraînement LightGBM...")
bst = lgb.train(params,
                lgb_train,
                num_boost_round=500,
                valid_sets=[lgb_train, lgb_val],
                callbacks=[lgb.early_stopping(stopping_rounds=30), lgb.log_evaluation(period=0)])


# -------------------------
# 6) ÉVALUATION
# -------------------------
y_val_pred_proba = bst.predict(X_val_prep)  # shape (n_samples, num_classes)
y_val_pred = np.argmax(y_val_pred_proba, axis=1)
acc = accuracy_score(y_val, y_val_pred)
# top-3 accuracy (si classes >3)
topk = min(3, num_classes)
topk_acc = top_k_accuracy_score(y_val, y_val_pred_proba, k=topk, labels=list(range(num_classes)))

print(f"Accuracy (val): {acc:.4f}")
print(f"Top-{topk} accuracy (val): {topk_acc:.4f}")

# -------------------------
# 7) SAUVEGARDER LE MODÈLE ET LE PREPROCESS
# -------------------------
joblib.dump(bst, MODEL_PATH)
joblib.dump(preprocessor, PREPROCESS_PATH)
joblib.dump(idx_to_prod, "idx_to_prod.joblib")
joblib.dump(num_cols, "num_cols.joblib")
joblib.dump(cat_cols, "cat_cols.joblib")

print(f"Modèle sauvegardé dans {MODEL_PATH}. Preprocess sauvegardé dans {PREPROCESS_PATH}.")

# -------------------------
# 8) FONCTION DE RECOMMANDATION
# -------------------------
# On charge model + preprocessor (ici déjà en mémoire)
def recommander_produits(client_id, k=3):
    """
    Retourne top-k produits (liste ordonnée par probabilité) pour le client donné.
    """
    # Récupérer ligne client
    client_row = df[df['ClientID'] == client_id]
    if client_row.empty:
        raise ValueError(f"ClientID {client_id} non trouvé.")
    X_client = client_row[num_cols + cat_cols]
    X_client_p = preprocessor.transform(X_client)
    proba = bst.predict(X_client_p)[0]  # vecteur probas
    topk_idx = np.argsort(proba)[::-1][:k]
    results = [(idx_to_prod[idx], float(proba[idx])) for idx in topk_idx]
    return results

# Exemple d'utilisation
sample_client = data['ClientID'].iloc[0]
print(f"Exemple recommendations pour client {sample_client}:")
print(recommander_produits(sample_client, k=3))

# -------------------------
# 9) UTILISATION EN PRODUCTION (exemple)
# -------------------------
# - Pour recommander pour tous les clients : itère sur df['ClientID'] et stocke
def recommander_pour_tous(k=3):
    out = []
    for cid in df['ClientID'].unique():
        try:
            recs = recommander_produits(cid, k=k)
            for rank, (prod, p) in enumerate(recs, start=1):
                out.append({'ClientID': cid, 'rank': rank, 'Produit': prod, 'proba': p})
        except Exception as e:
            # skip si problème
            continue
    return pd.DataFrame(out)

# Générer CSV de recommandations
reco_df = recommander_pour_tous(k=3)
reco_df.to_csv("recommandations_top3.csv", index=False)
print("Recommandations générées : recommandations_top3.csv")
