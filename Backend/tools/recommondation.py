import pandas as pd
import numpy as np
import joblib

# Chargement des données complètes
XLSX_PATH = "D:/fezaimohamedelamine/ia_genrative/BHAssurance/BD/Données_Assurance_S2.xlsx"

xls = pd.read_excel(XLSX_PATH, sheet_name=None)
clients = xls['Clients']
contrats = xls['Contrats']

# Refaire les transformations importantes

# Date Naissance, Age
clients['DateNaissance'] = pd.to_datetime(clients.get('DateNaissance'), errors='coerce')
today = pd.Timestamp.today().normalize()
clients['age'] = (today - clients['DateNaissance']).dt.days // 365
clients['age'] = clients['age'].fillna(-1).astype(int)
clients['RevenusMensuels'] = pd.to_numeric(clients['RevenusMensuels'], errors='coerce')

# Contrats actif
contrats['is_active'] = contrats['StatutContrat'].fillna('').str.lower().isin(['actif','active','en cours','en_cours','true','1'])
contrats_agg = contrats.groupby('ClientID').agg(
    n_contrats = ('ContratID','nunique'),
    n_active = ('is_active','sum'),
    avg_prime = ('PrimeAnnuelle', lambda s: pd.to_numeric(s, errors='coerce').mean()),
    last_contrat_date = ('DateEffet', 'max')
).reset_index()
contrats_agg['days_since_last_contrat'] = (today - contrats_agg['last_contrat_date']).dt.days.fillna(99999).astype(int)

# Top produits
top_products = contrats['Produit'].fillna('UNKNOWN').astype(str).value_counts().head(50).index.tolist()

def top_products_vector(df_contrats, top_list):
    df = df_contrats.copy()
    df['Produit'] = df['Produit'].fillna('UNKNOWN').astype(str)
    one_hot = df[df['Produit'].isin(top_list)].groupby('ClientID')['Produit'].agg(list).reset_index()
    for p in top_list:
        one_hot[f'prod_hist_{p}'] = one_hot['Produit'].apply(lambda lst: lst.count(p) if isinstance(lst, list) else 0)
    cols = ['ClientID'] + [f'prod_hist_{p}' for p in top_list]
    return one_hot[cols]

prod_hist = top_products_vector(contrats, top_products)

# Merge complet
df = clients.merge(contrats_agg, on='ClientID', how='left')
df = df.merge(prod_hist, on='ClientID', how='left')
df.fillna({c:0 for c in df.columns if c.startswith('prod_hist_')}, inplace=True)
df['n_contrats'] = df['n_contrats'].fillna(0).astype(int)
df['n_active'] = df['n_active'].fillna(0).astype(int)
df['avg_prime'] = pd.to_numeric(df['avg_prime'], errors='coerce').fillna(0)

# Charger modèle et preprocessor
bst = joblib.load("lgb_reco_model.joblib")
preprocessor = joblib.load("preprocess.joblib")
idx_to_prod = joblib.load("idx_to_prod.joblib")
num_cols = joblib.load("num_cols.joblib")
cat_cols = joblib.load("cat_cols.joblib")

def recommander_produits(client_id, k=3):
    client_row = df[df['ClientID'] == client_id]
    if client_row.empty:
        return f"ClientID {client_id} non trouvé."
    X_client = client_row[num_cols + cat_cols]
    X_client_p = preprocessor.transform(X_client)
    proba = bst.predict(X_client_p)[0]
    topk_idx = np.argsort(proba)[::-1][:k]
    results = [(idx_to_prod[idx], float(proba[idx])) for idx in topk_idx]
    return results

if __name__ == "__main__":
    test_client = df['ClientID'].iloc[122]
    print(f"Recommandations pour client {test_client}:")
    print(recommander_produits(test_client))
