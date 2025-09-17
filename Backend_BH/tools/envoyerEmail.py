import smtplib
from email.mime.text import MIMEText

def envoyer_email_complet(texte_complet: str, destinataire: str):
    """
    Envoie un email HTML basé sur une template BH Assurance améliorée (design moderne).
    
    Args:
        texte_complet (str): Contenu du corps du mail (texte ou HTML)
        destinataire (str): Adresse email du destinataire
    """

    # === Paramètres expéditeur ===
    sender_email = "yahyabenahmed522@gmail.com"
    sender_password = "pygq wnzv tuta lswk"  # ⚠️ mot de passe d’application Gmail

    sujet = "🌟 BH Assurance — Nouveautés Exclusives"

    # === Template HTML créative ===
    html_template = f"""\
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="UTF-8" />
        <title>{sujet}</title>
      </head>
      <body style="margin:0; padding:0; font-family: Arial, sans-serif; background:linear-gradient(135deg, #f0f4ff, #e8faff);">
        <table width="100%" cellpadding="0" cellspacing="0" border="0">
          <tr>
            <td align="center">
              <table width="650" cellpadding="0" cellspacing="0" border="0" 
                     style="background:#ffffff; margin:30px auto; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,0.1); overflow:hidden;">
                
                <!-- HEADER -->
                <tr>
                  <td align="center" style="background:linear-gradient(90deg, #0066cc, #0099ff); padding:30px;">
                    <h1 style="color:#ffffff; margin:0; font-size:28px;">BH Assurance</h1>
                    <p style="color:#e0e0e0; margin:5px 0 0; font-size:14px;">Votre partenaire confiance en assurance</p>
                  </td>
                </tr>
                
                <!-- CONTENU -->
                <tr>
                  <td style="padding:30px; font-size:16px; color:#333333; line-height:1.6;">
                    {texte_complet}
                    
                    <!-- Exemple d'encadré -->
                    <div style="margin-top:20px; padding:15px; background:#f9fbff; border-left:4px solid #0066cc; border-radius:8px;">
                      🚀 <b>Astuce :</b> Profitez de nos offres spéciales en ligne et gagnez du temps !
                    </div>
                  </td>
                </tr>
                
                <!-- CTA -->
                <tr>
                  <td align="center" style="padding:20px;">
                    <a href="https://bhassurance.tn" 
                       style="display:inline-block; padding:12px 24px; background:#0066cc; color:#ffffff; 
                              text-decoration:none; border-radius:6px; font-size:16px; font-weight:bold;">
                      Découvrir nos offres →
                    </a>
                  </td>
                </tr>
                
                <!-- FOOTER -->
                <tr>
                  <td align="center" style="padding:20px; background:#f0f4f8; font-size:12px; color:#666666;">
                    <p style="margin:0;">© 2025 BH Assurance — Tous droits réservés</p>
                    <p style="margin:5px 0;">
                      <a href="https://bhassurance.tn" style="color:#0066cc; text-decoration:none;">Visitez notre site</a> |
                      <a href="#" style="color:#0066cc; text-decoration:none;">Se désabonner</a>
                    </p>
                    
                    <!-- Icônes sociales -->
                    <p style="margin-top:10px;">
                      <a href="https://facebook.com" style="margin:0 8px; text-decoration:none;">
                        🌐 Facebook
                      </a>
                      <a href="https://linkedin.com" style="margin:0 8px; text-decoration:none;">
                        💼 LinkedIn
                      </a>
                      <a href="https://twitter.com" style="margin:0 8px; text-decoration:none;">
                        🐦 Twitter
                      </a>
                    </p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
      </body>
    </html>
    """

    # === Création du message ===
    msg = MIMEText(html_template, "html", "utf-8")
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


# =============================
# Exemple d'appel
# =============================

