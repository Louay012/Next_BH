from googletrans import Translator

def traduire_fr_ar_long(texte, chunk_size=4000):
    """
    Traduit un texte long du français vers l'arabe en découpant le texte en morceaux.

    Args:
        texte (str): texte en français à traduire
        chunk_size (int): taille maximale de chaque morceau (en caractères)

    Returns:
        str: texte traduit en arabe
    """
    traducteur = Translator()
    resultats = []
    
    # Découper le texte en morceaux
    for i in range(0, len(texte), chunk_size):
        morceau = texte[i:i+chunk_size]
        traduction = traducteur.translate(morceau, src='fr', dest='ar')
        resultats.append(traduction.text)
    
    # Combiner tous les morceaux traduits
    return " ".join(resultats)

# Exemple d'utilisation
texte_fr = """Madame,
En tant que chef de grande entreprise de 500 salariés et plus, votre rôle vous impose des responsabilitables considérables...
(votre texte complet ici)"""

texte_ar = traduire_fr_ar_long(texte_fr)
print(texte_ar)
