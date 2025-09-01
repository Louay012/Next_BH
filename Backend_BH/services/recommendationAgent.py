

# --- Charger la liste des clients depuis un fichier Excel trié ---
import pandas as pd


def get_clients_sorted(xlsx_path):
    df = pd.read_excel(xlsx_path, sheet_name="personne_physique")
    # On suppose que la colonne REF_PERSONNE existe
    df_sorted = df.sort_values(by="REF_PERSONNE")  # tri croissant
    return df_sorted["REF_PERSONNE"].tolist()

# --- Exemple d'utilisation ---
def get_agent():
    df=get_clients_sorted("D:/fezaimohamedelamine/ia_genrative/Backend_BH/BD/new_data.xlsx")
    for client_ref in df:
        from ..tools.agent5 import get_recommendations
        result = get_recommendations(str(client_ref))
        print(f"Recommandations pour le client {client_ref}: {result}")
    
    