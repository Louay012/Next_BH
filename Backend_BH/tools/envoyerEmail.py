import smtplib
from email.mime.text import MIMEText

def envoyer_email_complet(texte_complet: str, destinataire: str):
    """
    Envoie un email en utilisant Gmail SMTP.
    
    Args:
        texte_complet (str): Contenu complet du mail commençant par "Objet : ..."
        destinataire (str): Adresse email du destinataire
    """

    # === Paramètres de l'expéditeur (à personnaliser) ===
    sender_email = "yahyabenahmed522@gmail.com"
    sender_password = "pygq wnzv tuta lswk"  # ⚠️ mot de passe d’application Gmail

    # === Séparation Objet et Corps ===
    lignes = texte_complet.strip().split("\n", 1)  # coupe la première ligne du reste
    if lignes[0].lower().startswith("objet"):
        sujet = lignes[0].replace("Objet :", "").strip()
        corps = lignes[1].strip() if len(lignes) > 1 else ""
    else:
        sujet = "Recommandation de produit adaptée pour vous"
        corps = texte_complet.strip()


    # === Création du message ===
    msg = MIMEText(corps, "plain", "utf-8")
    msg["Subject"] = sujet
    msg["From"] = sender_email
    msg["To"] = destinataire

    # === Connexion SMTP et envoi ===
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, destinataire, msg.as_string())
            print(f"✅ Email envoyé à {destinataire} avec sujet : {sujet}")
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi : {e}")

