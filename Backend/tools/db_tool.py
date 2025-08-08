import pandas as pd

# 📁 Charger toutes les feuilles depuis un fichier Excel
def charger_donnees(filepath):
    excel_data = pd.read_excel(filepath, sheet_name=None)
    return excel_data

# 🛠 Tool : lire le parcours d’un client
def lire_parcours_client(client_id, filepath):
    data = charger_donnees(filepath)

    df_clients = data["Clients"]
    df_contrats = data["Contrats"]
    df_opps = data["Opportunités"]

    # ✅ 1. Infos de base du client
    client_info = df_clients[df_clients["ClientID"] == client_id].to_dict(orient="records")
    if not client_info:
        return {"error": "Client non trouvé"}
    client_info = client_info[0]

    # ✅ 2. Contrats souscrits
    contrats = df_contrats[df_contrats["ClientID"] == client_id].to_dict(orient="records")

    # ✅ 3. Opportunités existantes
    opps = df_opps[df_opps["ClientID"] == client_id].to_dict(orient="records")

    # Résultat structuré
    result = {
        "client_id": client_id,
        "profil": {
            "nom": client_info["Nom"],
            "prenom": client_info["Prénom"],
            "age": calculer_age(client_info["DateNaissance"]),
            "profession": client_info["Profession"],
            "revenus": client_info["RevenusMensuels"],
            "situation": client_info["SituationFamiliale"],
            "sexe": client_info["Sexe"],
            "email": client_info["Email"],
            "telephone": client_info["Téléphone"],
            "whatsapp": client_info["WhatsApp"]
        },
        "contrats": contrats,
        "opportunites": opps
    }

    return result

# 👴 Fonction utilitaire pour calculer l’âge
from datetime import datetime

def calculer_age(date_naissance):
    today = datetime.today()
    return today.year - date_naissance.year - ((today.month, today.day) < (date_naissance.month, date_naissance.day))

# Exemple d'utilisation

# 🛠 Tool : Extraire les contrats des clients similaires
def contrats_clients_similaires(profil_input, filepath):
    data = charger_donnees(filepath)
    
    df_clients = data["Clients"]
    df_contrats = data["Contrats"]

    # Extraire les caractéristiques de filtrage
    age = profil_input.get("age")
    profession = profil_input.get("profession")
    revenus = profil_input.get("revenus")
    situation = profil_input.get("situation")
    sexe = profil_input.get("sexe")

    # Calculer l’âge pour tous les clients
    df_clients["Age"] = df_clients["DateNaissance"].apply(calculer_age)

    # 🧠 Critères de similarité (tu peux les adapter)
    age_tolerance = 5
    revenus_tolerance = 1000

    # 🔍 Filtrer les clients similaires
    clients_similaires = df_clients[
        (df_clients["Profession"] == profession) &
        (df_clients["SituationFamiliale"] == situation) &
        (df_clients["Sexe"] == sexe) &
        (df_clients["Age"].between(age - age_tolerance, age + age_tolerance)) &
        (df_clients["RevenusMensuels"].between(revenus - revenus_tolerance, revenus + revenus_tolerance))
    ]

    if clients_similaires.empty:
        return {"message": "Aucun client similaire trouvé."}

    # Extraire les IDs des clients similaires
    ids_similaires = clients_similaires["ClientID"].tolist()

    # 🗂 Récupérer les contrats de ces clients
    contrats_similaires = df_contrats[df_contrats["ClientID"].isin(ids_similaires)].to_dict(orient="records")

    return {
        "profil_recherche": profil_input,
        "nombre_clients_similaires": len(ids_similaires),
        "contrats_recommandés": contrats_similaires
    }


parcours = lire_parcours_client(1, "Données_Assurance_S2.xlsx")
print(parcours)


