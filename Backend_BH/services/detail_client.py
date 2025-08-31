import pandas as pd


import numpy as np

XLSX_PATH = "C:/Users/louay/OneDrive/Desktop/NEXT_BH/Backend_BH/BD/new_data.xlsx"
def to_native_types(obj):
    """Convertit les types numpy/pandas en types Python natifs (JSON-friendly)."""
    if isinstance(obj, dict):
        return {k: to_native_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_native_types(v) for v in obj]
    elif isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    elif pd.isna(obj):  # NaN, NaT etc.
        return None  # Replace NaN with None
    else:
        return obj
# --- Charger les tables depuis Excel ---
def load_tables(xlsx_path):
    personne_physique = pd.read_excel(xlsx_path, sheet_name="personne_physique")
    personne_morale = pd.read_excel(xlsx_path, sheet_name="personne_morale")
    
    # Forcer REF_PERSONNE en string pour éviter les erreurs de type
    personne_physique["REF_PERSONNE"] = personne_physique["REF_PERSONNE"].astype(str).str.strip()
    personne_morale["REF_PERSONNE"] = personne_morale["REF_PERSONNE"].astype(str).str.strip()
    
    return personne_physique, personne_morale

# --- Fonction pour récupérer les infos d'un client ---
def get_client_info(ref_personne):
    ref_personne = str(ref_personne).strip()
    pp, pm = load_tables(XLSX_PATH)

    if ref_personne in pp['REF_PERSONNE'].values:
        client = pp[pp['REF_PERSONNE'] == ref_personne].iloc[0]
        return to_native_types({
            "type": "personne_physique",
            "nom_prenom": client['NOM_PRENOM'],
            "date_naissance": client['DATE_NAISSANCE'],
            "lieu_naissance": client['LIEU_NAISSANCE'],
            "sexe": client['CODE_SEXE'],
            "situation_familiale": client['SITUATION_FAMILIALE'],
            "numero_piece_identite": client['NUM_PIECE_IDENTITE'],
            "secteur_activite": client['LIB_SECTEUR_ACTIVITE'],
            "profession": client['LIB_PROFESSION'],
            "ville": client['VILLE'],
            "gouvernorat": client['LIB_GOUVERNORAT']
        })

    elif ref_personne in pm['REF_PERSONNE'].values:
        client = pm[pm['REF_PERSONNE'] == ref_personne].iloc[0]
        return to_native_types({
            "type": "personne_morale",
            "raison_sociale": client['RAISON_SOCIALE'],
            "matricule_fiscale": client['MATRICULE_FISCALE'],
            "secteur_activite": client['LIB_SECTEUR_ACTIVITE'],
            "activite": client['LIB_ACTIVITE'],
            "ville": client['VILLE'],
            "gouvernorat": client['LIB_GOUVERNORAT']
        })

    else:
        return {"error": f"REF_PERSONNE {ref_personne} introuvable"}


# --- Exemple d'utilisation ---
"""ref = "715"
info_client = get_client_info(ref)
print(info_client)"""