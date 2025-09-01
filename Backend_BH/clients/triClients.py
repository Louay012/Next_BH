import pandas as pd

XLSX_PATH = "D:/fezaimohamedelamine/ia_genrative/BHAssurance/BD/new_data.xlsx"
RESULT_PATH = "D:/fezaimohamedelamine/ia_genrative/BHAssurance/BD/resultat_clients.xlsx"

# Charger les tables
personne_physique = pd.read_excel(XLSX_PATH, sheet_name="personne_physique")
personne_morale = pd.read_excel(XLSX_PATH, sheet_name="personne_morale")
contrats = pd.read_excel(XLSX_PATH, sheet_name="Contrats")
sinistres = pd.read_excel(XLSX_PATH, sheet_name="sinistres")

# Fusion clients + contrats
clients = pd.concat([personne_physique, personne_morale], ignore_index=True, sort=False)
df = contrats.merge(clients, on="REF_PERSONNE", how="left")

# Ajouter sinistres
df = df.merge(
    sinistres.groupby("NUM_CONTRAT").size().reset_index(name="nb_sinistres"),
    on="NUM_CONTRAT", how="left"
).fillna({"nb_sinistres": 0})

# Exemple de scoring
df["score"] = 0
df["score"] += (df["Capital_assure"].astype(float) / 10000).clip(0, 5)  # max 5 pts
df["score"] += df["statut_paiement"].apply(lambda x: 5 if x == "Payé" else -3)
df["score"] += df["nb_sinistres"].apply(lambda x: 3 if x == 0 else (-2 if x <= 2 else -5))

# Trier les clients
top_clients = df.sort_values("score", ascending=False)

# Enregistrer le résultat dans un fichier Excel
top_clients.to_excel(RESULT_PATH, index=False)

print(f"✅ Résultat enregistré dans : {RESULT_PATH}")
