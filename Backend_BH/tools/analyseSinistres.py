import pandas as pd

# --- 1. Charger les tables depuis Excel ---
XLSX_PATH = "D:/fezaimohamedelamine/ia_genrative/BHAssurance/BD/new_data.xlsx"

def load_tables(xlsx_path):
    personne_physique = pd.read_excel(xlsx_path, sheet_name="personne_physique")
    personne_morale = pd.read_excel(xlsx_path, sheet_name="personne_morale")
    contrats = pd.read_excel(xlsx_path, sheet_name="Contrats")
    sinistres = pd.read_excel(xlsx_path, sheet_name="sinistres")
    return personne_physique, personne_morale, contrats, sinistres

# --- 2. Récupérer les infos personnelles du client ---
def get_infos_client(ref_personne: str):
    personne_physique, personne_morale, _, _ = load_tables(XLSX_PATH)

    client = personne_physique[personne_physique["REF_PERSONNE"] == int(ref_personne)]
    client_type = "physique"
    if client.empty:
        client = personne_morale[personne_morale["REF_PERSONNE"] == int(ref_personne)]
        client_type = "morale"

    if client.empty:
        return {"error": f"Aucun client trouvé pour {ref_personne}"}

    return {
        "type_client": client_type,
        "infos_personnelles": client.to_dict(orient="records")[0]
    }

# --- 3. Récupérer le dernier contrat et les sinistres ---
def get_sinistres_dernier_contrat(ref_personne: str, contrats_df, sinistres_df):
    # Filtrer les contrats du client
    contrats_client = contrats_df[contrats_df['REF_PERSONNE'] == int(ref_personne)].copy()
    if contrats_client.empty:
        return {"error": f"Aucun contrat trouvé pour le client {ref_personne}"}

    # Convertir les dates
    for col in ['DATE_EXPIRATION', 'EFFET_CONTRAT']:
        if col in contrats_client.columns:
            contrats_client[col] = pd.to_datetime(contrats_client[col], errors="coerce")

    # Identifier le dernier contrat (par expiration ou effet)
    if 'DATE_EXPIRATION' in contrats_client and contrats_client['DATE_EXPIRATION'].notna().any():
        dernier = contrats_client.sort_values(by='DATE_EXPIRATION', ascending=False).iloc[0]
    else:
        dernier = contrats_client.sort_values(by='EFFET_CONTRAT', ascending=False).iloc[0]

    num_contrat = dernier['NUM_CONTRAT']

    # Récupérer les sinistres du dernier contrat
    sins = sinistres_df[sinistres_df['NUM_CONTRAT'] == num_contrat].copy()

    sinistres_list = []
    if not sins.empty:
        for _, row in sins.iterrows():
            sinistres_list.append({
                "NUM_SINISTRE": str(row["NUM_SINISTRE"]),
                "NATURE_SINISTRE": row.get("NATURE_SINISTRE"),
                "DATE_SURVENANCE": str(row.get("DATE_SURVENANCE")),
                "MONTANT_ENCAISSE": float(row.get("MONTANT_ENCAISSE", 0) or 0),
                "MONTANT_A_ENCAISSER": float(row.get("MONTANT_A_ENCAISSER", 0) or 0)
            })

    return {
        "dernier_contrat": {
            "NUM_CONTRAT": str(dernier["NUM_CONTRAT"]),
            "LIB_PRODUIT": dernier.get("LIB_PRODUIT"),
            "EFFET_CONTRAT": str(dernier.get("EFFET_CONTRAT")),
            "DATE_EXPIRATION": str(dernier.get("DATE_EXPIRATION"))
        },
        "sinistres_dernier_contrat": sinistres_list
    }

def get_sinistres_client(ref_personne: str):
    """
    Récupère les informations personnelles d'un client ainsi que la liste des sinistres associés à son dernier contrat.

    Cette fonction charge les données depuis un fichier Excel, identifie le client (personne physique ou morale) à partir de sa référence,
    puis extrait les informations du dernier contrat du client et les sinistres qui y sont liés.

    Args:
        ref_personne (str): La référence unique du client (identifiant).

    Returns:
        dict: Un dictionnaire contenant deux clés :
            - "infos_client" : informations personnelles du client (type et détails).
            - "sinistres_dernier_contrat" : informations sur le dernier contrat et la liste des sinistres associés.
    """
    _, _, contrats_df, sinistres_df = load_tables(XLSX_PATH)
    result ={}
    result["infos_client"]= get_infos_client(ref_personne)
    result["sinistres_dernier_contrat"]=get_sinistres_dernier_contrat(ref_personne, contrats_df, sinistres_df)

    return result

# --- 4. Exemple d'utilisation ---
"""if __name__ == "__main__":
    ref_personne = "1381"  # ID du client

    # Infos personnelles
    infos_client = get_infos_client(ref_personne)
    print("📌 Infos personnelles:")
    print(infos_client)

    # Dernier contrat et sinistres
    _, _, contrats_df, sinistres_df = load_tables(XLSX_PATH)
    sinistres_client = get_sinistres_dernier_contrat(ref_personne, contrats_df, sinistres_df)
    print("\n⚠️ Dernier contrat et sinistres:")
    print(sinistres_client)"""
