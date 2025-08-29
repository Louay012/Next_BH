from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document


bh_products={
    "VIE": {
        "produit: TEMPORAIRE DECES ": [
            "DECES DOUBLEMENT: Dans le cadre du produit TEMPORAIRE DECES, garantie décès doublée : elle prévoit le versement d’un capital égal au double du montant assuré si le décès de l’assuré survient par accident.",
            "DECES TRIPLEMENT: Dans le cadre du produit TEMPORAIRE DECES, garantie décès triplée (transport) : versement d’un capital triple en cas de décès accidentel d’un membre d’équipage ou d’un passager assuré.",
            "EXONERATION: Dans le cadre du produit TEMPORAIRE DECES, garantie exonération des cotisations : en cas d’invalidité ou d’incapacité reconnue, l’assureur prend en charge le paiement des primes afin de maintenir les garanties en vigueur.",
            "DECES - I.D.T: Dans le cadre du produit TEMPORAIRE DECES, garantie décès et invalidité totale et définitive : elle verse le capital prévu au contrat en cas de décès de l’assuré ou d’invalidité définitive totale l’empêchant d’exercer toute activité rémunérée."
        ],
        "TEMPORAIRE DECES A CAPITAL DECROISSANT LINEAIREMENT": [
            "DECES - I.D.T: Dans le cadre du produit TEMPORAIRE DECES A CAPITAL DECROISSANT LINEAIREMENT, garantie décès et invalidité totale et définitive : elle verse le capital prévu au contrat en cas de décès de l’assuré ou d’invalidité définitive totale l’empêchant d’exercer toute activité rémunérée."
        ],
        "produit: ASSURANCE MIXTE VIE": [
            "EN CAS DE VIE: Dans le cadre du produit ASSURANCE MIXTE VIE, prestations en cas de vie : à l’échéance du contrat, un capital ou une rente est versé si l’assuré est en vie, constituant ainsi une épargne programmée.",
            "DECES DOUBLEMENT: Dans le cadre du produit ASSURANCE MIXTE VIE, garantie décès doublée : elle prévoit le versement d’un capital égal au double du montant assuré si le décès de l’assuré survient par accident.",
            "DECES TRIPLEMENT: Dans le cadre du produit ASSURANCE MIXTE VIE, garantie décès triplée (transport) : versement d’un capital triple en cas de décès accidentel d’un membre d’équipage ou d’un passager assuré.",
            "EXONERATION: Dans le cadre du produit ASSURANCE MIXTE VIE, garantie exonération des cotisations : en cas d’invalidité ou d’incapacité reconnue, l’assureur prend en charge le paiement des primes afin de maintenir les garanties en vigueur.",
            "DECES - I.D.T: Dans le cadre du produit ASSURANCE MIXTE VIE, garantie décès et invalidité totale et définitive : elle verse le capital prévu au contrat en cas de décès de l’assuré ou d’invalidité définitive totale l’empêchant d’exercer toute activité rémunérée."
        ],
        "produit: ASSURANCE VIE COMPLEMENT RETRAITE - HORIZON ": [
            "DECES DOUBLEMENT: Dans le cadre du produit ASSURANCE VIE COMPLEMENT RETRAITE - HORIZON, garantie décès doublée : elle prévoit le versement d’un capital égal au double du montant assuré si le décès de l’assuré survient par accident.",
            "DECES - I.D.T: Dans le cadre du produit ASSURANCE VIE COMPLEMENT RETRAITE - HORIZON, garantie décès et invalidité totale et définitive : elle verse le capital prévu au contrat en cas de décès de l’assuré ou d’invalidité définitive totale l’empêchant d’exercer toute activité rémunérée.",
            "EPARGNE: Dans le cadre du produit ASSURANCE VIE COMPLEMENT RETRAITE - HORIZON, garantie épargne : elle permet de constituer un capital grâce aux primes versées, capital qui est restitué à l’assuré ou aux bénéficiaires au terme du contrat ou en cas de décès.",
            "HOSPITALISATION: Dans le cadre du produit ASSURANCE VIE COMPLEMENT RETRAITE - HORIZON, garantie hospitalisation : elle prévoit le versement d’une indemnité journalière ou la prise en charge de frais en cas d’hospitalisation de l’assuré suite à un accident ou à une maladie couverte.",
            "INCAPACITE TEMPORAIRE PARTIELLE OU TOTALE DE TRAVAIL: Dans le cadre du produit ASSURANCE VIE COMPLEMENT RETRAITE - HORIZON, garantie incapacité temporaire de travail : elle indemnise l’assuré en cas d’arrêt de travail total ou partiel, en versant des prestations destinées à compenser la perte de revenus."
        ],
        "produit: ASSURANCE VIE COMPLEMENT RETRAITE - HORIZON": [
            "DECES TRIPLEMENT: Dans le cadre du produit ASSURANCE VIE COMPLEMENT RETRAITE - HORIZON, garantie décès triplée (transport) : versement d’un capital triple en cas de décès accidentel d’un membre d’équipage ou d’un passager assuré."
        ],
        "produit: ASSURANCE VIE COMPLEMENT RETRAITE - HORIZON+ ": [
            "DECES DOUBLEMENT: Dans le cadre du produit ASSURANCE VIE COMPLEMENT RETRAITE - HORIZON+, garantie décès doublée : elle prévoit le versement d’un capital égal au double du montant assuré si le décès de l’assuré survient par accident.",
            "DECES TRIPLEMENT: Dans le cadre du produit ASSURANCE VIE COMPLEMENT RETRAITE - HORIZON+, garantie décès triplée (transport) : versement d’un capital triple en cas de décès accidentel d’un membre d’équipage ou d’un passager assuré.",
            "DECES - I.D.T: Dans le cadre du produit ASSURANCE VIE COMPLEMENT RETRAITE - HORIZON+, garantie décès et invalidité totale et définitive : elle verse le capital prévu au contrat en cas de décès de l’assuré ou d’invalidité définitive totale l’empêchant d’exercer toute activité rémunérée.",
            "EPARGNE: Dans le cadre du produit ASSURANCE VIE COMPLEMENT RETRAITE - HORIZON+, garantie épargne : elle permet de constituer un capital grâce aux primes versées, capital qui est restitué à l’assuré ou aux bénéficiaires au terme du contrat ou en cas de décès.",
            "HOSPITALISATION: Dans le cadre du produit ASSURANCE VIE COMPLEMENT RETRAITE - HORIZON+, garantie hospitalisation : elle prévoit le versement d’une indemnité journalière ou la prise en charge de frais en cas d’hospitalisation de l’assuré suite à un accident ou à une maladie couverte.",
            "INCAPACITE TEMPORAIRE PARTIELLE OU TOTALE DE TRAVAIL: Dans le cadre du produit ASSURANCE VIE COMPLEMENT RETRAITE - HORIZON+, garantie incapacité temporaire de travail : elle indemnise l’assuré en cas d’arrêt de travail total ou partiel, en versant des prestations destinées à compenser la perte de revenus."
        ],
        "produit: RENTE EDUCATION": [
            "DECES - I.D.T: Dans le cadre du produit RENTE EDUCATION, garantie décès et invalidité totale et définitive : elle verse le capital prévu au contrat en cas de décès de l’assuré ou d’invalidité définitive totale l’empêchant d’exercer toute activité rémunérée.",
            "EPARGNE: Dans le cadre du produit RENTE EDUCATION, garantie épargne : elle permet de constituer un capital grâce aux primes versées, capital qui est restitué à l’assuré ou aux bénéficiaires au terme du contrat ou en cas de décès."
        ],
        "produit: DHAMEN": [
            "DECES - I.D.T: Dans le cadre du produit DHAMEN, garantie décès et invalidité totale et définitive : elle verse le capital prévu au contrat en cas de décès de l’assuré ou d’invalidité définitive totale l’empêchant d’exercer toute activité rémunérée.",
            "INCAPACITE TEMPORAIRE PARTIELLE OU TOTALE DE TRAVAIL: Dans le cadre du produit DHAMEN, garantie incapacité temporaire de travail : elle indemnise l’assuré en cas d’arrêt de travail total ou partiel, en versant des prestations destinées à compenser la perte de revenus.",
            "INVALIDITE DEFINITIVE PARTIELLE OU TOTALE: Dans le cadre du produit DHAMEN, garantie invalidité permanente : elle prévoit le versement d’un capital ou d’une rente en cas d’invalidité définitive partielle ou totale reconnue par expertise médicale."
        ],
        "produit: DHAMEN RETRAITE": [
            "EPARGNE: Dans le cadre du produit DHAMEN RETRAITE, garantie épargne : elle permet de constituer un capital grâce aux primes versées, capital qui est restitué à l’assuré ou aux bénéficiaires au terme du contrat ou en cas de décès.",
            "INCAPACITE TEMPORAIRE PARTIELLE OU TOTALE DE TRAVAIL: Dans le cadre du produit DHAMEN RETRAITE, garantie incapacité temporaire de travail : elle indemnise l’assuré en cas d’arrêt de travail total ou partiel, en versant des prestations destinées à compenser la perte de revenus.",
            "INVALIDITE DEFINITIVE PARTIELLE OU TOTALE: Dans le cadre du produit DHAMEN RETRAITE, garantie invalidité permanente : elle prévoit le versement d’un capital ou d’une rente en cas d’invalidité définitive partielle ou totale reconnue par expertise médicale."
        ],
        "produit: CREDIT STOCK": [
            "DECES - I.D.T: Dans le cadre du produit CREDIT STOCK, garantie décès et invalidité totale et définitive : elle verse le capital prévu au contrat en cas de décès de l’assuré ou d’invalidité définitive totale l’empêchant d’exercer toute activité rémunérée.",
            "INCAPACITE TEMPORAIRE PARTIELLE OU TOTALE DE TRAVAIL: Dans le cadre du produit CREDIT STOCK, garantie incapacité temporaire de travail : elle indemnise l’assuré en cas d’arrêt de travail total ou partiel, en versant des prestations destinées à compenser la perte de revenus.",
            "INVALIDITE DEFINITIVE PARTIELLE OU TOTALE: Dans le cadre du produit CREDIT STOCK, garantie invalidité permanente : elle prévoit le versement d’un capital ou d’une rente en cas d’invalidité définitive partielle ou totale reconnue par expertise médicale."
        ],
        "produit: DHAMEN COMPTE": [
            "DECES - I.D.T: Dans le cadre du produit DHAMEN COMPTE, garantie décès et invalidité totale et définitive : elle verse le capital prévu au contrat en cas de décès de l’assuré ou d’invalidité définitive totale l’empêchant d’exercer toute activité rémunérée.",
            "HOSPITALISATION: Dans le cadre du produit DHAMEN COMPTE, garantie hospitalisation : elle prévoit le versement d’une indemnité journalière ou la prise en charge de frais en cas d’hospitalisation de l’assuré suite à un accident ou à une maladie couverte.",
            "INCAPACITE TEMPORAIRE PARTIELLE OU TOTALE DE TRAVAIL: Dans le cadre du produit DHAMEN COMPTE, garantie incapacité temporaire de travail : elle indemnise l’assuré en cas d’arrêt de travail total ou partiel, en versant des prestations destinées à compenser la perte de revenus.",
            "INVALIDITE DEFINITIVE PARTIELLE OU TOTALE: Dans le cadre du produit DHAMEN COMPTE, garantie invalidité permanente : elle prévoit le versement d’un capital ou d’une rente en cas d’invalidité définitive partielle ou totale reconnue par expertise médicale."
        ],
        "produit: ASSUR SENIOR": [
            "DECES: Dans le cadre du produit ASSUR SENIOR, garantie décès : en cas de décès de l’assuré durant la période couverte, un capital est versé au bénéficiaire désigné.",
            "MALADIE REDOUTEE: Dans le cadre du produit ASSUR SENIOR, garantie maladies redoutées : elle prévoit un capital en cas de diagnostic d’une maladie grave (cancer, infarctus, AVC…) définie au contrat."
        ],
        "produit: CARTES BANCAIRES": [
            "DECES: Dans le cadre du produit CARTES BANCAIRES, garantie décès : en cas de décès de l’assuré durant la période couverte, un capital est versé au bénéficiaire désigné.",
            "USAGE FRAUDULEUX: Dans le cadre du produit CARTES BANCAIRES, garantie usage frauduleux des moyens de paiement : elle rembourse les pertes subies en cas d’utilisation frauduleuse des cartes ou moyens de paiement de l’assuré à la suite d’un vol ou d’une perte, ainsi que les frais de remplacement des clés et papiers【202102935357688†L116-L129】.",
            "DECES - I.D.T: Dans le cadre du produit CARTES BANCAIRES, garantie décès et invalidité totale et définitive : elle verse le capital prévu au contrat en cas de décès de l’assuré ou d’invalidité définitive totale l’empêchant d’exercer toute activité rémunérée.",
            "EPARGNE: Dans le cadre du produit CARTES BANCAIRES, garantie épargne : elle permet de constituer un capital grâce aux primes versées, capital qui est restitué à l’assuré ou aux bénéficiaires au terme du contrat ou en cas de décès.",
            "INCAPACITE TEMPORAIRE PARTIELLE OU TOTALE DE TRAVAIL: Dans le cadre du produit CARTES BANCAIRES, garantie incapacité temporaire de travail : elle indemnise l’assuré en cas d’arrêt de travail total ou partiel, en versant des prestations destinées à compenser la perte de revenus.",
            "INVALIDITE DEFINITIVE PARTIELLE OU TOTALE: Dans le cadre du produit CARTES BANCAIRES, garantie invalidité permanente : elle prévoit le versement d’un capital ou d’une rente en cas d’invalidité définitive partielle ou totale reconnue par expertise médicale.",
            "VOL, PERTE, USAGE FRAUDULEUX: Dans le cadre du produit CARTES BANCAIRES, garantie perte, vol et usage frauduleux : elle couvre l’assuré contre la perte ou le vol de ses moyens de paiement et rembourse les dépenses résultant d’une utilisation frauduleuse ; elle prend également en charge le remplacement des clés, des papiers d’identité ou des espèces dérobées【202102935357688†L116-L129】."
        ]
    },
    "RISQUES DIVERS": {
        "produit: VOL AVEC EFFRACTION MOBILIER D HABITATION": [
            "VOL : Dans le cadre du produit VOL AVEC EFFRACTION MOBILIER D HABITATION, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier.",
            "DETERIORATION MOBILIERE ET IMMOBILIERE SUITE VOL: Dans le cadre du produit VOL AVEC EFFRACTION MOBILIER D HABITATION, indemnisation des détériorations mobilières et immobilières causées par une effraction ou un vol (porte fracturée, serrures forcées, mobilier endommagé).",
            "OBJETS DANS LES DEPENDANCES: Dans le cadre du produit VOL AVEC EFFRACTION MOBILIER D HABITATION, garantie objets dans les dépendances : elle couvre le vol d’objets entreposés dans des dépendances (garage, cave, abri) situées sur le lieu assuré."
        ],
        "produit: VOL AVEC EFFRACTION DES MARCHANDISES DE TOUTE NATURE": [
            "VOL : Dans le cadre du produit VOL AVEC EFFRACTION DES MARCHANDISES DE TOUTE NATURE, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier."
        ],
        "produit: VOL DES RISQUES ACCESSOIRES": [
            "VOL : Dans le cadre du produit VOL DES RISQUES ACCESSOIRES, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier.",
            "RECONSTITUTION D ARCHIVES: Dans le cadre du produit VOL DES RISQUES ACCESSOIRES, prise en charge des frais de reconstitution d’archives, de dossiers et de documents professionnels détruits ou volés à la suite d’un sinistre.",
            "DETERIORATION MOBILIERE ET IMMOBILIERE SUITE VOL: Dans le cadre du produit VOL DES RISQUES ACCESSOIRES, indemnisation des détériorations mobilières et immobilières causées par une effraction ou un vol (porte fracturée, serrures forcées, mobilier endommagé)."
        ],
        "produit: VOL CONTENU DES COFFRES-FORTS DANS LES BANQUS,BUREAUX ET MAGASINS": [
            "VOL : Dans le cadre du produit VOL CONTENU DES COFFRES-FORTS DANS LES BANQUS,BUREAUX ET MAGASINS, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier.",
            "Vol avec effraction pendant les heures de travail par le personnel: Dans le cadre du produit VOL CONTENU DES COFFRES-FORTS DANS LES BANQUS,BUREAUX ET MAGASINS, garantie vol avec effraction commis par le personnel pendant les heures de travail : elle couvre la disparition de biens résultant d’une effraction réalisée par des employés sur le lieu assuré.",
            "Vol avec violence sur le détenteur des clefs: Dans le cadre du produit VOL CONTENU DES COFFRES-FORTS DANS LES BANQUS,BUREAUX ET MAGASINS, garantie vol avec violence sur le détenteur des clefs : indemnisation des biens volés lorsqu’une personne est contrainte par violence ou menace à remettre les clés des locaux.",
            "Vol avec violence ou menaces dite \\\"CHANTILLY\\\": Dans le cadre du produit VOL CONTENU DES COFFRES-FORTS DANS LES BANQUS,BUREAUX ET MAGASINS, garantie vol sous menaces (dite ‘Chantilly’) : elle couvre les vols commis avec violence ou menaces sur les personnes présentes dans les locaux assurés."
        ],
        "produit: VOL SUR LA PERSONNE ET PERTE PAR CAS DE FORCE MAJEURE": [
            "VOL : Dans le cadre du produit VOL SUR LA PERSONNE ET PERTE PAR CAS DE FORCE MAJEURE, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier."
        ],
        "produit: DETOURNEMENT DES ESPECES MONNAEES ET VALEURS PAR LE PERSONNEL": [
            "VOL : Dans le cadre du produit DETOURNEMENT DES ESPECES MONNAEES ET VALEURS PAR LE PERSONNEL, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier."
        ],
        "produit: VOL TOUTE CATEGORIES": [
            "VOL : Dans le cadre du produit VOL TOUTE CATEGORIES, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier.",
            "PERTE INDIRECTE: Dans le cadre du produit VOL TOUTE CATEGORIES, garantie perte indirecte : elle couvre les dépenses supplémentaires et pertes financières consécutives à un sinistre (retard de chantier, loyers…).",
            "HONORAIRE EXPERT: Dans le cadre du produit VOL TOUTE CATEGORIES, remboursement des honoraires de l’expert mandaté pour évaluer les dommages à la suite d’un sinistre.",
            "DETERIORATION MOBILIERE ET IMMOBILIERE SUITE VOL: Dans le cadre du produit VOL TOUTE CATEGORIES, indemnisation des détériorations mobilières et immobilières causées par une effraction ou un vol (porte fracturée, serrures forcées, mobilier endommagé).",
            "VOL-DETOURNEMENT DE FOND: Dans le cadre du produit VOL TOUTE CATEGORIES, garantie vol ou détournement de fonds : indemnisation des sommes détournées ou volées par des employés ou des tiers lors de l’exploitation de l’entreprise."
        ],
        "produit: BRIS DE GLACE": [
            "BRIS DE GLACES: Dans le cadre du produit BRIS DE GLACE, garantie bris de glaces : elle couvre la réparation ou le remplacement des vitres, vitrines, miroirs ou surfaces en verre endommagés.",
            "DOMMAGES MATERIIELS DES LUNETTES : Dans le cadre du produit BRIS DE GLACE, indemnisation des dommages matériels subis par les lunettes (verres ou monture) assurées."
        ],
        "produit: DEGATS DES EAUX": [
            "DEGATS DES EAUX: Dans le cadre du produit DEGATS DES EAUX, garantie dégâts des eaux : elle prend en charge les dommages causés par des fuites, ruptures de conduites, débordements ou infiltrations accidentelles d’eau.",
            "RECONSTITUTION D ARCHIVES: Dans le cadre du produit DEGATS DES EAUX, prise en charge des frais de reconstitution d’archives, de dossiers et de documents professionnels détruits ou volés à la suite d’un sinistre.",
            "PERTE DE LOYER: Dans le cadre du produit DEGATS DES EAUX, remboursement de la perte de loyer subie par le propriétaire lorsque le bien devient inhabitable à la suite d’un sinistre garanti.",
            "HONORAIRE EXPERT: Dans le cadre du produit DEGATS DES EAUX, remboursement des honoraires de l’expert mandaté pour évaluer les dommages à la suite d’un sinistre.",
            "PRIVATION DE JOUISSANCE: Dans le cadre du produit DEGATS DES EAUX, indemnité pour privation de jouissance : elle compense la perte d’usage du logement ou des locaux pendant la remise en état après un sinistre.",
            "RECOURS DES LOCATAIRES: Dans le cadre du produit DEGATS DES EAUX, garantie recours des locataires : elle protège le propriétaire contre les réclamations de ses locataires pour dommages causés à leurs biens lors d’un sinistre touchant l’immeuble.",
            "RECOURS DU PROPRIETAIRE: Dans le cadre du produit DEGATS DES EAUX, garantie recours du propriétaire : elle protège le locataire contre les réclamations du propriétaire en cas de dommages causés au logement ou à l’immeuble.",
            "INFILTRATIONS ACCIDENTELLES AU TRAVERS DES TOITURES: Dans le cadre du produit DEGATS DES EAUX, indemnisation des dommages provoqués par des infiltrations d’eau accidentelles à travers la toiture ou la couverture du bâtiment.",
            "RECOURS DES VOISINS ET TIERS: Dans le cadre du produit DEGATS DES EAUX, garantie recours des voisins et tiers : elle couvre la responsabilité de l’assuré vis‑à‑vis des voisins et des tiers en cas de dommages provoqués par un sinistre survenu dans le bâtiment assuré.",
            "FRAIS DE RECHERCHE DES FUITES D EAUX: Dans le cadre du produit DEGATS DES EAUX, prise en charge des frais engagés pour localiser et diagnostiquer l’origine d’une fuite d’eau responsable d’un sinistre."
        ],
        "produit: R.C MEDECIN": [
            "RESPONSABILITE CIVILE: Dans le cadre du produit R.C MEDECIN, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport.",
            "RC- DOMMAGES CORPORELS: Dans le cadre du produit R.C MEDECIN, responsabilité civile – dommages corporels : prise en charge des indemnités dues aux tiers pour les blessures ou atteintes corporelles causées par l’assuré.",
            "RC- DOMMAGES MATERIELS: Dans le cadre du produit R.C MEDECIN, responsabilité civile – dommages matériels : indemnisation des dégâts matériels causés à des biens appartenant à des tiers."
        ],
        "produit: R.C PARAMEDICALE": [
            "RESPONSABILITE CIVILE: Dans le cadre du produit R.C PARAMEDICALE, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport.",
            "RC- DOMMAGES CORPORELS: Dans le cadre du produit R.C PARAMEDICALE, responsabilité civile – dommages corporels : prise en charge des indemnités dues aux tiers pour les blessures ou atteintes corporelles causées par l’assuré.",
            "RC- DOMMAGES MATERIELS: Dans le cadre du produit R.C PARAMEDICALE, responsabilité civile – dommages matériels : indemnisation des dégâts matériels causés à des biens appartenant à des tiers.",
            "RC- PROFESSIONNELLE: Dans le cadre du produit R.C PARAMEDICALE, responsabilité civile professionnelle : elle couvre les dommages causés à des tiers dans le cadre de l’activité professionnelle de l’assuré."
        ],
        "produit: R.C PHARMACIEN": [
            "RESPONSABILITE CIVILE: Dans le cadre du produit R.C PHARMACIEN, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport."
        ],
        "produit: R.C PROFESSION CULINAIRE": [
            "RESPONSABILITE CIVILE: Dans le cadre du produit R.C PROFESSION CULINAIRE, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport.",
            "RC- DOMMAGES CORPORELS: Dans le cadre du produit R.C PROFESSION CULINAIRE, responsabilité civile – dommages corporels : prise en charge des indemnités dues aux tiers pour les blessures ou atteintes corporelles causées par l’assuré.",
            "RC- DOMMAGES MATERIELS: Dans le cadre du produit R.C PROFESSION CULINAIRE, responsabilité civile – dommages matériels : indemnisation des dégâts matériels causés à des biens appartenant à des tiers.",
            "RC- INTOXICATION ALIMENTAIRE: Dans le cadre du produit R.C PROFESSION CULINAIRE, responsabilité civile – intoxication alimentaire : indemnisation des victimes de toxi‑infections alimentaires causées par des aliments préparés ou vendus par l’assuré."
        ],
        "produit: R.C STATION DE SERVICE": [
            "RESPONSABILITE CIVILE: Dans le cadre du produit R.C STATION DE SERVICE, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport."
        ],
        "produit: R.C CHEF DE FAMILLE DETENTEUR D UN ANIMAL DOMESTIQUE": [
            "RESPONSABILITE CIVILE: Dans le cadre du produit R.C CHEF DE FAMILLE DETENTEUR D UN ANIMAL DOMESTIQUE, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport.",
            "RC- DOMMAGES CORPORELS: Dans le cadre du produit R.C CHEF DE FAMILLE DETENTEUR D UN ANIMAL DOMESTIQUE, responsabilité civile – dommages corporels : prise en charge des indemnités dues aux tiers pour les blessures ou atteintes corporelles causées par l’assuré.",
            "RC- DOMMAGES MATERIELS: Dans le cadre du produit R.C CHEF DE FAMILLE DETENTEUR D UN ANIMAL DOMESTIQUE, responsabilité civile – dommages matériels : indemnisation des dégâts matériels causés à des biens appartenant à des tiers."
        ],
        "produit: R.C GARDERIE ET JARDIN D ENFANTS": [
            "DECES: Dans le cadre du produit R.C GARDERIE ET JARDIN D ENFANTS, garantie décès : en cas de décès de l’assuré durant la période couverte, un capital est versé au bénéficiaire désigné.",
            "INVALIDITE PERMANENTE: Dans le cadre du produit R.C GARDERIE ET JARDIN D ENFANTS, cette garantie couvre les risques spécifiques liés à 'INVALIDITE PERMANENTE'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "MALADIE: Dans le cadre du produit R.C GARDERIE ET JARDIN D ENFANTS, garantie frais médicaux : prise en charge des dépenses de santé (consultations, médicaments, hospitalisation) engagées par l’assuré.",
            "RESPONSABILITE CIVILE: Dans le cadre du produit R.C GARDERIE ET JARDIN D ENFANTS, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport.",
            "RC- DOMMAGES CORPORELS: Dans le cadre du produit R.C GARDERIE ET JARDIN D ENFANTS, responsabilité civile – dommages corporels : prise en charge des indemnités dues aux tiers pour les blessures ou atteintes corporelles causées par l’assuré.",
            "RC- DOMMAGES MATERIELS: Dans le cadre du produit R.C GARDERIE ET JARDIN D ENFANTS, responsabilité civile – dommages matériels : indemnisation des dégâts matériels causés à des biens appartenant à des tiers."
        ],
        "produit: R.C COLONIES DE VACANCES": [
            "DECES: Dans le cadre du produit R.C COLONIES DE VACANCES, garantie décès : en cas de décès de l’assuré durant la période couverte, un capital est versé au bénéficiaire désigné.",
            "INVALIDITE PERMANENTE: Dans le cadre du produit R.C COLONIES DE VACANCES, cette garantie couvre les risques spécifiques liés à 'INVALIDITE PERMANENTE'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "MALADIE: Dans le cadre du produit R.C COLONIES DE VACANCES, garantie frais médicaux : prise en charge des dépenses de santé (consultations, médicaments, hospitalisation) engagées par l’assuré.",
            "RESPONSABILITE CIVILE: Dans le cadre du produit R.C COLONIES DE VACANCES, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport."
        ],
        "produit: R.C ETABLISSEMENT EDUCATION PHYSIQUE ET SPORTIVES": [
            "DECES: Dans le cadre du produit R.C ETABLISSEMENT EDUCATION PHYSIQUE ET SPORTIVES, garantie décès : en cas de décès de l’assuré durant la période couverte, un capital est versé au bénéficiaire désigné.",
            "INVALIDITE PERMANENTE: Dans le cadre du produit R.C ETABLISSEMENT EDUCATION PHYSIQUE ET SPORTIVES, cette garantie couvre les risks spécifiques liés à 'INVALIDITE PERMANENTE'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "MALADIE: Dans le cadre du produit R.C ETABLISSEMENT EDUCATION PHYSIQUE ET SPORTIVES, garantie frais médicaux : prise en charge des dépenses de santé (consultations, médicaments, hospitalisation) engagées par l’assuré.",
            "RESPONSABILITE CIVILE: Dans le cadre du produit R.C ETABLISSEMENT EDUCATION PHYSIQUE ET SPORTIVES, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport."
        ],
        "produit: R.C ETABLISSEMENT ENSEIGNEMENT (PRIVE /PUBLIC)": [
            "DECES: Dans le cadre du produit R.C ETABLISSEMENT ENSEIGNEMENT (PRIVE /PUBLIC), garantie décès : en cas de décès de l’assuré durant la période couverte, un capital est versé au bénéficiaire désigné.",
            "INVALIDITE PERMANENTE: Dans le cadre du produit R.C ETABLISSEMENT ENSEIGNEMENT (PRIVE /PUBLIC), cette garantie couvre les risques spécifiques liés à 'INVALIDITE PERMANENTE'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "MALADIE: Dans le cadre du produit R.C ETABLISSEMENT ENSEIGNEMENT (PRIVE /PUBLIC), garantie frais médicaux : prise en charge des dépenses de santé (consultations, médicaments, hospitalisation) engagées par l’assuré.",
            "RESPONSABILITE CIVILE: Dans le cadre du produit R.C ETABLISSEMENT ENSEIGNEMENT (PRIVE /PUBLIC), garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport."
        ],
        "produit: R.C CHASSE TERRESTRE ": [
            "DECES: Dans le cadre du produit R.C CHASSE TERRESTRE, garantie décès : en cas de décès de l’assuré durant la période couverte, un capital est versé au bénéficiaire désigné.",
            "INVALIDITE PERMANENTE: Dans le cadre du produit R.C CHASSE TERRESTRE, cette garantie couvre les risques spécifiques liés à 'INVALIDITE PERMANENTE'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "MALADIE: Dans le cadre du produit R.C CHASSE TERRESTRE, garantie frais médicaux : prise en charge des dépenses de santé (consultations, médicaments, hospitalisation) engagées par l’assuré.",
            "RESPONSABILITE CIVILE: Dans le cadre du produit R.C CHASSE TERRESTRE, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport."
        ],
        "produit: R.C BAIN MAURE - DOUCHE": [
            "RESPONSABILITE CIVILE: Dans le cadre du produit R.C BAIN MAURE - DOUCHE, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport.",
            "RC- DOMMAGES CORPORELS: Dans le cadre du produit R.C BAIN MAURE - DOUCHE, responsabilité civile – dommages corporels : prise en charge des indemnités dues aux tiers pour les blessures ou atteintes corporelles causées par l’assuré.",
            "RC- DOMMAGES MATERIELS: Dans le cadre du produit R.C BAIN MAURE - DOUCHE, responsabilité civile – dommages matériels : indemnisation des dégâts matériels causés à des biens appartenant à des tiers.",
            "RC EFFETS DES CLIENTS: Dans le cadre du produit R.C BAIN MAURE - DOUCHE, garantie responsabilité des effets des clients : elle couvre la perte ou la détérioration des objets confiés par les clients (vêtements, bagages, etc.)."
        ],
        "produit: R.C EMBARCATION DE PLAISANCE": [
            "RESPONSABILITE CIVILE: Dans le cadre du produit R.C EMBARCATION DE PLAISANCE, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport.",
            "RC REMORQUAGE DE SKI NAUTIQUE OU D'AQUTIQUE: Dans le cadre du produit R.C EMBARCATION DE PLAISANCE, responsabilité civile pour le remorquage de ski nautique ou d’engins aquatiques : elle couvre les dommages corporels ou matériels causés aux tiers au cours de ces activités.",
            "RC- DOMMAGES CORPORELS: Dans le cadre du produit R.C EMBARCATION DE PLAISANCE, responsabilité civile – dommages corporels : prise en charge des indemnités dues aux tiers pour les blessures ou atteintes corporelles causées par l’assuré.",
            "RC- DOMMAGES MATERIELS: Dans le cadre du produit R.C EMBARCATION DE PLAISANCE, responsabilité civile – dommages matériels : indemnisation des dégâts matériels causés à des biens appartenant à des tiers."
        ],
        "produit: R.C PROMONEUR EN CALECHE OU SUR MONTURE": [
            "RESPONSABILITE CIVILE: Dans le cadre du produit R.C PROMONEUR EN CALECHE OU SUR MONTURE, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport."
        ],
        "produit: R.C & INDIVIDUELLE COMPLEMENTAIRE PECHE ET PLONGE SOUS MARINE": [
            "DECES: Dans le cadre du produit R.C & INDIVIDUELLE COMPLEMENTAIRE PECHE ET PLONGE SOUS MARINE, garantie décès : en cas de décès de l’assuré durant la période couverte, un capital est versé au bénéficiaire désigné.",
            "INVALIDITE PERMANENTE: Dans le cadre du produit R.C & INDIVIDUELLE COMPLEMENTAIRE PECHE ET PLONGE SOUS MARINE, cette garantie couvre les risques spécifiques liés à 'INVALIDITE PERMANENTE'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "MALADIE: Dans le cadre du produit R.C & INDIVIDUELLE COMPLEMENTAIRE PECHE ET PLONGE SOUS MARINE, garantie frais médicaux : prise en charge des dépenses de santé (consultations, médicaments, hospitalisation) engagées par l’assuré.",
            "RESPONSABILITE CIVILE: Dans le cadre du produit R.C & INDIVIDUELLE COMPLEMENTAIRE PECHE ET PLONGE SOUS MARINE, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport."
        ],
        "produit: RC CHASSEUR": [
            "DECES: Dans le cadre du produit RC CHASSEUR, garantie décès : en cas de décès de l’assuré durant la période couverte, un capital est versé au bénéficiaire désigné.",
            "INVALIDITE PERMANENTE: Dans le cadre du produit RC CHASSEUR, cette garantie couvre les risques spécifiques liés à 'INVALIDITE PERMANENTE'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "RESPONSABILITE CIVILE: Dans le cadre du produit RC CHASSEUR, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport.",
            "RC DU CHASSEUR DU FAIT DE SON CHIEN PENDANT TOUTE L'ANNEE: Dans le cadre du produit RC CHASSEUR, responsabilité civile du chasseur pour les dommages causés par son chien durant toute l’année, y compris hors période de chasse."
        ],
        "produit: R.C PARTICULIER-CHEF DE FAMILLE- MAITRE DE MAISON": [
            "RESPONSABILITE CIVILE: Dans le cadre du produit R.C PARTICULIER-CHEF DE FAMILLE- MAITRE DE MAISON, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport.",
            "RC DESCENDANT MAJEURS CELIBATAIRES VIVANT AU FOYER DU SOUSCRIPTEUR: Dans le cadre du produit R.C PARTICULIER-CHEF DE FAMILLE- MAITRE DE MAISON, responsabilité civile pour les actes des enfants majeurs célibataires vivant au foyer de l’assuré.",
            "RC ASCENDANTOU CONJOINT VIVANT AU FOYER DU SOUSCRIPTEUR: Dans le cadre du produit R.C PARTICULIER-CHEF DE FAMILLE- MAITRE DE MAISON, responsabilité civile couvrant les dommages causés par le conjoint ou les ascendants vivant au foyer de l’assuré.",
            "RC CONDUITE VEHICULE TERRESTRE A MOTEUR APPARTENANT A UN TIERS: Dans le cadre du produit R.C PARTICULIER-CHEF DE FAMILLE- MAITRE DE MAISON, responsabilité civile pour la conduite occasionnelle d’un véhicule terrestre à moteur appartenant à un tiers.",
            "RC PROPRIETAIRE DE RESIDENCES SECONDAIRES DONT LA SUPERFICIE NE DEPASSE PAS 5000 m2 PAR RESIDENCE: Dans le cadre du produit R.C PARTICULIER-CHEF DE FAMILLE- MAITRE DE MAISON, responsabilité civile du propriétaire d’une résidence secondaire (surface maximale 5 000 m²) pour les dommages causés aux voisins et aux tiers.",
            "RC VOL POUR LES EMPLOYES DE MAISON: Dans le cadre du produit R.C PARTICULIER-CHEF DE FAMILLE- MAITRE DE MAISON, responsabilité civile pour les vols commis par les employés de maison chez l’assuré ou chez des tiers."
        ],
        "produit: R.C PROPRIETAIRE D IMMEUBLE": [
            "RESPONSABILITE CIVILE: Dans le cadre du produit R.C PROPRIETAIRE D IMMEUBLE, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport.",
            "RC ASCENSEUR ET MONTE-CHARGE: Dans le cadre du produit R.C PROPRIETAIRE D IMMEUBLE, responsabilité civile de l’exploitant d’ascenseurs et de monte‑charges pour les dommages causés aux usagers."
        ],
        "produit: RC ENTREPRISE DE BATIMENT ET TRAVAUX PUBLIC": [
            "RESPONSABILITE CIVILE: Dans le cadre du produit RC ENTREPRISE DE BATIMENT ET TRAVAUX PUBLIC, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport.",
            "RC- DOMMAGES CORPORELS: Dans le cadre du produit RC ENTREPRISE DE BATIMENT ET TRAVAUX PUBLIC, responsabilité civile – dommages corporels : prise en charge des indemnités dues aux tiers pour les blessures ou atteintes corporelles causées par l’assuré.",
            "RC- DOMMAGES MATERIELS: Dans le cadre du produit RC ENTREPRISE DE BATIMENT ET TRAVAUX PUBLIC, responsabilité civile – dommages matériels : indemnisation des dégâts matériels causés à des biens appartenant à des tiers."
        ],
        "produit: RC ARTISANTS ET COMMERCANTS": [
            "RESPONSABILITE CIVILE: Dans le cadre du produit RC ARTISANTS ET COMMERCANTS, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport.",
            "RC- DOMMAGES CORPORELS: Dans le cadre du produit RC ARTISANTS ET COMMERCANTS, responsabilité civile – dommages corporels : prise en charge des indemnités dues aux tiers pour les blessures ou atteintes corporelles causées par l’assuré.",
            "RC- DOMMAGES MATERIELS: Dans le cadre du produit RC ARTISANTS ET COMMERCANTS, responsabilité civile – dommages matériels : indemnisation des dégâts matériels causés à des biens appartenant à des tiers."
        ],
        "produit: RC HOTELIERS": [
            "RESPONSABILITE CIVILE: Dans le cadre du produit RC HOTELIERS, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport."
        ],
        "produit: RC COIFFEUR": [
            "RESPONSABILITE CIVILE: Dans le cadre du produit RC COIFFEUR, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport."
        ],
        "produit: RC EXPLOITATION DE THEATRE,CINEMA,SALLES DE CONCERTS, DE CONFEREN?CES ET DE SPECTACLES": [
            "RESPONSABILITE CIVILE: Dans le cadre du produit RC EXPLOITATION DE THEATRE,CINEMA,SALLES DE CONCERTS, DE CONFEREN?CES ET DE SPECTACLES, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport."
        ],
        "produit: RC EXPLOITATION ATTRACTION FORAINES": [
            "RESPONSABILITE CIVILE: Dans le cadre du produit RC EXPLOITATION ATTRACTION FORAINES, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport."
        ],
        "produit: RC EXPLOITATION PARKING PAYANT POUR AUTOMOBILES": [
            "RESPONSABILITE CIVILE: Dans le cadre du produit RC EXPLOITATION PARKING PAYANT POUR AUTOMOBILES, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport."
        ],
        "produit: RC AGRICULTURES": [
            "RESPONSABILITE CIVILE: Dans le cadre du produit RC AGRICULTURES, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport."
        ],
        "produit: RC ASSOCIATION SPORTIVES": [
            "MALADIE: Dans le cadre du produit RC ASSOCIATION SPORTIVES, garantie frais médicaux : prise en charge des dépenses de santé (consultations, médicaments, hospitalisation) engagées par l’assuré.",
            "RESPONSABILITE CIVILE: Dans le cadre du produit RC ASSOCIATION SPORTIVES, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport.",
            "DECES - I.D.T: Dans le cadre du produit RC ASSOCIATION SPORTIVES, garantie décès et invalidité totale et définitive : elle verse le capital prévu au contrat en cas de décès de l’assuré ou d’invalidité définitive totale l’empêchant d’exercer toute activité rémunérée."
        ],
        "produit: RC ENTRPRISES INDUSTRIELLES": [
            "RESPONSABILITE CIVILE: Dans le cadre du produit RC ENTRPRISES INDUSTRIELLES, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport."
        ],
        "produit: RESPONSABILITE CIVILE": [
            "DEFENSE ET RECOURS: Dans le cadre du produit RESPONSABILITE CIVILE, garantie défense et recours : elle prend en charge les frais de procédure et d’assistance pour défendre l’assuré ou exercer un recours contre un responsable après un sinistre.",
            "DECES: Dans le cadre du produit RESPONSABILITE CIVILE, garantie décès : en cas de décès de l’assuré durant la période couverte, un capital est versé au bénéficiaire désigné.",
            "INVALIDITE PERMANENTE: Dans le cadre du produit RESPONSABILITE CIVILE, cette garantie couvre les risques spécifiques liés à 'INVALIDITE PERMANENTE'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "INDEMNITE JOURNALIERE: Dans le cadre du produit RESPONSABILITE CIVILE, garantie indemnité journalière : versement d’une indemnité journalière compensant l’arrêt de production ou l’indisponibilité d’un équipement essentiel après un sinistre.",
            "MALADIE: Dans le cadre du produit RESPONSABILITE CIVILE, garantie frais médicaux : prise en charge des dépenses de santé (consultations, médicaments, hospitalisation) engagées par l’assuré.",
            "RESPONSABILITE CIVILE: Dans le cadre du produit RESPONSABILITE CIVILE, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport.",
            "RC CONDUITE VEHICULE TERRESTRE A MOTEUR APPARTENANT A UN TIERS: Dans le cadre du produit RESPONSABILITE CIVILE, responsabilité civile pour la conduite occasionnelle d’un véhicule terrestre à moteur appartenant à un tiers.",
            "RC PROPRIETAIRE DE RESIDENCES SECONDAIRES DONT LA SUPERFICIE NE DEPASSE PAS 5000 m2 PAR RESIDENCE: Dans le cadre du produit RESPONSABILITE CIVILE, responsabilité civile du propriétaire d’une résidence secondaire (surface maximale 5 000 m²) pour les dommages causés aux voisins et aux tiers.",
            "RC VOL POUR LES EMPLOYES DE MAISON: Dans le cadre du produit RESPONSABILITE CIVILE, responsabilité civile pour les vols commis par les employés de maison chez l’assuré ou chez des tiers.",
            "RC CROISEE: Dans le cadre du produit RESPONSABILITE CIVILE, responsabilité civile croisée : chaque partie co‑assurée est considérée comme tierce l’une vis‑à‑vis de l’autre, ce qui permet l’indemnisation croisée des dommages.",
            "RC- DOMMAGES CORPORELS: Dans le cadre du produit RESPONSABILITE CIVILE, responsabilité civile – dommages corporels : prise en charge des indemnités dues aux tiers pour les blessures ou atteintes corporelles causées par l’assuré.",
            "RC- DOMMAGES MATERIELS: Dans le cadre du produit RESPONSABILITE CIVILE, responsabilité civile – dommages matériels : indemnisation des dégâts matériels causés à des biens appartenant à des tiers.",
            "RC- INTOXICATION ALIMENTAIRE: Dans le cadre du produit RESPONSABILITE CIVILE, responsabilité civile – intoxication alimentaire : indemnisation des victimes de toxi‑infections alimentaires causées par des aliments préparés ou vendus par l’assuré.",
            "RC- PROFESSIONNELLE: Dans le cadre du produit RESPONSABILITE CIVILE, responsabilité civile professionnelle : elle couvre les dommages causés à des tiers dans le cadre de l’activité professionnelle de l’assuré."
        ],
        "produit: INDIVIDUELLE ACCIDENTS": [
            "DECES: Dans le cadre du produit INDIVIDUELLE ACCIDENTS, garantie décès : en cas de décès de l’assuré durant la période couverte, un capital est versé au bénéficiaire désigné.",
            "INVALIDITE PERMANENTE: Dans le cadre du produit INDIVIDUELLE ACCIDENTS, cette garantie couvre les risques spécifiques liés à 'INVALIDITE PERMANENTE'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "INDEMNITE JOURNALIERE: Dans le cadre du produit INDIVIDUELLE ACCIDENTS, garantie indemnité journalière : versement d’une indemnité journalière compensant l’arrêt de production ou l’indisponibilité d’un équipement essentiel après un sinistre.",
            "MALADIE: Dans le cadre du produit INDIVIDUELLE ACCIDENTS, garantie frais médicaux : prise en charge des dépenses de santé (consultations, médicaments, hospitalisation) engagées par l’assuré."
        ],
        "produit: INDIVIDUELLE ACCIDENTS ASSOCIE AU CONTRAT AUTO": [
            "DECES: Dans le cadre du produit INDIVIDUELLE ACCIDENTS ASSOCIE AU CONTRAT AUTO, garantie décès : en cas de décès de l’assuré durant la période couverte, un capital est versé au bénéficiaire désigné.",
            "INVALIDITE PERMANENTE: Dans le cadre du produit INDIVIDUELLE ACCIDENTS ASSOCIE AU CONTRAT AUTO, cette garantie couvre les risques spécifiques liés à 'INVALIDITE PERMANENTE'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "INDEMNITE JOURNALIERE: Dans le cadre du produit INDIVIDUELLE ACCIDENTS ASSOCIE AU CONTRAT AUTO, garantie indemnité journalière : versement d’une indemnité journalière compensant l’arrêt de production ou l’indisponibilité d’un équipement essentiel après un sinistre.",
            "MALADIE: Dans le cadre du produit INDIVIDUELLE ACCIDENTS ASSOCIE AU CONTRAT AUTO, garantie frais médicaux : prise en charge des dépenses de santé (consultations, médicaments, hospitalisation) engagées par l’assuré."
        ],
        "produit: ASSISTANCES EN VOYAGES - PLAN BASIQUE": [
            "ASSISTANCES VOYAGES: Dans le cadre du produit ASSISTANCES EN VOYAGES - PLAN BASIQUE, assistance voyages : elle couvre les frais de recherche, de secours et de rapatriement lors de voyages ainsi que l’assistance médicale à l’étranger.",
            "COVID19: Dans le cadre du produit ASSISTANCES EN VOYAGES - PLAN BASIQUE, cette garantie couvre les risques spécifiques liés à 'COVID19'. Veuillez consulter le contrat pour connaître le détail des prestations."
        ],
        "produit: ASSISTANCES EN VOYAGES - PLAN BUSINESS": [
            "ASSISTANCES VOYAGES: Dans le cadre du produit ASSISTANCES EN VOYAGES - PLAN BUSINESS, assistance voyages : elle couvre les frais de recherche, de secours et de rapatriement lors de voyages ainsi que l’assistance médicale à l’étranger."
        ],
        "produit: ASSISTANCES EN VOYAGES - PLAN GOLDEN": [
            "ASSISTANCES VOYAGES: Dans le cadre du produit ASSISTANCES EN VOYAGES - PLAN GOLDEN, assistance voyages : elle couvre les frais de recherche, de secours et de rapatriement lors de voyages ainsi que l’assistance médicale à l’étranger."
        ],
        "produit: ASSISTANCES EN VOYAGES - PLAN ETUDIANT": [
            "ASSISTANCES VOYAGES: Dans le cadre du produit ASSISTANCES EN VOYAGES - PLAN ETUDIANT, assistance voyages : elle couvre les frais de recherche, de secours et de rapatriement lors de voyages ainsi que l’assistance médicale à l’étranger."
        ],
        "produit: ASSISTANCES EN VOYAGES - PLAN ETUDIANT+": [
            "ASSISTANCES VOYAGES: Dans le cadre du produit ASSISTANCES EN VOYAGES - PLAN ETUDIANT+, assistance voyages : elle couvre les frais de recherche, de secours et de rapatriement lors de voyages ainsi que l’assistance médicale à l’étranger."
        ],
        "produit: ASSISTANCE DOMICILIAIRE": [
            "ASSISTANCE DOMICILIAIRE: Dans le cadre du produit ASSISTANCE DOMICILIAIRE, garantie assistance domiciliaire : elle organise l’envoi de professionnels (plombier, serrurier, électricien…) et prend en charge certains frais pour les petites interventions urgentes au domicile."
        ],
        "produit: CARTES BANCAIRES": [
            "ASSISTANCES VOYAGES: Dans le cadre du produit CARTES BANCAIRES, assistance voyages : elle couvre les frais de recherche, de secours et de rapatriement lors de voyages ainsi que l’assistance médicale à l’étranger.",
            "VOL : Dans le cadre du produit CARTES BANCAIRES, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier.",
            "ASSISTANCE: Dans le cadre du produit CARTES BANCAIRES, garantie assistance : elle met à disposition un service d’assistance 24h/24 (conseils, information, aide d’urgence) et organise les interventions nécessaires en cas d’imprévu.",
            "USAGE FRAUDULEUX: Dans le cadre du produit CARTES BANCAIRES, garantie usage frauduleux des moyens de paiement : elle rembourse les pertes subies en cas d’utilisation frauduleuse des cartes ou moyens de paiement de l’assuré à la suite d’un vol ou d’une perte, ainsi que les frais de remplacement des clés et papiers【202102935357688†L116-L129】.",
            "MISE EN OPPOSITION: Dans le cadre du produit CARTES BANCAIRES, cette garantie couvre les risques spécifiques liés à 'MISE EN OPPOSITION'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "ASSISTANCE DOMICILIAIRE: Dans le cadre du produit CARTES BANCAIRES, garantie assistance domiciliaire : elle organise l’envoi de professionnels (plombier, serrurier, électricien…) et prend en charge certains frais pour les petites interventions urgentes au domicile.",
            "ACHATS PROTEGES: Dans le cadre du produit CARTES BANCAIRES, cette garantie couvre les risques spécifiques liés à 'ACHATS PROTEGES'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "VOL, PERTE, USAGE FRAUDULEUX: Dans le cadre du produit CARTES BANCAIRES, garantie perte, vol et usage frauduleux : elle couvre l’assuré contre la perte ou le vol de ses moyens de paiement et rembourse les dépenses résultant d’une utilisation frauduleuse ; elle prend également en charge le remplacement des clés, des papiers d’identité ou des espèces dérobées【202102935357688†L116-L129】.",
            "FRAIS DE RECONFECTION DE LA CARTE: Dans le cadre du produit CARTES BANCAIRES, prise en charge des frais de reconstitution ou de remplacement de la carte bancaire après une perte ou un vol.",
            "FRAIS DE RECONFECTION DES SERRURES, CLES PERDUES AVEC LA CARTE: Dans le cadre du produit CARTES BANCAIRES, remboursement des coûts de remplacement des serrures et des clés lorsqu’elles ont été perdues ou volées en même temps que la carte bancaire.",
            "FRAIS DE REMPLACEMENT DES PAPIERS D IDENTITES OFFICIELS PERDUS AVEC LA CARTE: Dans le cadre du produit CARTES BANCAIRES, prise en charge des frais administratifs pour refaire les papiers d’identité officiels perdus ou volés avec la carte bancaire.",
            "SERVICE MEDIPHONE: Dans le cadre du produit CARTES BANCAIRES, service Mediphone : accès à une plateforme téléphonique offrant des conseils médicaux et une orientation vers les services appropriés."
        ],
        "produit: ASSISTANCE DES VEHICULES": [
            "PEUGEOT ASSISTANCE: Dans le cadre du produit ASSISTANCE DES VEHICULES, peugeot Assistance : service d’assistance dédié aux véhicules de la marque, comprenant dépannage, remorquage et prestations spécifiques selon la gamme."
        ],
        "produit: ASSISTANCE PROTECTION JURIDIQUE": [
            "ASSISTANCE JURIDIQUE: Dans le cadre du produit ASSISTANCE PROTECTION JURIDIQUE, garantie assistance juridique : elle fournit des conseils juridiques et prend en charge les frais de procédure en cas de litige couvert.",
            "ACHAT ET VENTE DE BIENS OU DE PRESTATION DE SERVICE: Dans le cadre du produit ASSISTANCE PROTECTION JURIDIQUE, protection juridique achat et vente de biens ou de prestations de service : elle accompagne l’assuré en cas de litige avec un vendeur ou un prestataire (non‑conformité, vice caché, retard de livraison).",
            "HABITATION ET MENUS TRAVAUX IMMOBILIERS: Dans le cadre du produit ASSISTANCE PROTECTION JURIDIQUE, protection juridique habitation et travaux : elle couvre les frais d’avocat et d’expertise lors de litiges liés à l’habitation ou à de petits travaux immobiliers.",
            "SALARIES: Dans le cadre du produit ASSISTANCE PROTECTION JURIDIQUE, protection juridique relative au droit du travail : elle conseille et défend l’assuré dans ses litiges avec des salariés (contrats, licenciements, harcèlement).",
            "SANTE: Dans le cadre du produit ASSISTANCE PROTECTION JURIDIQUE, protection juridique santé : elle assiste l’assuré lors de litiges liés à la santé (erreur médicale, remboursement de soins, litiges avec un établissement de santé).",
            "RECOURS CORPOREL/ATTEINTE A L INTEGRITE PHYSIQUE: Dans le cadre du produit ASSISTANCE PROTECTION JURIDIQUE, protection juridique recours corporel : elle permet de faire valoir les droits de l’assuré en cas d’atteinte à son intégrité physique (accident, agression) et de réclamer indemnisation.",
            "USURPATION D IDENTITE: Dans le cadre du produit ASSISTANCE PROTECTION JURIDIQUE, protection juridique usurpation d’identité : elle apporte aide et conseils pour rétablir l’identité de l’assuré et se défendre contre les conséquences d’un vol d’identité.",
            "DEFENSE PENALE: Dans le cadre du produit ASSISTANCE PROTECTION JURIDIQUE, garantie défense pénale : elle couvre les frais d’avocat et de procédure engagés pour assurer la défense pénale de l’assuré en cas de poursuites.",
            "PROTECTION SOCIALE/PREVOYANCE/RETRAITE: Dans le cadre du produit ASSISTANCE PROTECTION JURIDIQUE, protection juridique en matière sociale, de prévoyance et de retraite : assistance en cas de litige avec les organismes sociaux ou les caisses de retraite.",
            "FISCALITE: Dans le cadre du produit ASSISTANCE PROTECTION JURIDIQUE, protection juridique fiscalité : elle apporte assistance et défense en cas de litige avec l’administration fiscale (redressement, contentieux).",
            "EMPLOIS FAMILIAUX: Dans le cadre du produit ASSISTANCE PROTECTION JURIDIQUE, protection juridique emplois familiaux : elle informe et défend l’assuré dans les litiges concernant l’emploi d’un salarié à domicile (contrat, rupture, responsabilité).",
            "SUCCESSION: Dans le cadre du produit ASSISTANCE PROTECTION JURIDIQUE, protection juridique succession : elle accompagne l’assuré dans les démarches et litiges liés à une succession (partage, contestation de testament)."
        ]
    },
    "AUTOMOBILE": {
        "produit: AUTOMOBILE": [
            "RC - RTI: Dans le cadre du produit AUTOMOBILE, responsabilité civile automobile : garantie obligatoire couvrant les dommages corporels et matériels causés aux tiers lors d’un accident impliquant le véhicule assuré.",
            "DEFENSE ET RECOURS: Dans le cadre du produit AUTOMOBILE, garantie défense et recours : elle prend en charge les frais de procédure et d’assistance pour défendre l’assuré ou exercer un recours contre un responsable après un sinistre.",
            "INCENDIE: Dans le cadre du produit AUTOMOBILE, garantie incendie : elle indemnise les dommages causés par le feu, la foudre, l’explosion ou la chute de la foudre aux bâtiments et contenus assurés.",
            "VOL : Dans le cadre du produit AUTOMOBILE, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier.",
            "DOMMAGES AU VEHICULE: Dans le cadre du produit AUTOMOBILE, garantie dommages au véhicule : elle couvre les réparations du véhicule assuré à la suite d’un accident responsable ou non.",
            "DOMMAGES ET COLLISION: Dans le cadre du produit AUTOMOBILE, garantie dommages et collision : elle indemnise les dommages causés par une collision avec un autre véhicule ou un obstacle identifié.",
            "BRIS DE GLACES: Dans le cadre du produit AUTOMOBILE, garantie bris de glaces : elle couvre la réparation ou le remplacement des vitres, vitrines, miroirs ou surfaces en verre endommagés.",
            "P.T.A: Dans le cadre du produit AUTOMOBILE, garantie perte totale accidentelle (PTA) : elle prévoit l’indemnisation de la valeur du véhicule en cas de destruction totale consécutive à un accident couvert.",
            "ASSISTANCE + et CAR GLASS: Dans le cadre du produit AUTOMOBILE, formule combinée Assistance+ et Car Glass : elle inclut l’assistance renforcée et la prise en charge des réparations de vitrages du véhicule.",
            "INDIVIDUELLE ACCIDENT: Dans le cadre du produit AUTOMOBILE, garantie individuelle accident : elle verse un capital ou une rente en cas de décès ou d’invalidité d’une personne assurée lors d’un accident survenu dans les locaux.",
            "CHOC DE VEHICULES TERRESTRES IDENTIFIES: Dans le cadre du produit AUTOMOBILE, indemnisation des dommages causés aux biens assurés par la collision d’un véhicule terrestre identifié.",
            "ASSISTANCE ACCIDENT AUTOMOBILE (3A): Dans le cadre du produit AUTOMOBILE, garantie assistance accident automobile (3A) : en cas d’accident, l’assureur organise le dépannage, le remorquage et éventuellement le rapatriement des occupants.",
            "CATASTROPHE NATURELLE: Dans le cadre du produit AUTOMOBILE, garantie catastrophes naturelles : indemnisation des dommages causés au véhicule par un événement naturel reconnu (inondation, tempête, tremblement de terre…).",
            "EMEUTE ET MOUVEMENT POPULAIRE: Dans le cadre du produit AUTOMOBILE, garantie émeute et mouvements populaires : indemnisation des dommages causés au véhicule par des émeutes, des manifestations ou des actes de vandalisme collectifs.",
            "VOL RADIO CASSETTE: Dans le cadre du produit AUTOMOBILE, garantie vol autoradio : elle rembourse la valeur du système audio (radio, lecteur) volé ou détérioré suite à une effraction du véhicule.",
            "ASSISTANCE +: Dans le cadre du produit AUTOMOBILE, assistance renforcée : elle élargit les prestations d’assistance classiques en prévoyant des services supplémentaires (dépannage à domicile, véhicule de remplacement, logement provisoire).",
            "CAR GLASS: Dans le cadre du produit AUTOMOBILE, garantie Car Glass : prise en charge illimitée du remplacement ou de la réparation des vitrages du véhicule, sans incidence sur le bonus.",
            "ACCIDENT CARE: Dans le cadre du produit AUTOMOBILE, garantie Accident Care : elle couvre les blessures du conducteur et des passagers (frais médicaux, invalidité, décès) à la suite d’un accident de la circulation.",
            "ASSISTANCE GOLD: Dans le cadre du produit AUTOMOBILE, assistance Gold : offre haut de gamme avec dépannage rapide, véhicule de remplacement, prise en charge des frais d’hébergement et assistance aux personnes partout en Europe.",
            "SALIM ASSISTANCE AUTOMOBILE (S2A): Dans le cadre du produit AUTOMOBILE, salim Assistance Automobile (S2A) : service d’assistance automobile incluant le dépannage, le remorquage et le rapatriement des passagers pour les souscripteurs du produit."
        ],
        "produit: AUTOMOBILE II": [
            "RC - RTI: Dans le cadre du produit AUTOMOBILE II, responsabilité civile automobile : garantie obligatoire couvrant les dommages corporels et matériels causés aux tiers lors d’un accident impliquant le véhicule assuré.",
            "DEFENSE ET RECOURS: Dans le cadre du produit AUTOMOBILE II, garantie défense et recours : elle prend en charge les frais de procédure et d’assistance pour défendre l’assuré ou exercer un recours contre un responsable après un sinistre.",
            "INCENDIE: Dans le cadre du produit AUTOMOBILE II, garantie incendie : elle indemnise les dommages causés par le feu, la foudre, l’explosion ou la chute de la foudre aux bâtiments et contenus assurés.",
            "VOL : Dans le cadre du produit AUTOMOBILE II, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier.",
            "DOMMAGES AU VEHICULE: Dans le cadre du produit AUTOMOBILE II, garantie dommages au véhicule : elle couvre les réparations du véhicule assuré à la suite d’un accident responsable ou non.",
            "DOMMAGES ET COLLISION: Dans le cadre du produit AUTOMOBILE II, garantie dommages et collision : elle indemnise les dommages causés par une collision avec un autre véhicule ou un obstacle identifié.",
            "BRIS DE GLACES: Dans le cadre du produit AUTOMOBILE II, garantie bris de glaces : elle couvre la réparation ou le remplacement des vitres, vitrines, miroirs ou surfaces en verre endommagés.",
            "P.T.A: Dans le cadre du produit AUTOMOBILE II, garantie perte totale accidentelle (PTA) : elle prévoit l’indemnisation de la valeur du véhicule en cas de destruction totale consécutive à un accident couvert.",
            "ASSISTANCE + et CAR GLASS: Dans le cadre du produit AUTOMOBILE II, formule combinée Assistance+ et Car Glass : elle inclut l’assistance renforcée et la prise en charge des réparations de vitrages du véhicule.",
            "INDIVIDUELLE ACCIDENT: Dans le cadre du produit AUTOMOBILE II, garantie individuelle accident : elle verse un capital ou une rente en cas de décès ou d’invalidité d’une personne assurée lors d’un accident survenu dans les locaux.",
            "ASSISTANCE ACCIDENT AUTOMOBILE (3A): Dans le cadre du produit AUTOMOBILE II, garantie assistance accident automobile (3A) : en cas d’accident, l’assureur organise le dépannage, le remorquage et éventuellement le rapatriement des occupants.",
            "CATASTROPHE NATURELLE: Dans le cadre du produit AUTOMOBILE II, garantie catastrophes naturelles : indemnisation des dommages causés au véhicule par un événement naturel reconnu (inondation, tempête, tremblement de terre…).",
            "EMEUTE ET MOUVEMENT POPULAIRE: Dans le cadre du produit AUTOMOBILE II, garantie émeute et mouvements populaires : indemnisation des dommages causés au véhicule par des émeutes, des manifestations ou des actes de vandalisme collectifs.",
            "VOL RADIO CASSETTE: Dans le cadre du produit AUTOMOBILE II, garantie vol autoradio : elle rembourse la valeur du système audio (radio, lecteur) volé ou détérioré suite à une effraction du véhicule.",
            "ASSISTANCE +: Dans le cadre du produit AUTOMOBILE II, assistance renforcée : elle élargit les prestations d’assistance classiques en prévoyant des services supplémentaires (dépannage à domicile, véhicule de remplacement, logement provisoire).",
            "CAR GLASS: Dans le cadre du produit AUTOMOBILE II, garantie Car Glass : prise en charge illimitée du remplacement ou de la réparation des vitrages du véhicule, sans incidence sur le bonus.",
            "ACCIDENT CARE: Dans le cadre du produit AUTOMOBILE II, garantie Accident Care : elle couvre les blessures du conducteur et des passagers (frais médicaux, invalidité, décès) à la suite d’un accident de la circulation.",
            "ASSISTANCE GOLD: Dans le cadre du produit AUTOMOBILE II, assistance Gold : offre haut de gamme avec dépannage rapide, véhicule de remplacement, prise en charge des frais d’hébergement et assistance aux personnes partout en Europe.",
            "SALIM ASSISTANCE AUTOMOBILE (S2A): Dans le cadre du produit AUTOMOBILE II, salim Assistance Automobile (S2A) : service d’assistance automobile incluant le dépannage, le remorquage et le rapatriement des passagers pour les souscripteurs du produit.",
            "CATASTROPHES NATURELS (TREMBLEMENT DE TERRE, INONDATION)): Dans le cadre du produit AUTOMOBILE II, indemnisation des dommages causés aux biens ou aux travaux par un tremblement de terre, une inondation ou un glissement de terrain reconnu comme catastrophe naturelle."
        ],
        "produit: OMNICANAL AUTOMOBILE PACK1": [
            "RC - RTI: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK1, responsabilité civile automobile : garantie obligatoire couvrant les dommages corporels et matériels causés aux tiers lors d’un accident impliquant le véhicule assuré.",
            "DEFENSE ET RECOURS: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK1, garantie défense et recours : elle prend en charge les frais de procédure et d’assistance pour défendre l’assuré ou exercer un recours contre un responsable après un sinistre.",
            "INCENDIE: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK1, garantie incendie : elle indemnise les dommages causés par le feu, la foudre, l’explosion ou la chute de la foudre aux bâtiments et contenus assurés.",
            "VOL : Dans le cadre du produit OMNICANAL AUTOMOBILE PACK1, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier.",
            "DOMMAGES AU VEHICULE: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK1, garantie dommages au véhicule : elle couvre les réparations du véhicule assuré à la suite d’un accident responsable ou non.",
            "DOMMAGES ET COLLISION: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK1, garantie dommages et collision : elle indemnise les dommages causés par une collision avec un autre véhicule ou un obstacle identifié.",
            "BRIS DE GLACES: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK1, garantie bris de glaces : elle couvre la réparation ou le remplacement des vitres, vitrines, miroirs ou surfaces en verre endommagés.",
            "P.T.A: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK1, garantie perte totale accidentelle (PTA) : elle prévoit l’indemnisation de la valeur du véhicule en cas de destruction totale consécutive à un accident couvert.",
            "ASSISTANCE + et CAR GLASS: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK1, formule combinée Assistance+ et Car Glass : elle inclut l’assistance renforcée et la prise en charge des réparations de vitrages du véhicule.",
            "INDIVIDUELLE ACCIDENT: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK1, garantie individuelle accident : elle verse un capital ou une rente en cas de décès ou d’invalidité d’une personne assurée lors d’un accident survenu dans les locaux.",
            "CHOC DE VEHICULES TERRESTRES IDENTIFIES: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK1, indemnisation des dommages causés aux biens assurés par la collision d’un véhicule terrestre identifié.",
            "ASSISTANCE ACCIDENT AUTOMOBILE (3A): Dans le cadre du produit OMNICANAL AUTOMOBILE PACK1, garantie assistance accident automobile (3A) : en cas d’accident, l’assureur organise le dépannage, le remorquage et éventuellement le rapatriement des occupants.",
            "CATASTROPHE NATURELLE: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK1, garantie catastrophes naturelles : indemnisation des dommages causés au véhicule par un événement naturel reconnu (inondation, tempête, tremblement de terre…).",
            "EMEUTE ET MOUVEMENT POPULAIRE: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK1, garantie émeute et mouvements populaires : indemnisation des dommages causés au véhicule par des émeutes, des manifestations ou des actes de vandalisme collectifs.",
            "VOL RADIO CASSETTE: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK1, garantie vol autoradio : elle rembourse la valeur du système audio (radio, lecteur) volé ou détérioré suite à une effraction du véhicule.",
            "ASSISTANCE +: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK1, assistance renforcée : elle élargit les prestations d’assistance classiques en prévoyant des services supplémentaires (dépannage à domicile, véhicule de remplacement, logement provisoire).",
            "CAR GLASS: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK1, garantie Car Glass : prise en charge illimitée du remplacement ou de la réparation des vitrages du véhicule, sans incidence sur le bonus.",
            "ACCIDENT CARE: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK1, garantie Accident Care : elle couvre les blessures du conducteur et des passagers (frais médicaux, invalidité, décès) à la suite d’un accident de la circulation.",
            "ASSISTANCE GOLD: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK1, assistance Gold : offre haut de gamme avec dépannage rapide, véhicule de remplacement, prise en charge des frais d’hébergement et assistance aux personnes partout en Europe.",
            "SALIM ASSISTANCE AUTOMOBILE (S2A): Dans le cadre du produit OMNICANAL AUTOMOBILE PACK1, salim Assistance Automobile (S2A) : service d’assistance automobile incluant le dépannage, le remorquage et le rapatriement des passagers pour les souscripteurs du produit."
        ],
        "produit: OMNICANAL AUTOMOBILE PACK2": [
            "RC - RTI: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK2, responsabilité civile automobile : garantie obligatoire couvrant les dommages corporels et matériels causés aux tiers lors d’un accident impliquant le véhicule assuré.",
            "DEFENSE ET RECOURS: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK2, garantie défense et recours : elle prend en charge les frais de procédure et d’assistance pour défendre l’assuré ou exercer un recours contre un responsable après un sinistre.",
            "INCENDIE: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK2, garantie incendie : elle indemnise les dommages causés par le feu, la foudre, l’explosion ou la chute de la foudre aux bâtiments et contenus assurés.",
            "VOL : Dans le cadre du produit OMNICANAL AUTOMOBILE PACK2, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier.",
            "DOMMAGES AU VEHICULE: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK2, garantie dommages au véhicule : elle couvre les réparations du véhicule assuré à la suite d’un accident responsable ou non.",
            "DOMMAGES ET COLLISION: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK2, garantie dommages et collision : elle indemnise les dommages causés par une collision avec un autre véhicule ou un obstacle identifié.",
            "BRIS DE GLACES: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK2, garantie bris de glaces : elle couvre la réparation ou le remplacement des vitres, vitrines, miroirs ou surfaces en verre endommagés.",
            "P.T.A: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK2, garantie perte totale accidentelle (PTA) : elle prévoit l’indemnisation de la valeur du véhicule en cas de destruction totale consécutive à un accident couvert.",
            "ASSISTANCE + et CAR GLASS: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK2, formule combinée Assistance+ et Car Glass : elle inclut l’assistance renforcée et la prise en charge des réparations de vitrages du véhicule.",
            "INDIVIDUELLE ACCIDENT: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK2, garantie individuelle accident : elle verse un capital ou une rente en cas de décès ou d’invalidité d’une personne assurée lors d’un accident survenu dans les locaux.",
            "CHOC DE VEHICULES TERRESTRES IDENTIFIES: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK2, indemnisation des dommages causés aux biens assurés par la collision d’un véhicule terrestre identifié.",
            "ASSISTANCE ACCIDENT AUTOMOBILE (3A): Dans le cadre du produit OMNICANAL AUTOMOBILE PACK2, garantie assistance accident automobile (3A) : en cas d’accident, l’assureur organise le dépannage, le remorquage et éventuellement le rapatriement des occupants.",
            "CATASTROPHE NATURELLE: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK2, garantie catastrophes naturelles : indemnisation des dommages causés au véhicule par un événement naturel reconnu (inondation, tempête, tremblement de terre…).",
            "EMEUTE ET MOUVEMENT POPULAIRE: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK2, garantie émeute et mouvements populaires : indemnisation des dommages causés au véhicule par des émeutes, des manifestations ou des actes de vandalisme collectifs.",
            "VOL RADIO CASSETTE: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK2, garantie vol autoradio : elle rembourse la valeur du système audio (radio, lecteur) volé ou détérioré suite à une effraction du véhicule.",
            "ASSISTANCE +: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK2, assistance renforcée : elle élargit les prestations d’assistance classiques en prévoyant des services supplémentaires (dépannage à domicile, véhicule de remplacement, logement provisoire).",
            "CAR GLASS: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK2, garantie Car Glass : prise en charge illimitée du remplacement ou de la réparation des vitrages du véhicule, sans incidence sur le bonus.",
            "ACCIDENT CARE: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK2, garantie Accident Care : elle couvre les blessures du conducteur et des passagers (frais médicaux, invalidité, décès) à la suite d’un accident de la circulation.",
            "ASSISTANCE GOLD: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK2, assistance Gold : offre haut de gamme avec dépannage rapide, véhicule de remplacement, prise en charge des frais d’hébergement et assistance aux personnes partout en Europe.",
            "SALIM ASSISTANCE AUTOMOBILE (S2A): Dans le cadre du produit OMNICANAL AUTOMOBILE PACK2, salim Assistance Automobile (S2A) : service d’assistance automobile incluant le dépannage, le remorquage et le rapatriement des passagers pour les souscripteurs du produit.",
            "CATASTROPHES NATURELS (TREMBLEMENT DE TERRE, INONDATION)): Dans le cadre du produit OMNICANAL AUTOMOBILE PACK2, indemnisation des dommages causés aux biens ou aux travaux par un tremblement de terre, une inondation ou un glissement de terrain reconnu comme catastrophe naturelle."
        ],
        "produit: OMNICANAL AUTOMOBILE PACK3": [
            "RC - RTI: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK3, responsabilité civile automobile : garantie obligatoire couvrant les dommages corporels et matériels causés aux tiers lors d’un accident impliquant le véhicule assuré.",
            "DEFENSE ET RECOURS: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK3, garantie défense et recours : elle prend en charge les frais de procédure et d’assistance pour défendre l’assuré ou exercer un recours contre un responsable après un sinistre.",
            "INCENDIE: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK3, garantie incendie : elle indemnise les dommages causés par le feu, la foudre, l’explosion ou la chute de la foudre aux bâtiments et contenus assurés.",
            "VOL : Dans le cadre du produit OMNICANAL AUTOMOBILE PACK3, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier.",
            "DOMMAGES AU VEHICULE: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK3, garantie dommages au véhicule : elle couvre les réparations du véhicule assuré à la suite d’un accident responsable ou non.",
            "DOMMAGES ET COLLISION: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK3, garantie dommages et collision : elle indemnise les dommages causés par une collision avec un autre véhicule ou un obstacle identifié.",
            "BRIS DE GLACES: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK3, garantie bris de glaces : elle couvre la réparation ou le remplacement des vitres, vitrines, miroirs ou surfaces en verre endommagés.",
            "P.T.A: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK3, garantie perte totale accidentelle (PTA) : elle prévoit l’indemnisation de la valeur du véhicule en cas de destruction totale consécutive à un accident couvert.",
            "ASSISTANCE + et CAR GLASS: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK3, formule combinée Assistance+ et Car Glass : elle inclut l’assistance renforcée et la prise en charge des réparations de vitrages du véhicule.",
            "INDIVIDUELLE ACCIDENT: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK3, garantie individuelle accident : elle verse un capital ou une rente en cas de décès ou d’invalidité d’une personne assurée lors d’un accident survenu dans les locaux.",
            "CHOC DE VEHICULES TERRESTRES IDENTIFIES: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK3, indemnisation des dommages causés aux biens assurés par la collision d’un véhicule terrestre identifié.",
            "ASSISTANCE ACCIDENT AUTOMOBILE (3A): Dans le cadre du produit OMNICANAL AUTOMOBILE PACK3, garantie assistance accident automobile (3A) : en cas d’accident, l’assureur organise le dépannage, le remorquage et éventuellement le rapatriement des occupants.",
            "CATASTROPHE NATURELLE: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK3, garantie catastrophes naturelles : indemnisation des dommages causés au véhicule par un événement naturel reconnu (inondation, tempête, tremblement de terre…).",
            "EMEUTE ET MOUVEMENT POPULAIRE: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK3, garantie émeute et mouvements populaires : indemnisation des dommages causés au véhicule par des émeutes, des manifestations ou des actes de vandalisme collectifs.",
            "VOL RADIO CASSETTE: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK3, garantie vol autoradio : elle rembourse la valeur du système audio (radio, lecteur) volé ou détérioré suite à une effraction du véhicule.",
            "ASSISTANCE +: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK3, assistance renforcée : elle élargit les prestations d’assistance classiques en prévoyant des services supplémentaires (dépannage à domicile, véhicule de remplacement, logement provisoire).",
            "CAR GLASS: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK3, garantie Car Glass : prise en charge illimitée du remplacement ou de la réparation des vitrages du véhicule, sans incidence sur le bonus.",
            "ACCIDENT CARE: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK3, garantie Accident Care : elle couvre les blessures du conducteur et des passagers (frais médicaux, invalidité, décès) à la suite d’un accident de la circulation.",
            "ASSISTANCE GOLD: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK3, assistance Gold : offre haut de gamme avec dépannage rapide, véhicule de remplacement, prise en charge des frais d’hébergement et assistance aux personnes partout en Europe.",
            "SALIM ASSISTANCE AUTOMOBILE (S2A): Dans le cadre du produit OMNICANAL AUTOMOBILE PACK3, salim Assistance Automobile (S2A) : service d’assistance automobile incluant le dépannage, le remorquage et le rapatriement des passagers pour les souscripteurs du produit."
        ],
        "produit: OMNICANAL AUTOMOBILE PACK PERSONALISE": [
            "RC - RTI: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK PERSONALISE, responsabilité civile automobile : garantie obligatoire couvrant les dommages corporels et matériels causés aux tiers lors d’un accident impliquant le véhicule assuré.",
            "DEFENSE ET RECOURS: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK PERSONALISE, garantie défense et recours : elle prend en charge les frais de procédure et d’assistance pour défendre l’assuré ou exercer un recours contre un responsable après un sinistre.",
            "INCENDIE: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK PERSONALISE, garantie incendie : elle indemnise les dommages causés par le feu, la foudre, l’explosion ou la chute de la foudre aux bâtiments et contenus assurés.",
            "VOL : Dans le cadre du produit OMNICANAL AUTOMOBILE PACK PERSONALISE, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier.",
            "DOMMAGES AU VEHICULE: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK PERSONALISE, garantie dommages au véhicule : elle couvre les réparations du véhicule assuré à la suite d’un accident responsable ou non.",
            "DOMMAGES ET COLLISION: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK PERSONALISE, garantie dommages et collision : elle indemnise les dommages causés par une collision avec un autre véhicule ou un obstacle identifié.",
            "BRIS DE GLACES: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK PERSONALISE, garantie bris de glaces : elle couvre la réparation ou le remplacement des vitres, vitrines, miroirs ou surfaces en verre endommagés.",
            "P.T.A: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK PERSONALISE, garantie perte totale accidentelle (PTA) : elle prévoit l’indemnisation de la valeur du véhicule en cas de destruction totale consécutive à un accident couvert.",
            "ASSISTANCE + et CAR GLASS: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK PERSONALISE, formule combinée Assistance+ et Car Glass : elle inclut l’assistance renforcée et la prise en charge des réparations de vitrages du véhicule.",
            "INDIVIDUELLE ACCIDENT: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK PERSONALISE, garantie individuelle accident : elle verse un capital ou une rente en cas de décès ou d’invalidité d’une personne assurée lors d’un accident survenu dans les locaux.",
            "CHOC DE VEHICULES TERRESTRES IDENTIFIES: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK PERSONALISE, indemnisation des dommages causés aux biens assurés par la collision d’un véhicule terrestre identifié.",
            "ASSISTANCE ACCIDENT AUTOMOBILE (3A): Dans le cadre du produit OMNICANAL AUTOMOBILE PACK PERSONALISE, garantie assistance accident automobile (3A) : en cas d’accident, l’assureur organise le dépannage, le remorquage et éventuellement le rapatriement des occupants.",
            "CATASTROPHE NATURELLE: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK PERSONALISE, garantie catastrophes naturelles : indemnisation des dommages causés au véhicule par un événement naturel reconnu (inondation, tempête, tremblement de terre…).",
            "EMEUTE ET MOUVEMENT POPULAIRE: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK PERSONALISE, garantie émeute et mouvements populaires : indemnisation des dommages causés au véhicule par des émeutes, des manifestations ou des actes de vandalisme collectifs.",
            "VOL RADIO CASSETTE: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK PERSONALISE, garantie vol autoradio : elle rembourse la valeur du système audio (radio, lecteur) volé ou détérioré suite à une effraction du véhicule.",
            "ASSISTANCE +: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK PERSONALISE, assistance renforcée : elle élargit les prestations d’assistance classiques en prévoyant des services supplémentaires (dépannage à domicile, véhicule de remplacement, logement provisoire).",
            "CAR GLASS: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK PERSONALISE, garantie Car Glass : prise en charge illimitée du remplacement ou de la réparation des vitrages du véhicule, sans incidence sur le bonus.",
            "ACCIDENT CARE: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK PERSONALISE, garantie Accident Care : elle couvre les blessures du conducteur et des passagers (frais médicaux, invalidité, décès) à la suite d’un accident de la circulation.",
            "ASSISTANCE GOLD: Dans le cadre du produit OMNICANAL AUTOMOBILE PACK PERSONALISE, assistance Gold : offre haut de gamme avec dépannage rapide, véhicule de remplacement, prise en charge des frais d’hébergement et assistance aux personnes partout en Europe.",
            "SALIM ASSISTANCE AUTOMOBILE (S2A): Dans le cadre du produit OMNICANAL AUTOMOBILE PACK PERSONALISE, salim Assistance Automobile (S2A) : service d’assistance automobile incluant le dépannage, le remorquage et le rapatriement des passagers pour les souscripteurs du produit."
        ],
        "produit: PACK BASIC": [
            "RC - RTI: Dans le cadre du produit PACK BASIC, responsabilité civile automobile : garantie obligatoire couvrant les dommages corporels et matériels causés aux tiers lors d’un accident impliquant le véhicule assuré.",
            "DEFENSE ET RECOURS: Dans le cadre du produit PACK BASIC, garantie défense et recours : elle prend en charge les frais de procédure et d’assistance pour défendre l’assuré ou exercer un recours contre un responsable après un sinistre.",
            "INCENDIE: Dans le cadre du produit PACK BASIC, garantie incendie : elle indemnise les dommages causés par le feu, la foudre, l’explosion ou la chute de la foudre aux bâtiments et contenus assurés.",
            "VOL : Dans le cadre du produit PACK BASIC, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier.",
            "DOMMAGES AU VEHICULE: Dans le cadre du produit PACK BASIC, garantie dommages au véhicule : elle couvre les réparations du véhicule assuré à la suite d’un accident responsable ou non.",
            "DOMMAGES ET COLLISION: Dans le cadre du produit PACK BASIC, garantie dommages et collision : elle indemnise les dommages causés par une collision avec un autre véhicule ou un obstacle identifié.",
            "BRIS DE GLACES: Dans le cadre du produit PACK BASIC, garantie bris de glaces : elle couvre la réparation ou le remplacement des vitres, vitrines, miroirs ou surfaces en verre endommagés.",
            "P.T.A: Dans le cadre du produit PACK BASIC, garantie perte totale accidentelle (PTA) : elle prévoit l’indemnisation de la valeur du véhicule en cas de destruction totale consécutive à un accident couvert.",
            "ASSISTANCE + et CAR GLASS: Dans le cadre du produit PACK BASIC, formule combinée Assistance+ et Car Glass : elle inclut l’assistance renforcée et la prise en charge des réparations de vitrages du véhicule.",
            "INDIVIDUELLE ACCIDENT: Dans le cadre du produit PACK BASIC, garantie individuelle accident : elle verse un capital ou une rente en cas de décès ou d’invalidité d’une personne assurée lors d’un accident survenu dans les locaux.",
            "CHOC DE VEHICULES TERRESTRES IDENTIFIES: Dans le cadre du produit PACK BASIC, indemnisation des dommages causés aux biens assurés par la collision d’un véhicule terrestre identifié.",
            "ASSISTANCE ACCIDENT AUTOMOBILE (3A): Dans le cadre du produit PACK BASIC, garantie assistance accident automobile (3A) : en cas d’accident, l’assureur organise le dépannage, le remorquage et éventuellement le rapatriement des occupants.",
            "CATASTROPHE NATURELLE: Dans le cadre du produit PACK BASIC, garantie catastrophes naturelles : indemnisation des dommages causés au véhicule par un événement naturel reconnu (inondation, tempête, tremblement de terre…).",
            "EMEUTE ET MOUVEMENT POPULAIRE: Dans le cadre du produit PACK BASIC, garantie émeute et mouvements populaires : indemnisation des dommages causés au véhicule par des émeutes, des manifestations ou des actes de vandalisme collectifs.",
            "VOL RADIO CASSETTE: Dans le cadre du produit PACK BASIC, garantie vol autoradio : elle rembourse la valeur du système audio (radio, lecteur) volé ou détérioré suite à une effraction du véhicule.",
            "ASSISTANCE +: Dans le cadre du produit PACK BASIC, assistance renforcée : elle élargit les prestations d’assistance classiques en prévoyant des services supplémentaires (dépannage à domicile, véhicule de remplacement, logement provisoire).",
            "CAR GLASS: Dans le cadre du produit PACK BASIC, garantie Car Glass : prise en charge illimitée du remplacement ou de la réparation des vitrages du véhicule, sans incidence sur le bonus.",
            "ACCIDENT CARE: Dans le cadre du produit PACK BASIC, garantie Accident Care : elle couvre les blessures du conducteur et des passagers (frais médicaux, invalidité, décès) à la suite d’un accident de la circulation.",
            "ASSISTANCE GOLD: Dans le cadre du produit PACK BASIC, assistance Gold : offre haut de gamme avec dépannage rapide, véhicule de remplacement, prise en charge des frais d’hébergement et assistance aux personnes partout en Europe.",
            "SALIM ASSISTANCE AUTOMOBILE (S2A): Dans le cadre du produit PACK BASIC, salim Assistance Automobile (S2A) : service d’assistance automobile incluant le dépannage, le remorquage et le rapatriement des passagers pour les souscripteurs du produit."
        ],
        "produit: PACK BASIC+": [
            "RC - RTI: Dans le cadre du produit PACK BASIC+, responsabilité civile automobile : garantie obligatoire couvrant les dommages corporels et matériels causés aux tiers lors d’un accident impliquant le véhicule assuré.",
            "DEFENSE ET RECOURS: Dans le cadre du produit PACK BASIC+, garantie défense et recours : elle prend en charge les frais de procédure et d’assistance pour défendre l’assuré ou exercer un recours contre un responsable après un sinistre.",
            "INCENDIE: Dans le cadre du produit PACK BASIC+, garantie incendie : elle indemnise les dommages causés par le feu, la foudre, l’explosion ou la chute de la foudre aux bâtiments et contenus assurés.",
            "VOL : Dans le cadre du produit PACK BASIC+, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier.",
            "DOMMAGES AU VEHICULE: Dans le cadre du produit PACK BASIC+, garantie dommages au véhicule : elle couvre les réparations du véhicule assuré à la suite d’un accident responsable ou non.",
            "DOMMAGES ET COLLISION: Dans le cadre du produit PACK BASIC+, garantie dommages et collision : elle indemnise les dommages causés par une collision avec un autre véhicule ou un obstacle identifié.",
            "BRIS DE GLACES: Dans le cadre du produit PACK BASIC+, garantie bris de glaces : elle couvre la réparation ou le remplacement des vitres, vitrines, miroirs ou surfaces en verre endommagés.",
            "P.T.A: Dans le cadre du produit PACK BASIC+, garantie perte totale accidentelle (PTA) : elle prévoit l’indemnisation de la valeur du véhicule en cas de destruction totale consécutive à un accident couvert.",
            "ASSISTANCE + et CAR GLASS: Dans le cadre du produit PACK BASIC+, formule combinée Assistance+ et Car Glass : elle inclut l’assistance renforcée et la prise en charge des réparations de vitrages du véhicule.",
            "INDIVIDUELLE ACCIDENT: Dans le cadre du produit PACK BASIC+, garantie individuelle accident : elle verse un capital ou une rente en cas de décès ou d’invalidité d’une personne assurée lors d’un accident survenu dans les locaux.",
            "CHOC DE VEHICULES TERRESTRES IDENTIFIES: Dans le cadre du produit PACK BASIC+, indemnisation des dommages causés aux biens assurés par la collision d’un véhicule terrestre identifié.",
            "ASSISTANCE ACCIDENT AUTOMOBILE (3A): Dans le cadre du produit PACK BASIC+, garantie assistance accident automobile (3A) : en cas d’accident, l’assureur organise le dépannage, le remorquage et éventuellement le rapatriement des occupants.",
            "CATASTROPHE NATURELLE: Dans le cadre du produit PACK BASIC+, garantie catastrophes naturelles : indemnisation des dommages causés au véhicule par un événement naturel reconnu (inondation, tempête, tremblement de terre…).",
            "EMEUTE ET MOUVEMENT POPULAIRE: Dans le cadre du produit PACK BASIC+, garantie émeute et mouvements populaires : indemnisation des dommages causés au véhicule par des émeutes, des manifestations ou des actes de vandalisme collectifs.",
            "VOL RADIO CASSETTE: Dans le cadre du produit PACK BASIC+, garantie vol autoradio : elle rembourse la valeur du système audio (radio, lecteur) volé ou détérioré suite à une effraction du véhicule.",
            "ASSISTANCE +: Dans le cadre du produit PACK BASIC+, assistance renforcée : elle élargit les prestations d’assistance classiques en prévoyant des services supplémentaires (dépannage à domicile, véhicule de remplacement, logement provisoire).",
            "CAR GLASS: Dans le cadre du produit PACK BASIC+, garantie Car Glass : prise en charge illimitée du remplacement ou de la réparation des vitrages du véhicule, sans incidence sur le bonus.",
            "ACCIDENT CARE: Dans le cadre du produit PACK BASIC+, garantie Accident Care : elle couvre les blessures du conducteur et des passagers (frais médicaux, invalidité, décès) à la suite d’un accident de la circulation.",
            "ASSISTANCE GOLD: Dans le cadre du produit PACK BASIC+, assistance Gold : offre haut de gamme avec dépannage rapide, véhicule de remplacement, prise en charge des frais d’hébergement et assistance aux personnes partout en Europe.",
            "SALIM ASSISTANCE AUTOMOBILE (S2A): Dans le cadre du produit PACK BASIC+, salim Assistance Automobile (S2A) : service d’assistance automobile incluant le dépannage, le remorquage et le rapatriement des passagers pour les souscripteurs du produit."
        ],
        "produit: PACK DOMMAGE ET COLLISION": [
            "RC - RTI: Dans le cadre du produit PACK DOMMAGE ET COLLISION, responsabilité civile automobile : garantie obligatoire couvrant les dommages corporels et matériels causés aux tiers lors d’un accident impliquant le véhicule assuré.",
            "DEFENSE ET RECOURS: Dans le cadre du produit PACK DOMMAGE ET COLLISION, garantie défense et recours : elle prend en charge les frais de procédure et d’assistance pour défendre l’assuré ou exercer un recours contre un responsable après un sinistre.",
            "INCENDIE: Dans le cadre du produit PACK DOMMAGE ET COLLISION, garantie incendie : elle indemnise les dommages causés par le feu, la foudre, l’explosion ou la chute de la foudre aux bâtiments et contenus assurés.",
            "VOL : Dans le cadre du produit PACK DOMMAGE ET COLLISION, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier.",
            "DOMMAGES AU VEHICULE: Dans le cadre du produit PACK DOMMAGE ET COLLISION, garantie dommages au véhicule : elle couvre les réparations du véhicule assuré à la suite d’un accident responsable ou non.",
            "DOMMAGES ET COLLISION: Dans le cadre du produit PACK DOMMAGE ET COLLISION, garantie dommages et collision : elle indemnise les dommages causés par une collision avec un autre véhicule ou un obstacle identifié.",
            "BRIS DE GLACES: Dans le cadre du produit PACK DOMMAGE ET COLLISION, garantie bris de glaces : elle couvre la réparation ou le remplacement des vitres, vitrines, miroirs ou surfaces en verre endommagés.",
            "P.T.A: Dans le cadre du produit PACK DOMMAGE ET COLLISION, garantie perte totale accidentelle (PTA) : elle prévoit l’indemnisation de la valeur du véhicule en cas de destruction totale consécutive à un accident couvert.",
            "ASSISTANCE + et CAR GLASS: Dans le cadre du produit PACK DOMMAGE ET COLLISION, formule combinée Assistance+ et Car Glass : elle inclut l’assistance renforcée et la prise en charge des réparations de vitrages du véhicule.",
            "INDIVIDUELLE ACCIDENT: Dans le cadre du produit PACK DOMMAGE ET COLLISION, garantie individuelle accident : elle verse un capital ou une rente en cas de décès ou d’invalidité d’une personne assurée lors d’un accident survenu dans les locaux.",
            "CHOC DE VEHICULES TERRESTRES IDENTIFIES: Dans le cadre du produit PACK DOMMAGE ET COLLISION, indemnisation des dommages causés aux biens assurés par la collision d’un véhicule terrestre identifié.",
            "ASSISTANCE ACCIDENT AUTOMOBILE (3A): Dans le cadre du produit PACK DOMMAGE ET COLLISION, garantie assistance accident automobile (3A) : en cas d’accident, l’assureur organise le dépannage, le remorquage et éventuellement le rapatriement des occupants.",
            "CATASTROPHE NATURELLE: Dans le cadre du produit PACK DOMMAGE ET COLLISION, garantie catastrophes naturelles : indemnisation des dommages causés au véhicule par un événement naturel reconnu (inondation, tempête, tremblement de terre…).",
            "EMEUTE ET MOUVEMENT POPULAIRE: Dans le cadre du produit PACK DOMMAGE ET COLLISION, garantie émeute et mouvements populaires : indemnisation des dommages causés au véhicule par des émeutes, des manifestations ou des actes de vandalisme collectifs.",
            "VOL RADIO CASSETTE: Dans le cadre du produit PACK DOMMAGE ET COLLISION, garantie vol autoradio : elle rembourse la valeur du système audio (radio, lecteur) volé ou détérioré suite à une effraction du véhicule.",
            "ASSISTANCE +: Dans le cadre du produit PACK DOMMAGE ET COLLISION, assistance renforcée : elle élargit les prestations d’assistance classiques en prévoyant des services supplémentaires (dépannage à domicile, véhicule de remplacement, logement provisoire).",
            "CAR GLASS: Dans le cadre du produit PACK DOMMAGE ET COLLISION, garantie Car Glass : prise en charge illimitée du remplacement ou de la réparation des vitrages du véhicule, sans incidence sur le bonus.",
            "ACCIDENT CARE: Dans le cadre du produit PACK DOMMAGE ET COLLISION, garantie Accident Care : elle couvre les blessures du conducteur et des passagers (frais médicaux, invalidité, décès) à la suite d’un accident de la circulation.",
            "ASSISTANCE GOLD: Dans le cadre du produit PACK DOMMAGE ET COLLISION, assistance Gold : offre haut de gamme avec dépannage rapide, véhicule de remplacement, prise en charge des frais d’hébergement et assistance aux personnes partout en Europe.",
            "SALIM ASSISTANCE AUTOMOBILE (S2A): Dans le cadre du produit PACK DOMMAGE ET COLLISION, salim Assistance Automobile (S2A) : service d’assistance automobile incluant le dépannage, le remorquage et le rapatriement des passagers pour les souscripteurs du produit."
        ],
        "produit: PACK TOUS RISQUES SANS FRANCHISE ": [
            "RC - RTI: Dans le cadre du produit PACK TOUS RISQUES SANS FRANCHISE, responsabilité civile automobile : garantie obligatoire couvrant les dommages corporels et matériels causés aux tiers lors d’un accident impliquant le véhicule assuré.",
            "DEFENSE ET RECOURS: Dans le cadre du produit PACK TOUS RISQUES SANS FRANCHISE, garantie défense et recours : elle prend en charge les frais de procédure et d’assistance pour défendre l’assuré ou exercer un recours contre un responsable après un sinistre.",
            "INCENDIE: Dans le cadre du produit PACK TOUS RISQUES SANS FRANCHISE, garantie incendie : elle indemnise les dommages causés par le feu, la foudre, l’explosion ou la chute de la foudre aux bâtiments et contenus assurés.",
            "VOL : Dans le cadre du produit PACK TOUS RISQUES SANS FRANCHISE, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier.",
            "DOMMAGES AU VEHICULE: Dans le cadre du produit PACK TOUS RISQUES SANS FRANCHISE, garantie dommages au véhicule : elle couvre les réparations du véhicule assuré à la suite d’un accident responsable ou non.",
            "DOMMAGES ET COLLISION: Dans le cadre du produit PACK TOUS RISQUES SANS FRANCHISE, garantie dommages et collision : elle indemnise les dommages causés par une collision avec un autre véhicule ou un obstacle identifié.",
            "BRIS DE GLACES: Dans le cadre du produit PACK TOUS RISQUES SANS FRANCHISE, garantie bris de glaces : elle couvre la réparation ou le remplacement des vitres, vitrines, miroirs ou surfaces en verre endommagés.",
            "P.T.A: Dans le cadre du produit PACK TOUS RISQUES SANS FRANCHISE, garantie perte totale accidentelle (PTA) : elle prévoit l’indemnisation de la valeur du véhicule en cas de destruction totale consécutive à un accident couvert.",
            "ASSISTANCE + et CAR GLASS: Dans le cadre du produit PACK TOUS RISQUES SANS FRANCHISE, formule combinée Assistance+ et Car Glass : elle inclut l’assistance renforcée et la prise en charge des réparations de vitrages du véhicule.",
            "INDIVIDUELLE ACCIDENT: Dans le cadre du produit PACK TOUS RISQUES SANS FRANCHISE, garantie individuelle accident : elle verse un capital ou une rente en cas de décès ou d’invalidité d’a personne assurée lors d’un accident survenu dans les locaux.",
            "CHOC DE VEHICULES TERRESTRES IDENTIFIES: Dans le cadre du produit PACK TOUS RISQUES SANS FRANCHISE, indemnisation des dommages causés aux biens assurés par la collision d’un véhicule terrestre identifié.",
            "ASSISTANCE ACCIDENT AUTOMOBILE (3A): Dans le cadre du produit PACK TOUS RISQUES SANS FRANCHISE, garantie assistance accident automobile (3A) : en cas d’accident, l’assureur organise le dépannage, le remorquage et éventuellement le rapatriement des occupants.",
            "CATASTROPHE NATURELLE: Dans le cadre du produit PACK TOUS RISQUES SANS FRANCHISE, garantie catastrophes naturelles : indemnisation des dommages causés au véhicule par un événement naturel reconnu (inondation, tempête, tremblement de terre…).",
            "EMEUTE ET MOUVEMENT POPULAIRE: Dans le cadre du produit PACK TOUS RISQUES SANS FRANCHISE, garantie émeute et mouvements populaires : indemnisation des dommages causés au véhicule par des émeutes, des manifestations ou des actes de vandalisme collectifs.",
            "VOL RADIO CASSETTE: Dans le cadre du produit PACK TOUS RISQUES SANS FRANCHISE, garantie vol autoradio : elle rembourse la valeur du système audio (radio, lecteur) volé ou détérioré suite à une effraction du véhicule.",
            "ASSISTANCE +: Dans le cadre du produit PACK TOUS RISQUES SANS FRANCHISE, assistance renforcée : elle élargit les prestations d’assistance classiques en prévoyant des services supplémentaires (dépannage à domicile, véhicule de remplacement, logement provisoire).",
            "CAR GLASS: Dans le cadre du produit PACK TOUS RISQUES SANS FRANCHISE, garantie Car Glass : prise en charge illimitée du remplacement ou de la réparation des vitrages du véhicule, sans incidence sur le bonus.",
            "ACCIDENT CARE: Dans le cadre du produit PACK TOUS RISQUES SANS FRANCHISE, garantie Accident Care : elle couvre les blessures du conducteur et des passagers (frais médicaux, invalidité, décès) à la suite d’un accident de la circulation.",
            "ASSISTANCE GOLD: Dans le cadre du produit PACK TOUS RISQUES SANS FRANCHISE, assistance Gold : offre haut de gamme avec dépannage rapide, véhicule de remplacement, prise en charge des frais d’hébergement et assistance aux personnes partout en Europe.",
            "SALIM ASSISTANCE AUTOMOBILE (S2A): Dans le cadre du produit PACK TOUS RISQUES SANS FRANCHISE, salim Assistance Automobile (S2A) : service d’assistance automobile incluant le dépannage, le remorquage et le rapatriement des passagers pour les souscripteurs du produit."
        ],
        "produit: PACK TOUS RISQUES AVEC FRANCHISE ": [
            "RC - RTI: Dans le cadre du produit PACK TOUS RISQUES AVEC FRANCHISE, responsabilité civile automobile : garantie obligatoire couvrant les dommages corporels et matériels causés aux tiers lors d’un accident impliquant le véhicule assuré.",
            "DEFENSE ET RECOURS: Dans le cadre du produit PACK TOUS RISQUES AVEC FRANCHISE, garantie défense et recours : elle prend en charge les frais de procédure et d’assistance pour défendre l’assuré ou exercer un recours contre un responsable après un sinistre.",
            "INCENDIE: Dans le cadre du produit PACK TOUS RISQUES AVEC FRANCHISE, garantie incendie : elle indemnise les dommages causés par le feu, la foudre, l’explosion ou la chute de la foudre aux bâtiments et contenus assurés.",
            "VOL : Dans le cadre du produit PACK TOUS RISQUES AVEC FRANCHISE, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier.",
            "DOMMAGES AU VEHICULE: Dans le cadre du produit PACK TOUS RISQUES AVEC FRANCHISE, garantie dommages au véhicule : elle couvre les réparations du véhicule assuré à la suite d’un accident responsable ou non.",
            "DOMMAGES ET COLLISION: Dans le cadre du produit PACK TOUS RISQUES AVEC FRANCHISE, garantie dommages et collision : elle indemnise les dommages causés par une collision avec un autre véhicule ou un obstacle identifié.",
            "BRIS DE GLACES: Dans le cadre du produit PACK TOUS RISQUES AVEC FRANCHISE, garantie bris de glaces : elle couvre la réparation ou le remplacement des vitres, vitrines, miroirs ou surfaces en verre endommagés.",
            "P.T.A: Dans le cadre du produit PACK TOUS RISQUES AVEC FRANCHISE, garantie perte totale accidentelle (PTA) : elle prévoit l’indemnisation de la valeur du véhicule en cas de destruction totale consécutive à un accident couvert.",
            "ASSISTANCE + et CAR GLASS: Dans le cadre du produit PACK TOUS RISQUES AVEC FRANCHISE, formule combinée Assistance+ et Car Glass : elle inclut l’assistance renforcée et la prise en charge des réparations de vitrages du véhicule.",
            "INDIVIDUELLE ACCIDENT: Dans le cadre du produit PACK TOUS RISQUES AVEC FRANCHISE, garantie individuelle accident : elle verse un capital ou une rente en cas de décès ou d’invalidité d’une personne assurée lors d’un accident survenu dans les locaux.",
            "CHOC DE VEHICULES TERRESTRES IDENTIFIES: Dans le cadre du produit PACK TOUS RISQUES AVEC FRANCHISE, indemnisation des dommages causés aux biens assurés par la collision d’un véhicule terrestre identifié.",
            "ASSISTANCE ACCIDENT AUTOMOBILE (3A): Dans le cadre du produit PACK TOUS RISQUES AVEC FRANCHISE, garantie assistance accident automobile (3A) : en cas d’accident, l’assureur organise le dépannage, le remorquage et éventuellement le rapatriement des occupants.",
            "CATASTROPHE NATURELLE: Dans le cadre du produit PACK TOUS RISQUES AVEC FRANCHISE, garantie catastrophes naturelles : indemnisation des dommages causés au véhicule par un événement naturel reconnu (inondation, tempête, tremblement de terre…).",
            "EMEUTE ET MOUVEMENT POPULAIRE: Dans le cadre du produit PACK TOUS RISQUES AVEC FRANCHISE, garantie émeute et mouvements populaires : indemnisation des dommages causés au véhicule par des émeutes, des manifestations ou des actes de vandalisme collectifs.",
            "VOL RADIO CASSETTE: Dans le cadre du produit PACK TOUS RISQUES AVEC FRANCHISE, garantie vol autoradio : elle rembourse la valeur du système audio (radio, lecteur) volé ou détérioré suite à une effraction du véhicule.",
            "ASSISTANCE +: Dans le cadre du produit PACK TOUS RISQUES AVEC FRANCHISE, assistance renforcée : elle élargit les prestations d’assistance classiques en prévoyant des services supplémentaires (dépannage, véhicule de remplacement).",
            "CAR GLASS: Dans le cadre du produit PACK TOUS RISQUES AVEC FRANCHISE, garantie Car Glass : prise en charge illimitée du remplacement ou de la réparation des vitrages du véhicule, sans incidence sur le bonus.",
            "ACCIDENT CARE: Dans le cadre du produit PACK TOUS RISQUES AVEC FRANCHISE, garantie Accident Care : elle couvre les blessures du conducteur et des passagers (frais médicaux, invalidité, décès) à la suite d’un accident de la circulation.",
            "ASSISTANCE GOLD: Dans le cadre du produit PACK TOUS RISQUES AVEC FRANCHISE, assistance Gold : offre haut de gamme avec dépannage rapide, véhicule de remplacement, prise en charge des frais d’hébergement et assistance aux personnes partout en Europe.",
            "SALIM ASSISTANCE AUTOMOBILE (S2A): Dans le cadre du produit PACK TOUS RISQUES AVEC FRANCHISE, salim Assistance Automobile (S2A) : service d’assistance automobile incluant le dépannage, le remorquage et le rapatriement des passagers pour les souscripteurs du produit."
        ],
        "produit: AUTOMOBILE ASSURANCE FRONTIERE TEMPORAIRE": [
            "RC - RTI: Dans le cadre du produit AUTOMOBILE ASSURANCE FRONTIERE TEMPORAIRE, responsabilité civile automobile : garantie obligatoire couvrant les dommages corporels et matériels causés aux tiers lors d’un accident impliquant le véhicule assuré.",
            "DEFENSE ET RECOURS: Dans le cadre du produit AUTOMOBILE ASSURANCE FRONTIERE TEMPORAIRE, garantie défense et recours : elle prend en charge les frais de procédure et d’assistance pour défendre l’assuré ou exercer un recours contre un responsable après un sinistre.",
            "INCENDIE: Dans le cadre du produit AUTOMOBILE ASSURANCE FRONTIERE TEMPORAIRE, garantie incendie : elle indemnise les dommages causés par le feu, la foudre, l’explosion ou la chute de la foudre aux bâtiments et contenus assurés.",
            "VOL : Dans le cadre du produit AUTOMOBILE ASSURANCE FRONTIERE TEMPORAIRE, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier.",
            "DOMMAGES AU VEHICULE: Dans le cadre du produit AUTOMOBILE ASSURANCE FRONTIERE TEMPORAIRE, garantie dommages au véhicule : elle couvre les réparations du véhicule assuré à la suite d’un accident responsable ou non.",
            "DOMMAGES ET COLLISION: Dans le cadre du produit AUTOMOBILE ASSURANCE FRONTIERE TEMPORAIRE, garantie dommages et collision : elle indemnise les dommages causés par une collision avec un autre véhicule ou un obstacle identifié.",
            "BRIS DE GLACES: Dans le cadre du produit AUTOMOBILE ASSURANCE FRONTIERE TEMPORAIRE, garantie bris de glaces : elle couvre la réparation ou le remplacement des vitres, vitrines, miroirs ou surfaces en verre endommagés.",
            "P.T.A: Dans le cadre du produit AUTOMOBILE ASSURANCE FRONTIERE TEMPORAIRE, garantie perte totale accidentelle (PTA) : elle prévoit l’indemnisation de la valeur du véhicule en cas de destruction totale consécutive à un accident couvert.",
            "ASSISTANCE + et CAR GLASS: Dans le cadre du produit AUTOMOBILE ASSURANCE FRONTIERE TEMPORAIRE, formule combinée Assistance+ et Car Glass : elle inclut l’assistance renforcée et la prise en charge des réparations de vitrages du véhicule.",
            "INDIVIDUELLE ACCIDENT: Dans le cadre du produit AUTOMOBILE ASSURANCE FRONTIERE TEMPORAIRE, garantie individuelle accident : elle verse un capital ou une rente en cas de décès ou d’invalidité d’une personne assurée lors d’un accident survenu dans les locaux.",
            "CHOC DE VEHICULES TERRESTRES IDENTIFIES: Dans le cadre du produit AUTOMOBILE ASSURANCE FRONTIERE TEMPORAIRE, indemnisation des dommages causés aux biens assurés par la collision d’un véhicule terrestre identifié.",
            "ASSISTANCE ACCIDENT AUTOMOBILE (3A): Dans le cadre du produit AUTOMOBILE ASSURANCE FRONTIERE TEMPORAIRE, garantie assistance accident automobile (3A) : en cas d’accident, l’assureur organise le dépannage, le remorquage et éventuellement le rapatriement des occupants.",
            "CATASTROPHE NATURELLE: Dans le cadre du produit AUTOMOBILE ASSURANCE FRONTIERE TEMPORAIRE, garantie catastrophes naturelles : indemnisation des dommages causés au véhicule par un événement naturel reconnu (inondation, tempête, tremblement de terre…).",
            "EMEUTE ET MOUVEMENT POPULAIRE: Dans le cadre du produit AUTOMOBILE ASSURANCE FRONTIERE TEMPORAIRE, garantie émeute et mouvements populaires : indemnisation des dommages causés au véhicule par des émeutes, des manifestations ou des actes de vandalisme collectifs.",
            "VOL RADIO CASSETTE: Dans le cadre du produit AUTOMOBILE ASSURANCE FRONTIERE TEMPORAIRE, garantie vol autoradio : elle rembourse la valeur du système audio (radio, lecteur) volé ou détérioré suite à une effraction du véhicule.",
            "ASSISTANCE +: Dans le cadre du produit AUTOMOBILE ASSURANCE FRONTIERE TEMPORAIRE, assistance renforcée : elle élargit les prestations d’assistance classiques en prévoyant des services supplémentaires (dépannage à domicile, véhicule de remplacement, logement provisoire).",
            "CAR GLASS: Dans le cadre du produit AUTOMOBILE ASSURANCE FRONTIERE TEMPORAIRE, garantie Car Glass : prise en charge illimitée du remplacement ou de la réparation des vitrages du véhicule, sans incidence sur le bonus.",
            "ACCIDENT CARE: Dans le cadre du produit AUTOMOBILE ASSURANCE FRONTIERE TEMPORAIRE, garantie Accident Care : elle couvre les blessures du conducteur et des passagers (frais médicaux, invalidité, décès) à la suite d’un accident de la circulation.",
            "ASSISTANCE GOLD: Dans le cadre du produit AUTOMOBILE ASSURANCE FRONTIERE TEMPORAIRE, assistance Gold : offre haut de gamme avec dépannage rapide, véhicule de remplacement, prise en charge des frais d’hébergement et assistance aux personnes partout en Europe.",
            "SALIM ASSISTANCE AUTOMOBILE (S2A): Dans le cadre du produit AUTOMOBILE ASSURANCE FRONTIERE TEMPORAIRE, salim Assistance Automobile (S2A) : service d’assistance automobile incluant le dépannage, le remorquage et le rapatriement des passagers pour les souscripteurs du produit."
        ]
    },
    "ENGINEERING": {
        "produit: TOUS RISQUES CHANTIER": [
            "HONORAIRE EXPERT: Dans le cadre du produit TOUS RISQUES CHANTIER, remboursement des honoraires de l’expert mandaté pour évaluer les dommages à la suite d’un sinistre.",
            "FRAIS DE DEBLAIS ET DE DEMOLITION: Dans le cadre du produit TOUS RISQUES CHANTIER, cette garantie couvre les risques spécifiques liés à 'FRAIS DE DEBLAIS ET DE DEMOLITION'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "GREVE, EMEUTE ET MOUVEMENTS POPULAIRES: Dans le cadre du produit TOUS RISQUES CHANTIER, cette garantie couvre les risques spécifiques liés à 'GREVE, EMEUTE ET MOUVEMENTS POPULAIRES'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "RESPONSABILITE CIVILE: Dans le cadre du produit TOUS RISQUES CHANTIER, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport.",
            "DOMMAGES A L OUVRAGE: Dans le cadre du produit TOUS RISQUES CHANTIER, cette garantie couvre les risques spécifiques liés à 'DOMMAGES A L OUVRAGE'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "FRAIS SUPPLEMENTAIRES: Dans le cadre du produit TOUS RISQUES CHANTIER, prise en charge des frais supplémentaires engagés pour continuer ou reprendre l’activité après un sinistre (location de locaux temporaires, heures supplémentaires).",
            "FRAIS AERIEN: Dans le cadre du produit TOUS RISQUES CHANTIER, cette garantie couvre les risques spécifiques liés à 'FRAIS AERIEN'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "MAINTENANCE VISITES: Dans le cadre du produit TOUS RISQUES CHANTIER, cette garantie couvre les risques spécifiques liés à 'MAINTENANCE VISITES'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "MAINTENANCE ETENDUE: Dans le cadre du produit TOUS RISQUES CHANTIER, cette garantie couvre les risques spécifiques liés à 'MAINTENANCE ETENDUE'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "BIENS EXISTANTS: Dans le cadre du produit TOUS RISQUES CHANTIER, cette garantie couvre les risques spécifiques liés à 'BIENS EXISTANTS'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "ENGINS DE CHANTIER: Dans le cadre du produit TOUS RISQUES CHANTIER, cette garantie couvre les risques spécifiques liés à 'ENGINS DE CHANTIER'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "EQUIPEMENTS DE CHANTIER: Dans le cadre du produit TOUS RISQUES CHANTIER, cette garantie couvre les risques spécifiques liés à 'EQUIPEMENTS DE CHANTIER'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "ERREUR DE CONCEPTION - DE CALCULS - DE PLANS: Dans le cadre du produit TOUS RISQUES CHANTIER, cette garantie couvre les risques spécifiques liés à 'ERREUR DE CONCEPTION - DE CALCULS - DE PLANS'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "RC CROISEE: Dans le cadre du produit TOUS RISQUES CHANTIER, responsabilité civile croisée : chaque partie co‑assurée est considérée comme tierce l’une vis‑à‑vis de l’autre, ce qui permet l’indemnisation croisée des dommages.",
            "INSTALLATION PROVISOIRE: Dans le cadre du produit TOUS RISQUES CHANTIER, cette garantie couvre les risques spécifiques liés à 'INSTALLATION PROVISOIRE'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "PERTE EXPLOITATION ANTICIPEE: Dans le cadre du produit TOUS RISQUES CHANTIER, cette garantie couvre les risques spécifiques liés à 'PERTE EXPLOITATION ANTICIPEE'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "BRIS DE MACHINES: Dans le cadre du produit TOUS RISQUES CHANTIER, cette garantie couvre les risques spécifiques liés à 'BRIS DE MACHINES'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "FRAIS DE LUTTE CONTRE L INCENDIE: Dans le cadre du produit TOUS RISQUES CHANTIER, prise en charge des frais engagés pour lutter contre un incendie (extinction, pompiers) et éviter l’aggravation des dommages.",
            "CATASTROPHES NATURELS (TREMBLEMENT DE TERRE, INONDATION)): Dans le cadre du produit TOUS RISQUES CHANTIER, indemnisation des dommages causés aux biens ou aux travaux par un tremblement de terre, une inondation ou un glissement de terrain reconnu comme catastrophe naturelle.",
            "TRANSPORT A L INTERIEUR DU PAYS: Dans le cadre du produit TOUS RISQUES CHANTIER, garantie transport intérieur : elle couvre les risques de dommages ou de perte subis par les marchandises lors de leur transport à l’intérieur du pays.",
            "INCENDIE, FOUDRE, EXPLOSION: Dans le cadre du produit TOUS RISQUES CHANTIER, garantie incendie, foudre et explosion : indemnisation des dommages matériels causés par un incendie, la foudre ou une explosion aux travaux ou équipements assurés.",
            "TERRORISME ET ACTES DE SABOTAGE: Dans le cadre du produit TOUS RISQUES CHANTIER, garantie terrorisme et sabotage : elle couvre les dommages causés par des actes terroristes ou des actes de sabotage aux biens ou travaux assurés.",
            "RC PENDANT LA MAINTENANCE: Dans le cadre du produit TOUS RISQUES CHANTIER, responsabilité civile pendant la maintenance : elle couvre les dommages causés à des tiers par les interventions de maintenance après la livraison de l’ouvrage ou de l’équipement.",
            "FRAIS DE RECONSTITUTION DE DESSIN ET DE PLANS: Dans le cadre du produit TOUS RISQUES CHANTIER, prise en charge des coûts de reconstitution de dessins et de plans techniques détruits ou endommagés à la suite d’un sinistre.",
            "PERILS IMMINENTS \\\"SUE ET LABOUR\\\": Dans le cadre du produit TOUS RISQUES CHANTIER, garantie périls imminents (sue and labour) : prise en charge des dépenses engagées pour préserver les biens assurés et éviter l’aggravation d’un dommage imminent.",
            "MAINTENANCE CONSTRUCTEUR: Dans le cadre du produit TOUS RISQUES CHANTIER, cette garantie couvre les risques spécifiques liés à 'MAINTENANCE CONSTRUCTEUR'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "CONDUITES, CABLES ET CANALISATION SOUTERRAINES: Dans le cadre du produit TOUS RISQUES CHANTIER, garantie conduites, câbles et canalisations souterraines : elle indemnise les dommages causés à ces installations lors des travaux ou par un sinistre.",
            "DEFAUT DE FABRICATION ( MONTAGE / ESSAIS ): Dans le cadre du produit TOUS RISQUES CHANTIER, garantie défaut de fabrication (montage/essais) : couverture des dommages dus à un défaut de fabrication ou de montage constaté lors des essais de mise en service.",
            "DOMMAGES AUX BIENS EXISTANTS ET/OU AVOISINANT: Dans le cadre du produit TOUS RISQUES CHANTIER, indemnisation des dommages causés aux biens existants et/ou avoisinants du chantier (bâtiments voisins, installations) par les travaux ou un sinistre.",
            "BIENS ENTREPOSES SUR SITE: Dans le cadre du produit TOUS RISQUES CHANTIER, garantie biens entreposés sur site : elle couvre les matériaux et équipements stockés sur le chantier contre le vol, l’incendie et d’autres risques.",
            "BIENS ENTREPOSES HORS DE CHANTIER: Dans le cadre du produit TOUS RISQUES CHANTIER, garantie biens entreposés hors du chantier : couverture des matériaux et équipements stockés en entrepôt ou chez un fournisseur contre les risques de vol, d’incendie ou de détérioration."
        ],
        "produit: TOUS RISQUES MONTAGE": [
            "DOMMAGES AUX MATERIELS: Dans le cadre du produit TOUS RISQUES MONTAGE, garantie dommages aux matériels : elle couvre les dommages accidentels subis par les matériels de chantier (câbles, pompes, compresseurs).",
            "RC CROISEE: Dans le cadre du produit TOUS RISQUES MONTAGE, responsabilité civile croisée : chaque partie co‑assurée est considérée comme tierce l’une vis‑à‑vis de l’autre, ce qui permet l’indemnisation croisée des dommages."
        ],
        "produit: RESPONSABILITE DECENNALE": [
            "DOMMAGES AUX MATERIELS: Dans le cadre du produit RESPONSABILITE DECENNALE, garantie dommages aux matériels : elle couvre les dommages accidentels subis par les matériels de chantier (câbles, pompes, compresseurs).",
            "FRAIS DE DEBLAIS ET DE DEMOLITION: Dans le cadre du produit RESPONSABILITE DECENNALE, cette garantie couvre les risques spécifiques liés à 'FRAIS DE DEBLAIS ET DE DEMOLITION'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "ETANCHEITE: Dans le cadre du produit RESPONSABILITE DECENNALE, garantie étanchéité : indemnisation des dommages résultant d’un défaut d’étanchéité des toitures, terrasses ou ouvrages assurés.",
            "TRAVAUX NEUF: Dans le cadre du produit RESPONSABILITE DECENNALE, garantie travaux neufs : elle couvre les dommages survenant pendant les travaux de construction de bâtiments ou d’ouvrages neufs.",
            "PROCEDES NOUVEAUX: Dans le cadre du produit RESPONSABILITE DECENNALE, garantie procédés nouveaux : elle couvre les risques liés à l’utilisation de techniques ou procédés de construction innovants non encore éprouvés.",
            "BIENS EXISTANTS: Dans le cadre du produit RESPONSABILITE DECENNALE, cette garantie couvre les risques spécifiques liés à 'BIENS EXISTANTS'. Veuillez consulter le contrat pour connaître le détail des prestations."
        ],
        "produit: BRIS DE MACHINES": [
            "INCENDIE: Dans le cadre du produit BRIS DE MACHINES, garantie incendie : elle indemnise les dommages causés par le feu, la foudre, l’explosion ou la chute de la foudre aux bâtiments et contenus assurés.",
            "VOL : Dans le cadre du produit BRIS DE MACHINES, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier.",
            "PERTE INDIRECTE: Dans le cadre du produit BRIS DE MACHINES, garantie perte indirecte : elle couvre les dépenses supplémentaires et pertes financières consécutives à un sinistre (retard de chantier, loyers…).",
            "HONORAIRE EXPERT: Dans le cadre du produit BRIS DE MACHINES, remboursement des honoraires de l’expert mandaté pour évaluer les dommages à la suite d’un sinistre.",
            "DOMMAGES AUX MATERIELS: Dans le cadre du produit BRIS DE MACHINES, garantie dommages aux matériels : elle couvre les dommages accidentels subis par les matériels de chantier (câbles, pompes, compresseurs).",
            "GREVE, EMEUTE ET MOUVEMENTS POPULAIRES: Dans le cadre du produit BRIS DE MACHINES, cette garantie couvre les risques spécifiques liés à 'GREVE, EMEUTE ET MOUVEMENTS POPULAIRES'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "FRAIS SUPPLEMENTAIRES: Dans le cadre du produit BRIS DE MACHINES, prise en charge des frais supplémentaires engagés pour continuer ou reprendre l’activité après un sinistre (location de locaux temporaires, heures supplémentaires).",
            "FRAIS AERIEN: Dans le cadre du produit BRIS DE MACHINES, cette garantie couvre les risques spécifiques liés à 'FRAIS AERIEN'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "BIENS EXISTANTS: Dans le cadre du produit BRIS DE MACHINES, cette garantie couvre les risques spécifiques liés à 'BIENS EXISTANTS'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "INONDATIONS: Dans le cadre du produit BRIS DE MACHINES, garantie inondations : elle indemnise les dommages causés par une inondation, une remontée de nappe phréatique ou un ruissellement.",
            "SOCLES ET FONDATIONS: Dans le cadre du produit BRIS DE MACHINES, garantie socles et fondations : elle couvre les dommages causés aux fondations, aux socles et aux supports des machines et équipements en cas de sinistre.",
            "BONDE TRANSPORTEUSE: Dans le cadre du produit BRIS DE MACHINES, garantie bandes transporteuses : indemnisation des dommages subis par les bandes transporteuses utilisées dans les installations industrielles (usure prématurée, rupture accidentelle).",
            "PERTES EXPLOITATION APRES BRIS DE MACHINES: Dans le cadre du produit BRIS DE MACHINES, garantie pertes d’exploitation après bris de machines : indemnisation de la perte de chiffre d’affaires résultant de l’arrêt de l’activité à la suite d’un bris de machine couvert.",
            "DETERIORATION MARCHANDISES APRES BRIS DE MACHINES: Dans le cadre du produit BRIS DE MACHINES, indemnisation des marchandises détériorées à la suite d’un bris de machine (ex. compresseur) dans les installations frigorifiques.",
            "INCENDIE, FOUDRE, EXPLOSION: Dans le cadre du produit BRIS DE MACHINES, garantie incendie, foudre et explosion : indemnisation des dommages matériels causés par un incendie, la foudre ou une explosion aux travaux ou équipements assurés.",
            "CATASTROPHES NATURELS ( VENT, TREMBLEMENT DE TERRE): Dans le cadre du produit BRIS DE MACHINES, garantie catastrophes naturelles (vent, tremblement de terre) : elle indemnise les dommages causés par le vent violent ou un séisme reconnu comme catastrophe naturelle.",
            "TRANSPORT ENTRE SITE: Dans le cadre du produit BRIS DE MACHINES, cette garantie couvre les risques spécifiques liés à 'TRANSPORT ENTRE SITE'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "DOMMAGES RELEVANT DE LA GARANTIE DU FOURNISSEUR, DU CONSTRUCTEUR: Dans le cadre du produit BRIS DE MACHINES, garantie dommages relevant de la garantie du fournisseur ou du constructeur : elle prévoit l’indemnisation lorsque les dommages ne sont pas pris en charge par les garanties contractuelles du fabricant."
        ],
        "produit: ENGINS DE CHANTIERS": [
            "HONORAIRE EXPERT: Dans le cadre du produit ENGINS DE CHANTIERS, remboursement des honoraires de l’expert mandaté pour évaluer les dommages à la suite d’un sinistre.",
            "DOMMAGES AUX MATERIELS: Dans le cadre du produit ENGINS DE CHANTIERS, garantie dommages aux matériels : elle couvre les dommages accidentels subis par les matériels de chantier (câbles, pompes, compresseurs).",
            "GREVE, EMEUTE ET MOUVEMENTS POPULAIRES: Dans le cadre du produit ENGINS DE CHANTIERS, cette garantie couvre les risques spécifiques liés à 'GREVE, EMEUTE ET MOUVEMENTS POPULAIRES'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "FRAIS SUPPLEMENTAIRES: Dans le cadre du produit ENGINS DE CHANTIERS, prise en charge des frais supplémentaires engagés pour continuer ou reprendre l’activité après un sinistre (location de locaux temporaires, heures supplémentaires).",
            "FRAIS AERIEN: Dans le cadre du produit ENGINS DE CHANTIERS, cette garantie couvre les risques spécifiques liés à 'FRAIS AERIEN'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "TRANSPORT ENTRE SITE: Dans le cadre du produit ENGINS DE CHANTIERS, cette garantie couvre les risques spécifiques liés à 'TRANSPORT ENTRE SITE'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "DOMMAGES RELEVANT DE LA GARANTIE DU FOURNISSEUR, DU CONSTRUCTEUR: Dans le cadre du produit ENGINS DE CHANTIERS, garantie dommages relevant de la garantie du fournisseur ou du constructeur : elle prévoit l’indemnisation lorsque les dommages ne sont pas pris en charge par les garanties contractuelles du fabricant.",
            "DOMMAGES AUX BANDES TRANSPORTEUSES: Dans le cadre du produit ENGINS DE CHANTIERS, indemnisation des dommages subis par les bandes transporteuses (déchirure, incendie, bris) utilisées sur le site industriel.",
            "BRIS INTERNE: Dans le cadre du produit ENGINS DE CHANTIERS, garantie bris interne : elle couvre les dommages internes (rupture d’axe, court‑circuit, surtension) survenus à l’intérieur d’une machine assurée.",
            "CATASTROPHES NATURELS (OURAGON, TREMBLEMENT DE TERRE, INONDATION): Dans le cadre du produit ENGINS DE CHANTIERS, garantie catastrophes naturelles (ouragan, tremblement de terre, inondation) : elle couvre les dommages causés par ces événements exceptionnels lorsque l’état de catastrophe naturelle est déclaré."
        ],
        "produit: MULTIRISQUES INFORMATIQUES": [
            "INDEMNITE JOURNALIERE: Dans le cadre du produit MULTIRISQUES INFORMATIQUES, garantie indemnité journalière : versement d’une indemnité journalière compensant l’arrêt de production ou l’indisponibilité d’un équipement essentiel après un sinistre.",
            "HONORAIRE EXPERT: Dans le cadre du produit MULTIRISQUES INFORMATIQUES, remboursement des honoraires de l’expert mandaté pour évaluer les dommages à la suite d’un sinistre.",
            "DOMMAGES AUX MATERIELS: Dans le cadre du produit MULTIRISQUES INFORMATIQUES, garantie dommages aux matériels : elle couvre les dommages accidentels subis par les matériels de chantier (câbles, pompes, compresseurs).",
            "GREVE, EMEUTE ET MOUVEMENTS POPULAIRES: Dans le cadre du produit MULTIRISQUES INFORMATIQUES, cette garantie couvre les risques spécifiques liés à 'GREVE, EMEUTE ET MOUVEMENTS POPULAIRES'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "FRAIS SUPPLEMENTAIRES: Dans le cadre du produit MULTIRISQUES INFORMATIQUES, prise en charge des frais supplémentaires engagés pour continuer ou reprendre l’activité après un sinistre (location de locaux temporaires, heures supplémentaires).",
            "FRAIS AERIEN: Dans le cadre du produit MULTIRISQUES INFORMATIQUES, cette garantie couvre les risques spécifiques liés à 'FRAIS AERIEN'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "PERTE ET RECONSTITUTIONS DES DONNEES: Dans le cadre du produit MULTIRISQUES INFORMATIQUES, garantie perte et reconstitution des données : prise en charge des frais pour récupérer ou reconstituer des données informatiques perdues à la suite d’un sinistre.",
            "TRANSPORT ENTRE SITE: Dans le cadre du produit MULTIRISQUES INFORMATIQUES, cette garantie couvre les risques spécifiques liés à 'TRANSPORT ENTRE SITE'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "DOMMAGES RELEVANT DE LA GARANTIE DU FOURNISSEUR, DU CONSTRUCTEUR: Dans le cadre du produit MULTIRISQUES INFORMATIQUES, garantie dommages relevant de la garantie du fournisseur ou du constructeur : elle prévoit l’indemnisation lorsque les dommages ne sont pas pris en charge par les garanties contractuelles du fabricant.",
            "MATERIEL MOBILE: Dans le cadre du produit MULTIRISQUES INFORMATIQUES, garantie matériel mobile : elle couvre les dommages accidentels, le vol ou la disparition des équipements mobiles utilisés sur différents sites (ordinateurs portables, outillage).",
            "FRAIS SUPPLEMENTAIRES POUR TRANSPORTS A GRANDE VITESSE ET HEURES SUPP.: Dans le cadre du produit MULTIRISQUES INFORMATIQUES, prise en charge des frais de transport express et des heures supplémentaires nécessaires à la remise en service rapide des installations après un sinistre.",
            "CATASTROPHES NATURELS (OURAGON, TREMBLEMENT DE TERRE, INONDATION): Dans le cadre du produit MULTIRISQUES INFORMATIQUES, garantie catastrophes naturelles (ouragan, tremblement de terre, inondation) : elle couvre les dommages causés par ces événements exceptionnels lorsque l’état de catastrophe naturelle est déclaré.",
            "DOMMAGES MATERIELS DES SMARTPHONES ET APPAREILS MULTIMEDIAS: Dans le cadre du produit MULTIRISQUES INFORMATIQUES, garantie dommages matériels des smartphones et appareils multimédias : elle couvre la réparation ou le remplacement de ces appareils en cas de chute, choc ou contact avec un liquide.",
            "ATTAQUES INFORMATIQUES ET CYBERNETIQUES: Dans le cadre du produit MULTIRISQUES INFORMATIQUES, garantie attaques informatiques et cybernétiques : elle indemnise les dommages liés aux cyberattaques, y compris la restauration des systèmes et la prise en charge des frais d’expertise spécialisée."
        ]
    },
    "TRANSPORT": {
        "produit: POLICE AU VOYAGE(FACULTE TERRESTRE)": [
            "TOUS RISQUE: Dans le cadre du produit POLICE AU VOYAGE(FACULTE TERRESTRE), garantie tous risques transport : elle couvre l’ensemble des dommages et pertes subis par les marchandises pendant le transport, quelle qu’en soit la cause, sauf exclusions spécifiques.",
            "ACCIDENT CARACTERISE: Dans le cadre du produit POLICE AU VOYAGE(FACULTE TERRESTRE), garantie accident caractérisé : elle couvre les dommages subis par les marchandises uniquement en cas d’accident de transport clairement identifié (collision, choc, renversement).",
            "TOUS RISQUE + VOL: Dans le cadre du produit POLICE AU VOYAGE(FACULTE TERRESTRE), garantie tous risques plus vol : elle étend la garantie tous risques aux cas de vol et de disparition totale ou partielle des marchandises."
        ],
        "produit: POLICE ABONNEMENT(FACULTE TERRESTRE)": [
            "TOUS RISQUE: Dans le cadre du produit POLICE ABONNEMENT(FACULTE TERRESTRE), garantie tous risques transport : elle couvre l’ensemble des dommages et pertes subis par les marchandises pendant le transport, quelle qu’en soit la cause, sauf exclusions spécifiques.",
            "ACCIDENT CARACTERISE: Dans le cadre du produit POLICE ABONNEMENT(FACULTE TERRESTRE), garantie accident caractérisé : elle couvre les dommages subis par les marchandises uniquement en cas d’accident de transport clairement identifié (collision, choc, renversement).",
            "TOUS RISQUE + VOL: Dans le cadre du produit POLICE ABONNEMENT(FACULTE TERRESTRE), garantie tous risques plus vol : elle étend la garantie tous risques aux cas de vol et de disparition totale ou partielle des marchandises."
        ],
        "produit: POLICE A ALIMENTER(FACULTE TERRESTRE)": [
            "TOUS RISQUE: Dans le cadre du produit POLICE A ALIMENTER(FACULTE TERRESTRE), garantie tous risques transport : elle couvre l’ensemble des dommages et pertes subis par les marchandises pendant le transport, quelle qu’en soit la cause, sauf exclusions spécifiques.",
            "ACCIDENT CARACTERISE: Dans le cadre du produit POLICE A ALIMENTER(FACULTE TERRESTRE), garantie accident caractérisé : elle couvre les dommages subis par les marchandises uniquement en cas d’accident de transport clairement identifié (collision, choc, renversement).",
            "TOUS RISQUE + VOL: Dans le cadre du produit POLICE A ALIMENTER(FACULTE TERRESTRE), garantie tous risques plus vol : elle étend la garantie tous risques aux cas de vol et de disparition totale ou partielle des marchandises."
        ],
        "produit: POLICE AU VOYAGE(FACULTE MARITIME)": [
            "TOUS RISQUE: Dans le cadre du produit POLICE AU VOYAGE(FACULTE MARITIME), garantie tous risques transport : elle couvre l’ensemble des dommages et pertes subis par les marchandises pendant le transport, quelle qu’en soit la cause, sauf exclusions spécifiques.",
            "FAP SAUF: Dans le cadre du produit POLICE AU VOYAGE(FACULTE MARITIME), garantie FAP sauf (Franc d’avarie particulière sauf) : couverture limitée aux pertes et dommages résultant de certains événements graves énumérés au contrat (naufrage, incendie, abordage), à l’exclusion des avaries courantes.",
            "ACCIDENT CARACTERISE: Dans le cadre du produit POLICE AU VOYAGE(FACULTE MARITIME), garantie accident caractérisé : elle couvre les dommages subis par les marchandises uniquement en cas d’accident de transport clairement identifié (collision, choc, renversement).",
            "RISQUE DE GUERRE: Dans le cadre du produit POLICE AU VOYAGE(FACULTE MARITIME), garantie risque de guerre : indemnisation des pertes ou dommages causés aux marchandises par des événements liés à la guerre ou à des actes assimilés.",
            "TOUS RISQUE + VOL: Dans le cadre du produit POLICE AU VOYAGE(FACULTE MARITIME), garantie tous risques plus vol : elle étend la garantie tous risques aux cas de vol et de disparition totale ou partielle des marchandises.",
            "H.S.S.C: Dans le cadre du produit POLICE AU VOYAGE(FACULTE MARITIME), garantie H.S.S.C. : intitulé spécifique dont l’objet doit être précisé dans le contrat (par exemple garantie pour chevaux de course ou clause maritime particulière)."
        ],
        "produit: POLICE ABONNEMENT(FACULTE MARITIME)": [
            "DECES TRIPLEMENT: Dans le cadre du produit POLICE ABONNEMENT(FACULTE MARITIME), garantie décès triplée (transport) : versement d’un capital triple en cas de décès accidentel d’un membre d’équipage ou d’un passager assuré.",
            "TOUS RISQUE: Dans le cadre du produit POLICE ABONNEMENT(FACULTE MARITIME), garantie tous risques transport : elle couvre l’ensemble des dommages et pertes subis par les marchandises pendant le transport, quelle qu’en soit la cause, sauf exclusions spécifiques.",
            "FAP SAUF: Dans le cadre du produit POLICE ABONNEMENT(FACULTE MARITIME), garantie FAP sauf (Franc d’avarie particulière sauf) : couverture limitée aux pertes et dommages résultant de certains événements graves énumérés au contrat (naufrage, incendie, abordage), à l’exclusion des avaries courantes.",
            "ACCIDENT CARACTERISE: Dans le cadre du produit POLICE ABONNEMENT(FACULTE MARITIME), garantie accident caractérisé : elle couvre les dommages subis par les marchandises uniquement en cas d’accident de transport clairement identifié (collision, choc, renversement).",
            "RISQUE DE GUERRE: Dans le cadre du produit POLICE ABONNEMENT(FACULTE MARITIME), garantie risque de guerre : indemnisation des pertes ou dommages causés aux marchandises par des événements liés à la guerre ou à des actes assimilés.",
            "TOUS RISQUE + VOL: Dans le cadre du produit POLICE ABONNEMENT(FACULTE MARITIME), garantie tous risques plus vol : elle étend la garantie tous risques aux cas de vol et de disparition totale ou partielle des marchandises.",
            "H.S.S.C: Dans le cadre du produit POLICE ABONNEMENT(FACULTE MARITIME), garantie H.S.S.C. : intitulé spécifique dont l’objet doit être précisé dans le contrat (par exemple garantie pour chevaux de course ou clause maritime particulière)."
        ],
        "produit: POLICE A ALIMENTER(FACULTE MARITIME)": [
            "TOUS RISQUE: Dans le cadre du produit POLICE A ALIMENTER(FACULTE MARITIME), garantie tous risques transport : elle couvre l’ensemble des dommages et pertes subis par les marchandises pendant le transport, quelle qu’en soit la cause, sauf exclusions spécifiques.",
            "FAP SAUF: Dans le cadre du produit POLICE A ALIMENTER(FACULTE MARITIME), garantie FAP sauf (Franc d’avarie particulière sauf) : couverture limitée aux pertes et dommages résultant de certains événements graves énumérés au contrat (naufrage, incendie, abordage), à l’exclusion des avaries courantes.",
            "ACCIDENT CARACTERISE: Dans le cadre du produit POLICE A ALIMENTER(FACULTE MARITIME), garantie accident caractérisé : elle couvre les dommages subis par les marchandises uniquement en cas d’accident de transport clairement identifié (collision, choc, renversement).",
            "RISQUE DE GUERRE: Dans le cadre du produit POLICE A ALIMENTER(FACULTE MARITIME), garantie risque de guerre : indemnisation des pertes ou dommages causés aux marchandises par des événements liés à la guerre ou à des actes assimilés.",
            "TOUS RISQUE + VOL: Dans le cadre du produit POLICE A ALIMENTER(FACULTE MARITIME), garantie tous risques plus vol : elle étend la garantie tous risques aux cas de vol et de disparition totale ou partielle des marchandises.",
            "H.S.S.C: Dans le cadre du produit POLICE A ALIMENTER(FACULTE MARITIME), garantie H.S.S.C. : intitulé spécifique dont l’objet doit être précisé dans le contrat (par exemple garantie pour chevaux de course ou clause maritime particulière)."
        ],
        "produit: POLICE AU VOYAGE(FACULTE AERIEN)": [
            "TOUS RISQUE: Dans le cadre du produit POLICE AU VOYAGE(FACULTE AERIEN), garantie tous risques transport : elle couvre l’ensemble des dommages et pertes subis par les marchandises pendant le transport, quelle qu’en soit la cause, sauf exclusions spécifiques.",
            "ACCIDENT CARACTERISE: Dans le cadre du produit POLICE AU VOYAGE(FACULTE AERIEN), garantie accident caractérisé : elle couvre les dommages subis par les marchandises uniquement en cas d’accident de transport clairement identifié (collision, choc, renversement).",
            "TOUS RISQUE + VOL: Dans le cadre du produit POLICE AU VOYAGE(FACULTE AERIEN), garantie tous risques plus vol : elle étend la garantie tous risques aux cas de vol et de disparition totale ou partielle des marchandises."
        ],
        "produit: POLICE ABONNEMENT(FACULTE AERIEN)": [
            "TOUS RISQUE: Dans le cadre du produit POLICE ABONNEMENT(FACULTE AERIEN), garantie tous risques transport : elle couvre l’ensemble des dommages et pertes subis par les marchandises pendant le transport, quelle qu’en soit la cause, sauf exclusions spécifiques.",
            "ACCIDENT CARACTERISE: Dans le cadre du produit POLICE ABONNEMENT(FACULTE AERIEN), garantie accident caractérisé : elle couvre les dommages subis par les marchandises uniquement en cas d’accident de transport clairement identifié (collision, choc, renversement).",
            "TOUS RISQUE + VOL: Dans le cadre du produit POLICE ABONNEMENT(FACULTE AERIEN), garantie tous risques plus vol : elle étend la garantie tous risques aux cas de vol et de disparition totale ou partielle des marchandises."
        ],
        "produit: POLICE A ALIMENTER(FACULTE AERIEN)": [
            "TOUS RISQUE: Dans le cadre du produit POLICE A ALIMENTER(FACULTE AERIEN), garantie tous risques transport : elle couvre l’ensemble des dommages et pertes subis par les marchandises pendant le transport, quelle qu’en soit la cause, sauf exclusions spécifiques.",
            "ACCIDENT CARACTERISE: Dans le cadre du produit POLICE A ALIMENTER(FACULTE AERIEN), garantie accident caractérisé : elle couvre les dommages subis par les marchandises uniquement en cas d’accident de transport clairement identifié (collision, choc, renversement).",
            "TOUS RISQUE + VOL: Dans le cadre du produit POLICE A ALIMENTER(FACULTE AERIEN), garantie tous risques plus vol : elle étend la garantie tous risques aux cas de vol et de disparition totale ou partielle des marchandises."
        ],
        "produit: POLICE AU VOYAGE(CORPS DE PLAISANCE)": [
            "TOUS RISQUE: Dans le cadre du produit POLICE AU VOYAGE(CORPS DE PLAISANCE), garantie tous risques transport : elle couvre l’ensemble des dommages et pertes subis par les marchandises pendant le transport, quelle qu’en soit la cause, sauf exclusions spécifiques.",
            "FAP SAUF: Dans le cadre du produit POLICE AU VOYAGE(CORPS DE PLAISANCE), garantie FAP sauf (Franc d’avarie particulière sauf) : couverture limitée aux pertes et dommages résultant de certains événements graves énumérés au contrat (naufrage, incendie, abordage), à l’exclusion des avaries courantes.",
            "RISQUE DE GUERRE: Dans le cadre du produit POLICE AU VOYAGE(CORPS DE PLAISANCE), garantie risque de guerre : indemnisation des pertes ou dommages causés aux marchandises par des événements liés à la guerre ou à des actes assimilés.",
            "TOUS RISQUE + VOL: Dans le cadre du produit POLICE AU VOYAGE(CORPS DE PLAISANCE), garantie tous risques plus vol : elle étend la garantie tous risques aux cas de vol et de disparition totale ou partielle des marchandises."
        ],
        "produit: POLICE ABONNEMENT(CORPS DE PLAISANCE)": [
            "TOUS RISQUE: Dans le cadre du produit POLICE ABONNEMENT(CORPS DE PLAISANCE), garantie tous risques transport : elle couvre l’ensemble des dommages et pertes subis par les marchandises pendant le transport, quelle qu’en soit la cause, sauf exclusions spécifiques.",
            "FAP SAUF: Dans le cadre du produit POLICE ABONNEMENT(CORPS DE PLAISANCE), garantie FAP sauf (Franc d’avarie particulière sauf) : couverture limitée aux pertes et dommages résultant de certains événements graves énumérés au contrat (naufrage, incendie, abordage), à l’exclusion des avaries courantes.",
            "ACCIDENT CARACTERISE: Dans le cadre du produit POLICE ABONNEMENT(CORPS DE PLAISANCE), garantie accident caractérisé : elle couvre les dommages subis par les marchandises uniquement en cas d’accident de transport clairement identifié (collision, choc, renversement).",
            "RISQUE DE GUERRE: Dans le cadre du produit POLICE ABONNEMENT(CORPS DE PLAISANCE), garantie risque de guerre : indemnisation des pertes ou dommages causés aux marchandises par des événements liés à la guerre ou à des actes assimilés.",
            "TOUS RISQUE + VOL: Dans le cadre du produit POLICE ABONNEMENT(CORPS DE PLAISANCE), garantie tous risques plus vol : elle étend la garantie tous risques aux cas de vol et de disparition totale ou partielle des marchandises."
        ],
        "produit: POLICE A ALIMENTER(CORPS DE PLAISANCE)": [
            "TOUS RISQUE: Dans le cadre du produit POLICE A ALIMENTER(CORPS DE PLAISANCE), garantie tous risques transport : elle couvre l’ensemble des dommages et pertes subis par les marchandises pendant le transport, quelle qu’en soit la cause, sauf exclusions spécifiques.",
            "FAP SAUF: Dans le cadre du produit POLICE A ALIMENTER(CORPS DE PLAISANCE), garantie FAP sauf (Franc d’avarie particulière sauf) : couverture limitée aux pertes et dommages résultant de certains événements graves énumérés au contrat (naufrage, incendie, abordage), à l’exclusion des avaries courantes.",
            "ACCIDENT CARACTERISE: Dans le cadre du produit POLICE A ALIMENTER(CORPS DE PLAISANCE), garantie accident caractérisé : elle couvre les dommages subis par les marchandises uniquement en cas d’accident de transport clairement identifié (collision, choc, renversement).",
            "RISQUE DE GUERRE: Dans le cadre du produit POLICE A ALIMENTER(CORPS DE PLAISANCE), garantie risque de guerre : indemnisation des pertes ou dommages causés aux marchandises par des événements liés à la guerre ou à des actes assimilés.",
            "TOUS RISQUE + VOL: Dans le cadre du produit POLICE A ALIMENTER(CORPS DE PLAISANCE), garantie tous risques plus vol : elle étend la garantie tous risques aux cas de vol et de disparition totale ou partielle des marchandises."
        ],
        "produit: POLICE AU VOYAGE(CORPS DE PECHE)": [
            "TOUS RISQUE: Dans le cadre du produit POLICE AU VOYAGE(CORPS DE PECHE), garantie tous risques transport : elle couvre l’ensemble des dommages et pertes subis par les marchandises pendant le transport, quelle qu’en soit la cause, sauf exclusions spécifiques.",
            "FAP SAUF: Dans le cadre du produit POLICE AU VOYAGE(CORPS DE PECHE), garantie FAP sauf (Franc d’avarie particulière sauf) : couverture limitée aux pertes et dommages résultant de certains événements graves énumérés au contrat (naufrage, incendie, abordage), à l’exclusion des avaries courantes.",
            "RISQUE DE GUERRE: Dans le cadre du produit POLICE AU VOYAGE(CORPS DE PECHE), garantie risque de guerre : indemnisation des pertes ou dommages causés aux marchandises par des événements liés à la guerre ou à des actes assimilés.",
            "TOUS RISQUE + VOL: Dans le cadre du produit POLICE AU VOYAGE(CORPS DE PECHE), garantie tous risques plus vol : elle étend la garantie tous risques aux cas de vol et de disparition totale ou partielle des marchandises."
        ],
        "produit: POLICE ABONNEMENT(CORPS DE PECHE)": [
            "TOUS RISQUE: Dans le cadre du produit POLICE ABONNEMENT(CORPS DE PECHE), garantie tous risques transport : elle couvre l’ensemble des dommages et pertes subis par les marchandises pendant le transport, quelle qu’en soit la cause, sauf exclusions spécifiques.",
            "FAP SAUF: Dans le cadre du produit POLICE ABONNEMENT(CORPS DE PECHE), garantie FAP sauf (Franc d’avarie particulière sauf) : couverture limitée aux pertes et dommages résultant de certains événements graves énumérés au contrat (naufrage, incendie, abordage), à l’exclusion des avaries courantes.",
            "ACCIDENT CARACTERISE: Dans le cadre du produit POLICE ABONNEMENT(CORPS DE PECHE), garantie accident caractérisé : elle couvre les dommages subis par les marchandises uniquement en cas d’accident de transport clairement identifié (collision, choc, renversement).",
            "RISQUE DE GUERRE: Dans le cadre du produit POLICE ABONNEMENT(CORPS DE PECHE), garantie risque de guerre : indemnisation des pertes ou dommages causés aux marchandises par des événements liés à la guerre ou à des actes assimilés.",
            "TOUS RISQUE + VOL: Dans le cadre du produit POLICE ABONNEMENT(CORPS DE PECHE), garantie tous risques plus vol : elle étend la garantie tous risques aux cas de vol et de disparition totale ou partielle des marchandises."
        ],
        "produit: POLICE A ALIMENTER(CORPS DE PECHE)": [
            "TOUS RISQUE: Dans le cadre du produit POLICE A ALIMENTER(CORPS DE PECHE), garantie tous risques transport : elle couvre l’ensemble des dommages et pertes subis par les marchandises pendant le transport, quelle qu’en soit la cause, sauf exclusions spécifiques.",
            "FAP SAUF: Dans le cadre du produit POLICE A ALIMENTER(CORPS DE PECHE), garantie FAP sauf (Franc d’avarie particulière sauf) : couverture limitée aux pertes et dommages résultant de certains événements graves énumérés au contrat (naufrage, incendie, abordage), à l’exclusion des avaries courantes.",
            "ACCIDENT CARACTERISE: Dans le cadre du produit POLICE A ALIMENTER(CORPS DE PECHE), garantie accident caractérisé : elle couvre les dommages subis par les marchandises uniquement en cas d’accident de transport clairement identifié (collision, choc, renversement).",
            "RISQUE DE GUERRE: Dans le cadre du produit POLICE A ALIMENTER(CORPS DE PECHE), garantie risque de guerre : indemnisation des pertes ou dommages causés aux marchandises par des événements liés à la guerre ou à des actes assimilés.",
            "TOUS RISQUE + VOL: Dans le cadre du produit POLICE A ALIMENTER(CORPS DE PECHE), garantie tous risques plus vol : elle étend la garantie tous risques aux cas de vol et de disparition totale ou partielle des marchandises."
        ],
        "produit: POLICE AU VOYAGE(CORPS DE TOUT NAVIRES)": [
            "TOUS RISQUE: Dans le cadre du produit POLICE AU VOYAGE(CORPS DE TOUT NAVIRES), garantie tous risques transport : elle couvre l’ensemble des dommages et pertes subis par les marchandises pendant le transport, quelle qu’en soit la cause, sauf exclusions spécifiques.",
            "FAP SAUF: Dans le cadre du produit POLICE AU VOYAGE(CORPS DE TOUT NAVIRES), garantie FAP sauf (Franc d’avarie particulière sauf) : couverture limitée aux pertes et dommages résultant de certains événements graves énumérés au contrat (naufrage, incendie, abordage), à l’exclusion des avaries courantes.",
            "RISQUE DE GUERRE: Dans le cadre du produit POLICE AU VOYAGE(CORPS DE TOUT NAVIRES), garantie risque de guerre : indemnisation des pertes ou dommages causés aux marchandises par des événements liés à la guerre ou à des actes assimilés.",
            "TOUS RISQUE + VOL: Dans le cadre du produit POLICE AU VOYAGE(CORPS DE TOUT NAVIRES), garantie tous risques plus vol : elle étend la garantie tous risques aux cas de vol et de disparition totale ou partielle des marchandises."
        ],
        "produit: POLICE ABONNEMENT(CORPS DE TOUT NAVIRES)": [
            "TOUS RISQUE: Dans le cadre du produit POLICE ABONNEMENT(CORPS DE TOUT NAVIRES), garantie tous risques transport : elle couvre l’ensemble des dommages et pertes subis par les marchandises pendant le transport, quelle qu’en soit la cause, sauf exclusions spécifiques.",
            "FAP SAUF: Dans le cadre du produit POLICE ABONNEMENT(CORPS DE TOUT NAVIRES), garantie FAP sauf (Franc d’avarie particulière sauf) : couverture limitée aux pertes et dommages résultant de certains événements graves énumérés au contrat (naufrage, incendie, abordage), à l’exclusion des avaries courantes.",
            "ACCIDENT CARACTERISE: Dans le cadre du produit POLICE ABONNEMENT(CORPS DE TOUT NAVIRES), garantie accident caractérisé : elle couvre les dommages subis par les marchandises uniquement en cas d’accident de transport clairement identifié (collision, choc, renversement).",
            "RISQUE DE GUERRE: Dans le cadre du produit POLICE ABONNEMENT(CORPS DE TOUT NAVIRES), garantie risque de guerre : indemnisation des pertes ou dommages causés aux marchandises par des événements liés à la guerre ou à des actes assimilés.",
            "TOUS RISQUE + VOL: Dans le cadre du produit POLICE ABONNEMENT(CORPS DE TOUT NAVIRES), garantie tous risques plus vol : elle étend la garantie tous risques aux cas de vol et de disparition totale ou partielle des marchandises."
        ],
        "produit: POLICE A ALIMENTER(CORPS DE TOUT NAVIRES)": [
            "TOUS RISQUE: Dans le cadre du produit POLICE A ALIMENTER(CORPS DE TOUT NAVIRES), garantie tous risques transport : elle couvre l’ensemble des dommages et pertes subis par les marchandises pendant le transport, quelle qu’en soit la cause, sauf exclusions spécifiques.",
            "FAP SAUF: Dans le cadre du produit POLICE A ALIMENTER(CORPS DE TOUT NAVIRES), garantie FAP sauf (Franc d’avarie particulière sauf) : couverture limitée aux pertes et dommages résultant de certains événements graves énumérés au contrat (naufrage, incendie, abordage), à l’exclusion des avaries courantes.",
            "ACCIDENT CARACTERISE: Dans le cadre du produit POLICE A ALIMENTER(CORPS DE TOUT NAVIRES), garantie accident caractérisé : elle couvre les dommages subis par les marchandises uniquement en cas d’accident de transport clairement identifié (collision, choc, renversement).",
            "RISQUE DE GUERRE: Dans le cadre du produit POLICE A ALIMENTER(CORPS DE TOUT NAVIRES), garantie risque de guerre : indemnisation des pertes ou dommages causés aux marchandises par des événements liés à la guerre ou à des actes assimilés.",
            "TOUS RISQUE + VOL: Dans le cadre du produit POLICE A ALIMENTER(CORPS DE TOUT NAVIRES), garantie tous risques plus vol : elle étend la garantie tous risques aux cas de vol et de disparition totale ou partielle des marchandises."
        ],
        "produit: POLICE AU VOYAGE(CORPS DE CONSTRUCTION NAVAL)": [
            "TOUS RISQUE: Dans le cadre du produit POLICE AU VOYAGE(CORPS DE CONSTRUCTION NAVAL), garantie tous risques transport : elle couvre l’ensemble des dommages et pertes subis par les marchandises pendant le transport, quelle qu’en soit la cause, sauf exclusions spécifiques.",
            "FAP SAUF: Dans le cadre du produit POLICE AU VOYAGE(CORPS DE CONSTRUCTION NAVAL), garantie FAP sauf (Franc d’avarie particulière sauf) : couverture limitée aux pertes et dommages résultant de certains événements graves énumérés au contrat (naufrage, incendie, abordage), à l’exclusion des avaries courantes.",
            "RISQUE DE GUERRE: Dans le cadre du produit POLICE AU VOYAGE(CORPS DE CONSTRUCTION NAVAL), garantie risque de guerre : indemnisation des pertes ou dommages causés aux marchandises par des événements liés à la guerre ou à des actes assimilés.",
            "TOUS RISQUE + VOL: Dans le cadre du produit POLICE AU VOYAGE(CORPS DE CONSTRUCTION NAVAL), garantie tous risques plus vol : elle étend la garantie tous risques aux cas de vol et de disparition totale ou partielle des marchandises."
        ],
        "produit: POLICE ABONNEMENT(CORPS DE CONSTRUCTION NAVAL)": [
            "TOUS RISQUE: Dans le cadre du produit POLICE ABONNEMENT(CORPS DE CONSTRUCTION NAVAL), garantie tous risques transport : elle couvre l’ensemble des dommages et pertes subis par les marchandises pendant le transport, quelle qu’en soit la cause, sauf exclusions spécifiques.",
            "FAP SAUF: Dans le cadre du produit POLICE ABONNEMENT(CORPS DE CONSTRUCTION NAVAL), garantie FAP sauf (Franc d’avarie particulière sauf) : couverture limitée aux pertes et dommages résultant de certains événements graves énumérés au contrat (naufrage, incendie, abordage), à l’exclusion des avaries courantes.",
            "ACCIDENT CARACTERISE: Dans le cadre du produit POLICE ABONNEMENT(CORPS DE CONSTRUCTION NAVAL), garantie accident caractérisé : elle couvre les dommages subis par les marchandises uniquement en cas d’accident de transport clairement identifié (collision, choc, renversement).",
            "RISQUE DE GUERRE: Dans le cadre du produit POLICE ABONNEMENT(CORPS DE CONSTRUCTION NAVAL), garantie risque de guerre : indemnisation des pertes ou dommages causés aux marchandises par des événements liés à la guerre ou à des actes assimilés.",
            "TOUS RISQUE + VOL: Dans le cadre du produit POLICE ABONNEMENT(CORPS DE CONSTRUCTION NAVAL), garantie tous risques plus vol : elle étend la garantie tous risques aux cas de vol et de disparition totale ou partielle des marchandises."
        ],
        "produit: POLICE A ALIMENTER(CORPS DE CONSTRUCTION NAVAL)": [
            "TOUS RISQUE: Dans le cadre du produit POLICE A ALIMENTER(CORPS DE CONSTRUCTION NAVAL), garantie tous risques transport : elle couvre l’ensemble des dommages et pertes subis par les marchandises pendant le transport, quelle qu’en soit la cause, sauf exclusions spécifiques.",
            "FAP SAUF: Dans le cadre du produit POLICE A ALIMENTER(CORPS DE CONSTRUCTION NAVAL), garantie FAP sauf (Franc d’avarie particulière sauf) : couverture limitée aux pertes et dommages résultant de certains événements graves énumérés au contrat (naufrage, incendie, abordage), à l’exclusion des avaries courantes.",
            "ACCIDENT CARACTERISE: Dans le cadre du produit POLICE A ALIMENTER(CORPS DE CONSTRUCTION NAVAL), garantie accident caractérisé : elle couvre les dommages subis par les marchandises uniquement en cas d’accident de transport clairement identifié (collision, choc, renversement).",
            "RISQUE DE GUERRE: Dans le cadre du produit POLICE A ALIMENTER(CORPS DE CONSTRUCTION NAVAL), garantie risque de guerre : indemnisation des pertes ou dommages causés aux marchandises par des événements liés à la guerre ou à des actes assimilés.",
            "TOUS RISQUE + VOL: Dans le cadre du produit POLICE A ALIMENTER(CORPS DE CONSTRUCTION NAVAL), garantie tous risques plus vol : elle étend la garantie tous risques aux cas de vol et de disparition totale ou partielle des marchandises."
        ],
        "produit: TRANSPORT CORPS AVIATION": [
            "TOUS RISQUE: Dans le cadre du produit TRANSPORT CORPS AVIATION, garantie tous risques transport : elle couvre l’ensemble des dommages et pertes subis par les marchandises pendant le transport, quelle qu’en soit la cause, sauf exclusions spécifiques.",
            "FAP SAUF: Dans le cadre du produit TRANSPORT CORPS AVIATION, garantie FAP sauf (Franc d’avarie particulière sauf) : couverture limitée aux pertes et dommages résultant de certains événements graves énumérés au contrat (naufrage, incendie, abordage), à l’exclusion des avaries courantes.",
            "RISQUE DE GUERRE: Dans le cadre du produit TRANSPORT CORPS AVIATION, garantie risque de guerre : indemnisation des pertes ou dommages causés aux marchandises par des événements liés à la guerre ou à des actes assimilés.",
            "TOUS RISQUE + VOL: Dans le cadre du produit TRANSPORT CORPS AVIATION, garantie tous risques plus vol : elle étend la garantie tous risques aux cas de vol et de disparition totale ou partielle des marchandises.",
            "RESPONSABILITE CIVILE: Dans le cadre du produit TRANSPORT CORPS AVIATION, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport.",
            "CORPS PERTE TOTALE: Dans le cadre du produit TRANSPORT CORPS AVIATION, garantie corps – perte totale : indemnisation en cas de perte totale du navire ou de l’aéronef assuré à la suite d’un événement couvert.",
            "CORPS: Dans le cadre du produit TRANSPORT CORPS AVIATION, garantie corps : elle couvre les dommages matériels subis par le navire ou le véhicule de transport assuré (coque, moteur, équipements)."
        ]
    },
    "INCENDIE": {
        "produit: INCENDIE RISQUES SIMPLE CENTRALISE": [
            "DEFENSE ET RECOURS: Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, garantie défense et recours : elle prend en charge les frais de procédure et d’assistance pour défendre l’assuré ou exercer un recours contre un responsable après un sinistre.",
            "INCENDIE: Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, garantie incendie : elle indemnise les dommages causés par le feu, la foudre, l’explosion ou la chute de la foudre aux bâtiments et contenus assurés.",
            "VOL : Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier.",
            "DEGATS DES EAUX: Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, garantie dégâts des eaux : elle prend en charge les dommages causés par des fuites, ruptures de conduites, débordements ou infiltrations accidentelles d’eau.",
            "RECONSTITUTION D ARCHIVES: Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, prise en charge des frais de reconstitution d’archives, de dossiers et de documents professionnels détruits ou volés à la suite d’un sinistre.",
            "TOUTES EXPLOSIONS ET CHUTE DE LA FOUDRE: Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, garantie toutes explosions et chute de la foudre : elle couvre les dommages résultant d’une explosion ou d’une chute de foudre sur le bâtiment assuré.",
            "PERTE INDIRECTE: Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, garantie perte indirecte : elle couvre les dépenses supplémentaires et pertes financières consécutives à un sinistre (retard de chantier, loyers…).",
            "CHUTE DE LA FOUDRE: Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, garantie chute de la foudre : elle couvre les dommages causés par la foudre tombant directement sur le bâtiment ou une installation assurée.",
            "PERTE DE LOYER: Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, remboursement de la perte de loyer subie par le propriétaire lorsque le bien devient inhabitable à la suite d’un sinistre garanti.",
            "HONORAIRE EXPERT: Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, remboursement des honoraires de l’expert mandaté pour évaluer les dommages à la suite d’un sinistre.",
            "MODELES-DESSIN, DOCUMENTS TECHNIQUES: Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, garantie modèles, dessins et documents techniques : elle couvre les frais de reconstitution ou de reproduction de documents techniques perdus ou détruits par un sinistre.",
            "FRAIS DE DEBLAIS ET DE DEMOLITION: Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, cette garantie couvre les risques spécifiques liés à 'FRAIS DE DEBLAIS ET DE DEMOLITION'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "CHUTE D APPAREILS DE NAVIGATION AERIENNE: Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, indemnisation des dommages causés par la chute d’appareils de navigation aérienne ou de parties de ceux‑ci sur les biens assurés.",
            "VALEUR A NEUF: Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, garantie valeur à neuf : elle indemnise le coût de reconstruction ou de remplacement des biens sinistrés sans application de vétusté.",
            "GREVE, EMEUTE ET MOUVEMENTS POPULAIRES: Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, cette garantie couvre les risques spécifiques liés à 'GREVE, EMEUTE ET MOUVEMENTS POPULAIRES'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "TEMPÊTES, OURAGANS, CYCLONES,GRÊLES: Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, garantie tempêtes, ouragans, cyclones et grêles : indemnisation des dommages causés par des vents violents ou des chutes de grêle.",
            "PRIVATION DE JOUISSANCE: Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, indemnité pour privation de jouissance : elle compense la perte d’usage du logement ou des locaux pendant la remise en état après un sinistre.",
            "TREMBLEMENT DE TERRE: Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, garantie tremblement de terre : elle couvre les dommages causés aux biens assurés par un séisme reconnu comme catastrophe naturelle.",
            "RESPONSABILITE CIVILE: Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport.",
            "DOMMAGES AUX APPAREILS ELECTRIQUES: Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, garantie dommages aux appareils électriques : elle couvre la détérioration des appareils électriques due à un incendie, une surtension ou un court‑circuit.",
            "RECOURS DES VOISINS ET TIERS: Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, garantie recours des voisins et tiers : elle couvre la responsabilité de l’assuré vis‑à‑vis des voisins et des tiers en cas de dommages provoqués par un sinistre survenu dans le bâtiment assuré.",
            "RENONCIATION A RECOURS : Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, renonciation à recours : clause par laquelle l’assureur renonce à exercer un recours contre un tiers responsable, souvent exigée dans les baux commerciaux.",
            "INONDATIONS: Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, garantie inondations : elle indemnise les dommages causés par une inondation, une remontée de nappe phréatique ou un ruissellement.",
            "CHOC DE VEHICULES TERRESTRES IDENTIFIES: Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, indemnisation des dommages causés aux biens assurés par la collision d’un véhicule terrestre identifié.",
            "RECOURS DES VOISINS ET TIERS (SUITE INCENDIE): Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, garantie recours des voisins et tiers (suite incendie) : elle prend en charge les dommages causés aux voisins et aux tiers par un incendie survenu chez l’assuré.",
            "FUMEE: Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, garantie fumée : elle couvre les dommages causés par la fumée provenant d’un incendie accidentel ou soudain.",
            "DETERIORATION MARCHANDISES DANS LES CHAMBRES FRIGORIFIQUES: Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, indemnisation des marchandises conservées en chambres frigorifiques détériorées à la suite d’un incendie ou d’une panne de froid.",
            "DETERIORATION MARCHANDISES APRES BRIS DE MACHINES: Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, indemnisation des marchandises détériorées à la suite d’un bris de machine (ex. compresseur) dans les installations frigorifiques.",
            "VEHICULES EN STATIONNEMENT: Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, garantie véhicules en stationnement : elle couvre les dommages subis par des véhicules stationnés sur le site assuré en cas d’incendie ou d’explosion.",
            "FRAIS DE LUTTE CONTRE L INCENDIE: Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, prise en charge des frais engagés pour lutter contre un incendie (extinction, pompiers) et éviter l’aggravation des dommages.",
            "FRAIS DE PEPLACEMENT: Dans le cadre du produit INCENDIE RISQUES SIMPLE CENTRALISE, garantie frais de déplacement : remboursement des frais engagés pour le déplacement des biens ou des personnes suite à un sinistre."
        ],
        "produit: INCENDIE RISQUES SIMPLE": [
            "INCENDIE: Dans le cadre du produit INCENDIE RISQUES SIMPLE, garantie incendie : elle indemnise les dommages causés par le feu, la foudre, l’explosion ou la chute de la foudre aux bâtiments et contenus assurés.",
            "TOUTES EXPLOSIONS ET CHUTE DE LA FOUDRE: Dans le cadre du produit INCENDIE RISQUES SIMPLE, garantie toutes explosions et chute de la foudre : elle couvre les dommages résultant d’une explosion ou d’une chute de foudre sur le bâtiment assuré.",
            "PERTE INDIRECTE: Dans le cadre du produit INCENDIE RISQUES SIMPLE, garantie perte indirecte : elle couvre les dépenses supplémentaires et pertes financières consécutives à un sinistre (retard de chantier, loyers…).",
            "RESPONSABILITE CIVILE: Dans le cadre du produit INCENDIE RISQUES SIMPLE, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport.",
            "DOMMAGES AUX APPAREILS ELECTRIQUES: Dans le cadre du produit INCENDIE RISQUES SIMPLE, garantie dommages aux appareils électriques : elle couvre la détérioration des appareils électriques due à un incendie, une surtension ou un court‑circuit.",
            "RECOURS DES VOISINS ET TIERS: Dans le cadre du produit INCENDIE RISQUES SIMPLE, garantie recours des voisins et tiers : elle couvre la responsabilité de l’assuré vis‑à‑vis des voisins et des tiers en cas de dommages provoqués par un sinistre survenu dans le bâtiment assuré."
        ],
        "produit: INCENDIE RISQUES SIMPLE AMICALE": [
            "DEFENSE ET RECOURS: Dans le cadre du produit INCENDIE RISQUES SIMPLE AMICALE, garantie défense et recours : elle prend en charge les frais de procédure et d’assistance pour défendre l’assuré ou exercer un recours contre un responsable après un sinistre.",
            "INCENDIE: Dans le cadre du produit INCENDIE RISQUES SIMPLE AMICALE, garantie incendie : elle indemnise les dommages causés par le feu, la foudre, l’explosion ou la chute de la foudre aux bâtiments et contenus assurés.",
            "VOL : Dans le cadre du produit INCENDIE RISQUES SIMPLE AMICALE, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier.",
            "DEGATS DES EAUX: Dans le cadre du produit INCENDIE RISQUES SIMPLE AMICALE, garantie dégâts des eaux : elle prend en charge les dommages causés par des fuites, ruptures de conduites, débordements ou infiltrations accidentelles d’eau.",
            "RECONSTITUTION D ARCHIVES: Dans le cadre du produit INCENDIE RISQUES SIMPLE AMICALE, prise en charge des frais de reconstitution d’archives, de dossiers et de documents professionnels détruits ou volés à la suite d’un sinistre.",
            "TOUTES EXPLOSIONS ET CHUTE DE LA FOUDRE: Dans le cadre du produit INCENDIE RISQUES SIMPLE AMICALE, garantie toutes explosions et chute de la foudre : elle couvre les dommages résultant d’une explosion ou d’une chute de foudre sur le bâtiment assuré.",
            "PERTE INDIRECTE: Dans le cadre du produit INCENDIE RISQUES SIMPLE AMICALE, garantie perte indirecte : elle couvre les dépenses supplémentaires et pertes financières consécutives à un sinistre (retard de chantier, loyers…).",
            "CHUTE DE LA FOUDRE: Dans le cadre du produit INCENDIE RISQUES SIMPLE AMICALE, garantie chute de la foudre : elle couvre les dommages causés par la foudre tombant directement sur le bâtiment ou une installation assurée.",
            "PERTE DE LOYER: Dans le cadre du produit INCENDIE RISQUES SIMPLE AMICALE, remboursement de la perte de loyer subie par le propriétaire lorsque le bien devient inhabitable à la suite d’un sinistre garanti.",
            "HONORAIRE EXPERT: Dans le cadre du produit INCENDIE RISQUES SIMPLE AMICALE, remboursement des honoraires de l’expert mandaté pour évaluer les dommages à la suite d’un sinistre.",
            "MODELES-DESSIN, DOCUMENTS TECHNIQUES: Dans le cadre du produit INCENDIE RISQUES SIMPLE AMICALE, garantie modèles, dessins et documents techniques : elle couvre les frais de reconstitution ou de reproduction de documents techniques perdus ou détruits par un sinistre.",
            "FRAIS DE DEBLAIS ET DE DEMOLITION: Dans le cadre du produit INCENDIE RISQUES SIMPLE AMICALE, cette garantie couvre les risques spécifiques liés à 'FRAIS DE DEBLAIS ET DE DEMOLITION'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "CHUTE D APPAREILS DE NAVIGATION AERIENNE: Dans le cadre du produit INCENDIE RISQUES SIMPLE AMICALE, indemnisation des dommages causés par la chute d’appareils de navigation aérienne ou de parties de ceux‑ci sur les biens assurés.",
            "VALEUR A NEUF: Dans le cadre du produit INCENDIE RISQUES SIMPLE AMICALE, garantie valeur à neuf : elle indemnise le coût de reconstruction ou de remplacement des biens sinistrés sans application de vétusté.",
            "GREVE, EMEUTE ET MOUVEMENTS POPULAIRES: Dans le cadre du produit INCENDIE RISQUES SIMPLE AMICALE, cette garantie couvre les risques spécifiques liés à 'GREVE, EMEUTE ET MOUVEMENTS POPULAIRES'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "TEMPÊTES, OURAGANS, CYCLONES,GRÊLES: Dans le cadre du produit INCENDIE RISQUES SIMPLE AMICALE, garantie tempêtes, ouragans, cyclones et grêles : indemnisation des dommages causés par des vents violents ou des chutes de grêle.",
            "PRIVATION DE JOUISSANCE: Dans le cadre du produit INCENDIE RISQUES SIMPLE AMICALE, indemnité pour privation de jouissance : elle compense la perte d’usage du logement ou des locaux pendant la remise en état après un sinistre.",
            "TREMBLEMENT DE TERRE: Dans le cadre du produit INCENDIE RISQUES SIMPLE AMICALE, garantie tremblement de terre : elle couvre les dommages causés aux biens assurés par un séisme reconnu comme catastrophe naturelle.",
            "RESPONSABILITE CIVILE: Dans le cadre du produit INCENDIE RISQUES SIMPLE AMICALE, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport.",
            "DOMMAGES AUX APPAREILS ELECTRIQUES: Dans le cadre du produit INCENDIE RISQUES SIMPLE AMICALE, garantie dommages aux appareils électriques : elle couvre la détérioration des appareils électriques due à un incendie, une surtension ou un court‑circuit.",
            "RECOURS DES VOISINS ET TIERS: Dans le cadre du produit INCENDIE RISQUES SIMPLE AMICALE, garantie recours des voisins et tiers : elle couvre la responsabilité de l’assuré vis‑à‑vis des voisins et des tiers en cas de dommages provoqués par un sinistre survenu dans le bâtiment assuré.",
            "RENONCIATION A RECOURS : Dans le cadre du produit INCENDIE RISQUES SIMPLE AMICALE, renonciation à recours : clause par laquelle l’assureur renonce à exercer un recours contre un tiers responsable, souvent exigée dans les baux commerciaux.",
            "RECOURS DES VOISINS ET TIERS (SUITE INCENDIE): Dans le cadre du produit INCENDIE RISQUES SIMPLE AMICALE, garantie recours des voisins et tiers (suite incendie) : elle prend en charge les dommages causés aux voisins et aux tiers par un incendie survenu chez l’assuré."
        ],
        "produit: INCENDIE RISQUES INDUSTRIEL": [
            "DEFENSE ET RECOURS: Dans le cadre du produit INCENDIE RISQUES INDUSTRIEL, garantie défense et recours : elle prend en charge les frais de procédure et d’assistance pour défendre l’assuré ou exercer un recours contre un responsable après un sinistre.",
            "INCENDIE: Dans le cadre du produit INCENDIE RISQUES INDUSTRIEL, garantie incendie : elle indemnise les dommages causés par le feu, la foudre, l’explosion ou la chute de la foudre aux bâtiments et contenus assurés.",
            "VOL : Dans le cadre du produit INCENDIE RISQUES INDUSTRIEL, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier.",
            "DEGATS DES EAUX: Dans le cadre du produit INCENDIE RISQUES INDUSTRIEL, garantie dégâts des eaux : elle prend en charge les dommages causés par des fuites, ruptures de conduites, débordements ou infiltrations accidentelles d’eau.",
            "PERTE EXPLOITATION APRES INCENDIE: Dans le cadre du produit INCENDIE RISQUES INDUSTRIEL, garantie perte d’exploitation après incendie : indemnisation de la perte de marge brute résultant d’un arrêt d’activité à la suite d’un incendie.",
            "RECONSTITUTION D ARCHIVES: Dans le cadre du produit INCENDIE RISQUES INDUSTRIEL, prise en charge des frais de reconstitution d’archives, de dossiers et de documents professionnels détruits ou volés à la suite d’un sinistre.",
            "TOUTES EXPLOSIONS ET CHUTE DE LA FOUDRE: Dans le cadre du produit INCENDIE RISQUES INDUSTRIEL, garantie toutes explosions et chute de la foudre : elle couvre les dommages résultant d’une explosion ou d’une chute de foudre sur le bâtiment assuré.",
            "PERTE INDIRECTE: Dans le cadre du produit INCENDIE RISQUES INDUSTRIEL, garantie perte indirecte : elle couvre les dépenses supplémentaires et pertes financières consécutives à un sinistre (retard de chantier, loyers…).",
            "CHUTE DE LA FOUDRE: Dans le cadre du produit INCENDIE RISQUES INDUSTRIEL, garantie chute de la foudre : elle couvre les dommages causés par la foudre tombant directement sur le bâtiment ou une installation assurée.",
            "PERTE DE LOYER: Dans le cadre du produit INCENDIE RISQUES INDUSTRIEL, remboursement de la perte de loyer subie par le propriétaire lorsque le bien devient inhabitable à la suite d’un sinistre garanti.",
            "HONORAIRE EXPERT: Dans le cadre du produit INCENDIE RISQUES INDUSTRIEL, remboursement des honoraires de l’expert mandaté pour évaluer les dommages à la suite d’un sinistre.",
            "MODELES-DESSIN, DOCUMENTS TECHNIQUES: Dans le cadre du produit INCENDIE RISQUES INDUSTRIEL, garantie modèles, dessins et documents techniques : elle couvre les frais de reconstitution ou de reproduction de documents techniques perdus ou détruits par un sinistre.",
            "FRAIS DE DEBLAIS ET DE DEMOLITION: Dans le cadre du produit INCENDIE RISQUES INDUSTRIEL, cette garantie couvre les risques spécifiques liés à 'FRAIS DE DEBLAIS ET DE DEMOLITION'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "CHUTE D APPAREILS DE NAVIGATION AERIENNE: Dans le cadre du produit INCENDIE RISQUES INDUSTRIEL, indemnisation des dommages causés par la chute d’appareils de navigation aérienne ou de parties de ceux‑ci sur les biens assurés.",
            "VALEUR A NEUF: Dans le cadre du produit INCENDIE RISQUES INDUSTRIEL, garantie valeur à neuf : elle indemnise le coût de reconstruction ou de remplacement des biens sinistrés sans application de vétusté.",
            "GREVE, EMEUTE ET MOUVEMENTS POPULAIRES: Dans le cadre du produit INCENDIE RISQUES INDUSTRIEL, cette garantie couvre les risques spécifiques liés à 'GREVE, EMEUTE ET MOUVEMENTS POPULAIRES'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "TEMPÊTES, OURAGANS, CYCLONES,GRÊLES: Dans le cadre du produit INCENDIE RISQUES INDUSTRIEL, garantie tempêtes, ouragans, cyclones et grêles : indemnisation des dommages causés par des vents violents ou des chutes de grêle.",
            "PRIVATION DE JOUISSANCE: Dans le cadre du produit INCENDIE RISQUES INDUSTRIEL, indemnité pour privation de jouissance : elle compense la perte d’usage du logement ou des locaux pendant la remise en état après un sinistre.",
            "TREMBLEMENT DE TERRE: Dans le cadre du produit INCENDIE RISQUES INDUSTRIEL, garantie tremblement de terre : elle couvre les dommages causés aux biens assurés par un séisme reconnu comme catastrophe naturelle.",
            "RESPONSABILITE CIVILE: Dans le cadre du produit INCENDIE RISQUES INDUSTRIEL, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport.",
            "DOMMAGES AUX APPAREILS ELECTRIQUES: Dans le cadre du produit INCENDIE RISQUES INDUSTRIEL, garantie dommages aux appareils électriques : elle couvre la détérioration des appareils électriques due à un incendie, une surtension ou un court‑circuit.",
            "RECOURS DES LOCATAIRES: Dans le cadre du produit INCENDIE RISQUES INDUSTRIEL, garantie recours des locataires : elle protège le propriétaire contre les réclamations de ses locataires pour dommages causés à leurs biens lors d’un sinistre touchant l’immeuble.",
            "RECOURS DES VOISINS ET TIERS: Dans le cadre du produit INCENDIE RISQUES INDUSTRIEL, garantie recours des voisins et tiers : elle couvre la responsabilité de l’assuré vis‑à‑vis des voisins et des tiers en cas de dommages provoqués par un sinistre survenu dans le bâtiment assuré.",
            "RENONCIATION A RECOURS : Dans le cadre du produit INCENDIE RISQUES INDUSTRIEL, renonciation à recours : clause par laquelle l’assureur renonce à exercer un recours contre un tiers responsable, souvent exigée dans les baux commerciaux.",
            "INONDATIONS: Dans le cadre du produit INCENDIE RISQUES INDUSTRIEL, garantie inondations : elle indemnise les dommages causés par une inondation, une remontée de nappe phréatique ou un ruissellement.",
            "CHOC DE VEHICULES TERRESTRES IDENTIFIES: Dans le cadre du produit INCENDIE RISQUES INDUSTRIEL, indemnisation des dommages causés aux biens assurés par la collision d’un véhicule terrestre identifié.",
            "RECOURS DES VOISINS ET TIERS (SUITE INCENDIE): Dans le cadre du produit INCENDIE RISQUES INDUSTRIEL, garantie recours des voisins et tiers (suite incendie) : elle prend en charge les dommages causés aux voisins et aux tiers par un incendie survenu chez l’assuré."
        ],
        "produit: INCENDIE COMMERCIAL / LEASING": [
            "INCENDIE: Dans le cadre du produit INCENDIE COMMERCIAL / LEASING, garantie incendie : elle indemnise les dommages causés par le feu, la foudre, l’explosion ou la chute de la foudre aux bâtiments et contenus assurés.",
            "VOL : Dans le cadre du produit INCENDIE COMMERCIAL / LEASING, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier.",
            "DEGATS DES EAUX: Dans le cadre du produit INCENDIE COMMERCIAL / LEASING, garantie dégâts des eaux : elle prend en charge les dommages causés par des fuites, ruptures de conduites, débordements ou infiltrations accidentelles d’eau.",
            "DOMMAGES AUX APPAREILS ELECTRIQUES: Dans le cadre du produit INCENDIE COMMERCIAL / LEASING, garantie dommages aux appareils électriques : elle couvre la détérioration des appareils électriques due à un incendie, une surtension ou un court‑circuit."
        ],
        "produit: MULTIRISQUES PROFESSIONNELLES CENTRALISE": [
            "DEFENSE ET RECOURS: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, garantie défense et recours : elle prend en charge les frais de procédure et d’assistance pour défendre l’assuré ou exercer un recours contre un responsable après un sinistre.",
            "INCENDIE: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, garantie incendie : elle indemnise les dommages causés par le feu, la foudre, l’explosion ou la chute de la foudre aux bâtiments et contenus assurés.",
            "VOL : Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier.",
            "BRIS DE GLACES: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, garantie bris de glaces : elle couvre la réparation ou le remplacement des vitres, vitrines, miroirs ou surfaces en verre endommagés.",
            "DEGATS DES EAUX: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, garantie dégâts des eaux : elle prend en charge les dommages causés par des fuites, ruptures de conduites, débordements ou infiltrations accidentelles d’eau.",
            "PERTE EXPLOITATION APRES INCENDIE: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, garantie perte d’exploitation après incendie : indemnisation de la perte de marge brute résultant d’un arrêt d’activité à la suite d’un incendie.",
            "RECONSTITUTION D ARCHIVES: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, prise en charge des frais de reconstitution d’archives, de dossiers et de documents professionnels détruits ou volés à la suite d’un sinistre.",
            "TOUTES EXPLOSIONS ET CHUTE DE LA FOUDRE: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, garantie toutes explosions et chute de la foudre : elle couvre les dommages résultant d’une explosion ou d’une chute de foudre sur le bâtiment assuré.",
            "PERTE INDIRECTE: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, garantie perte indirecte : elle couvre les dépenses supplémentaires et pertes financières consécutives à un sinistre (retard de chantier, loyers…).",
            "PERTE DE LOYER: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, remboursement de la perte de loyer subie par le propriétaire lorsque le bien devient inhabitable à la suite d’un sinistre garanti.",
            "HONORAIRE EXPERT: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, remboursement des honoraires de l’expert mandaté pour évaluer les dommages à la suite d’un sinistre.",
            "FRAIS DE DEBLAIS ET DE DEMOLITION: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, cette garantie couvre les risques spécifiques liés à 'FRAIS DE DEBLAIS ET DE DEMOLITION'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "CHUTE D APPAREILS DE NAVIGATION AERIENNE: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, indemnisation des dommages causés par la chute d’appareils de navigation aérienne ou de parties de ceux‑ci sur les biens assurés.",
            "VALEUR A NEUF: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, garantie valeur à neuf : elle indemnise le coût de reconstruction ou de remplacement des biens sinistrés sans application de vétusté.",
            "GREVE, EMEUTE ET MOUVEMENTS POPULAIRES: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, cette garantie couvre les risques spécifiques liés à 'GREVE, EMEUTE ET MOUVEMENTS POPULAIRES'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "TEMPÊTES, OURAGANS, CYCLONES,GRÊLES: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, garantie tempêtes, ouragans, cyclones et grêles : indemnisation des dommages causés par des vents violents ou des chutes de grêle.",
            "PRIVATION DE JOUISSANCE: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, indemnité pour privation de jouissance : elle compense la perte d’usage du logement ou des locaux pendant la remise en état après un sinistre.",
            "TREMBLEMENT DE TERRE: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, garantie tremblement de terre : elle couvre les dommages causés aux biens assurés par un séisme reconnu comme catastrophe naturelle.",
            "DETERIORATION MOBILIERE ET IMMOBILIERE SUITE VOL: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, indemnisation des détériorations mobilières et immobilières causées par une effraction ou un vol (porte fracturée, serrures forcées, mobilier endommagé).",
            "RESPONSABILITE CIVILE: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport.",
            "DOMMAGES AUX APPAREILS ELECTRIQUES: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, garantie dommages aux appareils électriques : elle couvre la détérioration des appareils électriques due à un incendie, une surtension ou un court‑circuit.",
            "FRAIS SUPPLEMENTAIRES: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, prise en charge des frais supplémentaires engagés pour continuer ou reprendre l’activité après un sinistre (location de locaux temporaires, heures supplémentaires).",
            "INDIVIDUELLE ACCIDENT: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, garantie individuelle accident : elle verse un capital ou une rente en cas de décès ou d’invalidité d’une personne assurée lors d’un accident survenu dans les locaux.",
            "PERTE ET RECONSTITUTIONS DES DONNEES: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, garantie perte et reconstitution des données : prise en charge des frais pour récupérer ou reconstituer des données informatiques perdues à la suite d’un sinistre.",
            "RECOURS DES LOCATAIRES: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, garantie recours des locataires : elle protège le propriétaire contre les réclamations de ses locataires pour dommages causés à leurs biens lors d’un sinistre touchant l’immeuble.",
            "INFILTRATIONS ACCIDENTELLES AU TRAVERS DES TOITURES: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, indemnisation des dommages provoqués par des infiltrations d’eau accidentelles à travers la toiture ou la couverture du bâtiment.",
            "RECOURS DES VOISINS ET TIERS: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, garantie recours des voisins et tiers : elle couvre la responsabilité de l’assuré vis‑à‑vis des voisins et des tiers en cas de dommages provoqués par un sinistre survenu dans le bâtiment assuré.",
            "FRAIS DE RELOGEMENT DES CLIENTS: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, prise en charge des frais de relogement des clients (par exemple d’un hôtel) lorsque l’établissement est temporairement inhabitable à la suite d’un sinistre.",
            "RENONCIATION A RECOURS : Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, renonciation à recours : clause par laquelle l’assureur renonce à exercer un recours contre un tiers responsable, souvent exigée dans les baux commerciaux.",
            "INONDATIONS: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, garantie inondations : elle indemnise les dommages causés par une inondation, une remontée de nappe phréatique ou un ruissellement.",
            "EFFET DES CLIENTS: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, garantie effets des clients : indemnisation des effets personnels des clients (vêtements, bagages) détruits ou volés lors d’un sinistre dans l’établissement.",
            "RC- DOMMAGES CORPORELS: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, responsabilité civile – dommages corporels : prise en charge des indemnités dues aux tiers pour les blessures ou atteintes corporelles causées par l’assuré.",
            "RC- DOMMAGES MATERIELS: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, responsabilité civile – dommages matériels : indemnisation des dégâts matériels causés à des biens appartenant à des tiers.",
            "RC- INTOXICATION ALIMENTAIRE: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, responsabilité civile – intoxication alimentaire : indemnisation des victimes de toxi‑infections alimentaires causées par des aliments préparés ou vendus par l’assuré.",
            "RC- PROFESSIONNELLE: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, responsabilité civile professionnelle : elle couvre les dommages causés à des tiers dans le cadre de l’activité professionnelle de l’assuré.",
            "CHOC DE VEHICULES TERRESTRES IDENTIFIES: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, indemnisation des dommages causés aux biens assurés par la collision d’un véhicule terrestre identifié.",
            "FRAIS DE SAUVETAGE: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, prise en charge des frais de sauvetage : remboursement des dépenses pour préserver les biens et limiter les dégâts pendant un sinistre.",
            "FUMEE: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, garantie fumée : elle couvre les dommages causés par la fumée provenant d’un incendie accidentel ou soudain.",
            "TERRORISME: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, garantie terrorisme : indemnisation des dommages causés aux biens assurés par des actes de terrorisme reconnus par les autorités.",
            "FRAIS DE POSE ET DE REPOSE: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, garantie frais de pose et de repose : remboursement des frais nécessaires pour retirer et reposer des installations lors des réparations après sinistre.",
            "FRAIS DE RECHERCHE DES FUITES D EAUX: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, prise en charge des frais engagés pour localiser et diagnostiquer l’origine d’une fuite d’eau responsable d’un sinistre.",
            "VOL ESPECE EN CAISSE: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, garantie vol d’espèces en caisse : elle couvre le vol d’argent liquide conservé dans la caisse ou dans un coffre pendant les heures d’ouverture.",
            "R.C DEPOSITAIRE: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, responsabilité civile du dépositaire : indemnisation des dommages ou pertes subis par des biens confiés en dépôt chez l’assuré.",
            "BRIS DE MACHINES: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, cette garantie couvre les risques spécifiques liés à 'BRIS DE MACHINES'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "PERTES EXPLOITATION APRES BRIS DE MACHINES: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, garantie pertes d’exploitation après bris de machines : indemnisation de la perte de chiffre d’affaires résultant de l’arrêt de l’activité à la suite d’un bris de machine couvert.",
            "DOMMAGE MATERIELS INFORMATIQUES: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, garantie dommages matériels informatiques : elle couvre la réparation ou le remplacement du matériel informatique endommagé par un sinistre.",
            "DETERIORATION MARCHANDISES DANS LES CHAMBRES FRIGORIFIQUES: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, indemnisation des marchandises conservées en chambres frigorifiques détériorées à la suite d’un incendie ou d’une panne de froid.",
            "DETERIORATION MARCHANDISES APRES BRIS DE MACHINES: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, indemnisation des marchandises détériorées à la suite d’a bris de machine (ex. compresseur) dans les installations frigorifiques.",
            "DOMMAGES AUX VEHICULES NEUFS EXPOSES A ENCEINTE DU SHOWROOM COUVERT: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, indemnisation des dommages causés aux véhicules neufs exposés dans un showroom couvert lors d’un incendie, d’un vol ou d’une catastrophe naturelle.",
            "DOMMAGES AUX VEHICULES NEUFS EXPOSES EN PLEIN AIR: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, indemnisation des dommages causés aux véhicules neufs exposés en plein air (vent, grêle, actes de vandalisme).",
            "DOMMAGES INEXPLIQUES AUX VEHICULES NEUFS: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, garantie dommages inexpliqués aux véhicules neufs : elle couvre les détériorations constatées sur des véhicules neufs sans cause apparente.",
            "RC APRES LIVRAISON: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, responsabilité civile après livraison : couvre les dommages causés aux tiers après la livraison d’un produit ou l’achèvement d’un service.",
            "RC PROFESSIONNELLE : DOMMAGES CORPORELS: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, responsabilité civile professionnelle – dommages corporels : indemnisation des blessures causées à des clients ou à des tiers par l’assuré ou ses préposés dans l’exercice de son activité.",
            "RC PROFESSIONNELLE : DOMMAGES MATERIELS: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, responsabilité civile professionnelle – dommages matériels : indemnisation des biens de tiers endommagés par l’assuré dans le cadre de son activité professionnelle.",
            "RC EXPLOITATION : DOMMAGES CORPORELS: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, responsabilité civile exploitation – dommages corporels : couvre les blessures causées aux tiers dans le cadre de l’exploitation d’une entreprise.",
            "RC EXPLOITATION : DOMMAGES MATERIELS: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, responsabilité civile exploitation – dommages matériels : couvre les dégâts causés à des biens de tiers lors de l’exploitation de l’entreprise.",
            "ASSURANCE AUTOMATIQUE DE LA GARANTIE: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, clause d’assurance automatique : extension automatique des garanties existantes à de nouveaux biens ou bâtiments sans déclaration préalable, dans certaines limites.",
            "CLAUSES DE REVERSIBILITE DES EXCEDENTS: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, clause de réversibilité des excédents : disposition permettant la restitution d’une partie des excédents techniques ou financiers au souscripteur en fin d’exercice.",
            "PERTES DES DONNEES ET DE LEURS SUPPORTS DES DONNEES: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, garantie pertes de données et de leurs supports : couverture des coûts de remplacement des supports et de récupération des informations détruites.",
            "DETOURNEMENT DE FONDS PAR LES PREPOSES: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, garantie détournement de fonds par les employés ou mandataires de l’assuré.",
            "FRAIS DE DEPLACEMENT ET DE REPLACEMENT: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, prise en charge des frais de déplacement et de replacement : remboursement des dépenses pour transférer et repositionner les biens lors des travaux de remise en état.",
            "PERTE DE PRODUIT: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES CENTRALISE, garantie perte de produit : indemnisation des pertes de marchandises ou de produits finis résultant d’un sinistre (incendie, dégât des eaux)."
        ],
        "produit: MULTIRISQUE HOTELIER": [
            "INCENDIE: Dans le cadre du produit MULTIRISQUE HOTELIER, garantie incendie : elle indemnise les dommages causés par le feu, la foudre, l’explosion ou la chute de la foudre aux bâtiments et contenus assurés.",
            "VOL : Dans le cadre du produit MULTIRISQUE HOTELIER, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier.",
            "BRIS DE GLACES: Dans le cadre du produit MULTIRISQUE HOTELIER, garantie bris de glaces : elle couvre la réparation ou le remplacement des vitres, vitrines, miroirs ou surfaces en verre endommagés.",
            "DEGATS DES EAUX: Dans le cadre du produit MULTIRISQUE HOTELIER, garantie dégâts des eaux : elle prend en charge les dommages causés par des fuites, ruptures de conduites, débordements ou infiltrations accidentelles d’eau.",
            "PERTE EXPLOITATION APRES INCENDIE: Dans le cadre du produit MULTIRISQUE HOTELIER, garantie perte d’exploitation après incendie : indemnisation de la perte de marge brute résultant d’un arrêt d’activité à la suite d’un incendie.",
            "TOUTES EXPLOSIONS ET CHUTE DE LA FOUDRE: Dans le cadre du produit MULTIRISQUE HOTELIER, garantie toutes explosions et chute de la foudre : elle couvre les dommages résultant d’une explosion ou d’une chute de foudre sur le bâtiment assuré.",
            "PERTE INDIRECTE: Dans le cadre du produit MULTIRISQUE HOTELIER, garantie perte indirecte : elle couvre les dépenses supplémentaires et pertes financières consécutives à un sinistre (retard de chantier, loyers…).",
            "CHUTE DE LA FOUDRE: Dans le cadre du produit MULTIRISQUE HOTELIER, garantie chute de la foudre : elle couvre les dommages causés par la foudre tombant directement sur le bâtiment ou une installation assurée.",
            "HONORAIRE EXPERT: Dans le cadre du produit MULTIRISQUE HOTELIER, remboursement des honoraires de l’expert mandaté pour évaluer les dommages à la suite d’un sinistre.",
            "FRAIS DE DEBLAIS ET DE DEMOLITION: Dans le cadre du produit MULTIRISQUE HOTELIER, cette garantie couvre les risques spécifiques liés à 'FRAIS DE DEBLAIS ET DE DEMOLITION'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "CHUTE D APPAREILS DE NAVIGATION AERIENNE: Dans le cadre du produit MULTIRISQUE HOTELIER, indemnisation des dommages causés par la chute d’appareils de navigation aérienne ou de parties de ceux‑ci sur les biens assurés.",
            "VALEUR A NEUF: Dans le cadre du produit MULTIRISQUE HOTELIER, garantie valeur à neuf : elle indemnise le coût de reconstruction ou de remplacement des biens sinistrés sans application de vétusté.",
            "GREVE, EMEUTE ET MOUVEMENTS POPULAIRES: Dans le cadre du produit MULTIRISQUE HOTELIER, cette garantie couvre les risques spécifiques liés à 'GREVE, EMEUTE ET MOUVEMENTS POPULAIRES'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "RESPONSABILITE CIVILE: Dans le cadre du produit MULTIRISQUE HOTELIER, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport.",
            "DOMMAGES AUX APPAREILS ELECTRIQUES: Dans le cadre du produit MULTIRISQUE HOTELIER, garantie dommages aux appareils électriques : elle couvre la détérioration des appareils électriques due à un incendie, une surtension ou un court‑circuit.",
            "INFILTRATIONS ACCIDENTELLES AU TRAVERS DES TOITURES: Dans le cadre du produit MULTIRISQUE HOTELIER, indemnisation des dommages provoqués par des infiltrations d’eau accidentelles à travers la toiture ou la couverture du bâtiment.",
            "RECOURS DES VOISINS ET TIERS: Dans le cadre du produit MULTIRISQUE HOTELIER, garantie recours des voisins et tiers : elle couvre la responsabilité de l’assuré vis‑à‑vis des voisins et des tiers en cas de dommages provoqués par un sinistre survenu dans le bâtiment assuré.",
            "FRAIS DE RELOGEMENT DES CLIENTS: Dans le cadre du produit MULTIRISQUE HOTELIER, prise en charge des frais de relogement des clients (par exemple d’un hôtel) lorsque l’établissement est temporairement inhabitable à la suite d’un sinistre.",
            "RENONCIATION A RECOURS : Dans le cadre du produit MULTIRISQUE HOTELIER, renonciation à recours : clause par laquelle l’assureur renonce à exercer un recours contre un tiers responsable, souvent exigée dans les baux commerciaux.",
            "INONDATIONS: Dans le cadre du produit MULTIRISQUE HOTELIER, garantie inondations : elle indemnise les dommages causés par une inondation, une remontée de nappe phréatique ou un ruissellement.",
            "EFFET DES CLIENTS: Dans le cadre du produit MULTIRISQUE HOTELIER, garantie effets des clients : indemnisation des effets personnels des clients (vêtements, bagages) détruits ou volés lors d’un sinistre dans l’établissement.",
            "VOL-CONTENU DES COFFRES FORT: Dans le cadre du produit MULTIRISQUE HOTELIER, garantie vol du contenu des coffres-forts : elle indemnise la disparition d’espèces, de documents ou d’objets de valeur contenus dans un coffre-fort assuré.",
            "VOL-CONTENU DES TIROIRES CAISSES: Dans le cadre du produit MULTIRISQUE HOTELIER, garantie vol du contenu des tiroirs-caisses : elle couvre le vol d’argent ou de valeurs déposés dans les tiroirs-caisses au sein de l’entreprise.",
            "VOL-TRANSPORT DE FONDS: Dans le cadre du produit MULTIRISQUE HOTELIER, garantie vol lors du transport de fonds : elle couvre la disparition d’espèces ou de valeurs lors de leur transport entre les locaux de l’entreprise et la banque.",
            "VOL-DETOURNEMENT DE FOND: Dans le cadre du produit MULTIRISQUE HOTELIER, garantie vol ou détournement de fonds : indemnisation des sommes détournées ou volées par des employés ou des tiers lors de l’exploitation de l’entreprise.",
            "CHOC DE VEHICULES TERRESTRES IDENTIFIES: Dans le cadre du produit MULTIRISQUE HOTELIER, indemnisation des dommages causés aux biens assurés par la collision d’un véhicule terrestre identifié.",
            "FRAIS DE RECHERCHE DES FUITES D EAUX: Dans le cadre du produit MULTIRISQUE HOTELIER, prise en charge des frais engagés pour localiser et diagnostiquer l’origine d’une fuite d’eau responsable d’un sinistre.",
            "R.C DEPOSITAIRE: Dans le cadre du produit MULTIRISQUE HOTELIER, responsabilité civile du dépositaire : indemnisation des dommages ou pertes subis par des biens confiés en dépôt chez l’assuré.",
            "BRIS DE MACHINES: Dans le cadre du produit MULTIRISQUE HOTELIER, cette garantie couvre les risques spécifiques liés à 'BRIS DE MACHINES'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "PERTES EXPLOITATION APRES BRIS DE MACHINES: Dans le cadre du produit MULTIRISQUE HOTELIER, garantie pertes d’exploitation après bris de machines : indemnisation de la perte de chiffre d’affaires résultant de l’arrêt de l’activité à la suite d’un bris de machine couvert.",
            "DETERIORATION MARCHANDISES DANS LES CHAMBRES FRIGORIFIQUES: Dans le cadre du produit MULTIRISQUE HOTELIER, indemnisation des marchandises conservées en chambres frigorifiques détériorées à la suite d’un incendie ou d’une panne de froid.",
            "DETERIORATION MARCHANDISES APRES BRIS DE MACHINES: Dans le cadre du produit MULTIRISQUE HOTELIER, indemnisation des marchandises détériorées à la suite d’un bris de machine (ex. compresseur) dans les installations frigorifiques.",
            "VEHICULES EN STATIONNEMENT: Dans le cadre du produit MULTIRISQUE HOTELIER, garantie véhicules en stationnement : elle couvre les dommages subis par des véhicules stationnés sur le site assuré en cas d’incendie ou d’explosion.",
            "FRAIS DE LUTTE CONTRE L INCENDIE: Dans le cadre du produit MULTIRISQUE HOTELIER, prise en charge des frais engagés pour lutter contre un incendie (extinction, pompiers) et éviter l’aggravation des dommages.",
            "FRAIS DE PEPLACEMENT: Dans le cadre du produit MULTIRISQUE HOTELIER, garantie frais de déplacement : remboursement des frais engagés pour le déplacement des biens ou des personnes suite à un sinistre.",
            "RC PROFESSIONNELLE : DOMMAGES CORPORELS: Dans le cadre du produit MULTIRISQUE HOTELIER, responsabilité civile professionnelle – dommages corporels : indemnisation des blessures causées à des clients ou à des tiers par l’assuré ou ses préposés dans l’exercice de son activité.",
            "RC PROFESSIONNELLE : DOMMAGES MATERIELS: Dans le cadre du produit MULTIRISQUE HOTELIER, responsabilité civile professionnelle – dommages matériels : indemnisation des biens de tiers endommagés par l’assuré dans le cadre de son activité professionnelle.",
            "RC EXPLOITATION : DOMMAGES CORPORELS: Dans le cadre du produit MULTIRISQUE HOTELIER, responsabilité civile exploitation – dommages corporels : couvre les blessures causées aux tiers dans le cadre de l’exploitation d’une entreprise.",
            "RC EXPLOITATION : DOMMAGES MATERIELS: Dans le cadre du produit MULTIRISQUE HOTELIER, responsabilité civile exploitation – dommages matériels : couvre les dégâts causés à des biens de tiers lors de l’exploitation de l’entreprise.",
            "ASSURANCE AUTOMATIQUE DE LA GARANTIE: Dans le cadre du produit MULTIRISQUE HOTELIER, clause d’assurance automatique : extension automatique des garanties existantes à de nouveaux biens ou bâtiments sans déclaration préalable, dans certaines limites.",
            "CLAUSES DE REVERSIBILITE DES EXCEDENTS: Dans le cadre du produit MULTIRISQUE HOTELIER, clause de réversibilité des excédents : disposition permettant la restitution d’une partie des excédents techniques ou financiers au souscripteur en fin d’exercice.",
            "PERTES DES DONNEES ET DE LEURS SUPPORTS DES DONNEES: Dans le cadre du produit MULTIRISQUE HOTELIER, garantie pertes de données et de leurs supports : couverture des coûts de remplacement des supports et de récupération des informations détruites.",
            "FRAIS DE DEPLACEMENT ET DE REPLACEMENT: Dans le cadre du produit MULTIRISQUE HOTELIER, prise en charge des frais de déplacement et de replacement : remboursement des dépenses pour transférer et repositionner les biens lors des travaux de remise en état.",
            "FRAIS DE RECONSTITUTION DE DESSIN ET DE PLANS: Dans le cadre du produit MULTIRISQUE HOTELIER, prise en charge des coûts de reconstitution de dessins et de plans techniques détruits ou endommagés à la suite d’un sinistre.",
            "FUMEE CONSECUTIVE A UN INCENDIE: Dans le cadre du produit MULTIRISQUE HOTELIER, garantie fumée consécutive à un incendie : indemnisation des dommages causés par la fumée et les suies à la suite d’un incendie.",
            "TOUS RISQUES MATERIEL INFORMATIQUE ELECTRONIQUE ET ELECTRIQUE: Dans le cadre du produit MULTIRISQUE HOTELIER, garantie tous risques matériel informatique, électronique et électrique : couverture large des dommages accidentels, vol, incendie et bris affectant les matériels informatiques et électroniques."
        ],
        "produit: MULTIRISQUES PROFESSIONNELLES": [
            "INCENDIE: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, garantie incendie : elle indemnise les dommages causés par le feu, la foudre, l’explosion ou la chute de la foudre aux bâtiments et contenus assurés.",
            "VOL : Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier.",
            "BRIS DE GLACES: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, garantie bris de glaces : elle couvre la réparation ou le remplacement des vitres, vitrines, miroirs ou surfaces en verre endommagés.",
            "DEGATS DES EAUX: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, garantie dégâts des eaux : elle prend en charge les dommages causés par des fuites, ruptures de conduites, débordements ou infiltrations accidentelles d’eau.",
            "TOUTES EXPLOSIONS ET CHUTE DE LA FOUDRE: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, garantie toutes explosions et chute de la foudre : elle couvre les dommages résultant d’une explosion ou d’une chute de foudre sur le bâtiment assuré.",
            "PERTE INDIRECTE: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, garantie perte indirecte : elle couvre les dépenses supplémentaires et pertes financières consécutives à un sinistre (retard de chantier, loyers…).",
            "HONORAIRE EXPERT: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, remboursement des honoraires de l’expert mandaté pour évaluer les dommages à la suite d’un sinistre.",
            "FRAIS DE DEBLAIS ET DE DEMOLITION: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, cette garantie couvre les risques spécifiques liés à 'FRAIS DE DEBLAIS ET DE DEMOLITION'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "CHUTE D APPAREILS DE NAVIGATION AERIENNE: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, indemnisation des dommages causés par la chute d’appareils de navigation aérienne ou de parties de ceux‑ci sur les biens assurés.",
            "VALEUR A NEUF: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, garantie valeur à neuf : elle indemnise le coût de reconstruction ou de remplacement des biens sinistrés sans application de vétusté.",
            "GREVE, EMEUTE ET MOUVEMENTS POPULAIRES: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, cette garantie couvre les risques spécifiques liés à 'GREVE, EMEUTE ET MOUVEMENTS POPULAIRES'. Veuillez consulter le contrat pour connaître le détail des prestations.",
            "TEMPÊTES, OURAGANS, CYCLONES,GRÊLES: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, garantie tempêtes, ouragans, cyclones et grêles : indemnisation des dommages causés par des vents violents ou des chutes de grêle.",
            "PRIVATION DE JOUISSANCE: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, indemnité pour privation de jouissance : elle compense la perte d’usage du logement ou des locaux pendant la remise en état après un sinistre.",
            "TREMBLEMENT DE TERRE: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, garantie tremblement de terre : elle couvre les dommages causés aux biens assurés par un séisme reconnu comme catastrophe naturelle.",
            "DETERIORATION MOBILIERE ET IMMOBILIERE SUITE VOL: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, indemnisation des détériorations mobilières et immobilières causées par une effraction ou un vol (porte fracturée, serrures forcées, mobilier endommagé).",
            "DOMMAGES AUX APPAREILS ELECTRIQUES: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, garantie dommages aux appareils électriques : elle couvre la détérioration des appareils électriques due à un incendie, une surtension ou un court‑circuit.",
            "RECOURS DES LOCATAIRES: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, garantie recours des locataires : elle protège le propriétaire contre les réclamations de ses locataires pour dommages causés à leurs biens lors d’un sinistre touchant l’immeuble.",
            "RECOURS DES VOISINS ET TIERS: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, garantie recours des voisins et tiers : elle couvre la responsabilité de l’assuré vis‑à‑vis des voisins et des tiers en cas de dommages provoqués par un sinistre survenu dans le bâtiment assuré.",
            "INONDATIONS: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, garantie inondations : elle indemnise les dommages causés par une inondation, une remontée de nappe phréatique ou un ruissellement.",
            "RC- DOMMAGES CORPORELS: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, responsabilité civile – dommages corporels : prise en charge des indemnités dues aux tiers pour les blessures ou atteintes corporelles causées par l’assuré.",
            "RC- DOMMAGES MATERIELS: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, responsabilité civile – dommages matériels : indemnisation des dégâts matériels causés à des biens appartenant à des tiers.",
            "RC- INTOXICATION ALIMENTAIRE: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, responsabilité civile – intoxication alimentaire : indemnisation des victimes de toxi‑infections alimentaires causées par des aliments préparés ou vendus par l’assuré.",
            "CHOC DE VEHICULES TERRESTRES IDENTIFIES: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, indemnisation des dommages causés aux biens assurés par la collision d’un véhicule terrestre identifié.",
            "RECOURS DES VOISINS ET TIERS (SUITE D.D.EAUX): Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, garantie recours des voisins et tiers (suite dégâts des eaux) : elle prend en charge les dommages causés aux voisins et aux tiers par un dégât des eaux survenu chez l’assuré.",
            "FUMEE: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, garantie fumée : elle couvre les dommages causés par la fumée provenant d’un incendie accidentel ou soudain.",
            "FRAIS DE RECHERCHE DES FUITES D EAUX: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, prise en charge des frais engagés pour localiser et diagnostiquer l’origine d’une fuite d’eau responsable d’un sinistre.",
            "PRIVATION DE JUISSANCE (SUITE DEGATS DES EAUX ): Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, indemnité pour privation de jouissance à la suite de dégâts des eaux : elle compense la perte d’usage du logement pendant la durée des réparations.",
            "RC PROFESSIONNELLE : DOMMAGES CORPORELS: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, responsabilité civile professionnelle – dommages corporels : indemnisation des blessures causées à des clients ou à des tiers par l’assuré ou ses préposés dans l’exercice de son activité.",
            "RC PROFESSIONNELLE : DOMMAGES MATERIELS: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, responsabilité civile professionnelle – dommages matériels : indemnisation des biens de tiers endommagés par l’assuré dans le cadre de son activité professionnelle.",
            "FRAIS DE DEPLACEMENT ET DE REPLACEMENT: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, prise en charge des frais de déplacement et de replacement : remboursement des dépenses pour transférer et repositionner les biens lors des travaux de remise en état.",
            "FRAIS DE CLOTURE PROVISOIRE ET GARDIENNAGE: Dans le cadre du produit MULTIRISQUES PROFESSIONNELLES, prise en charge des frais de clôture provisoire et de gardiennage pour sécuriser les lieux sinistrés et prévenir les intrusions."
        ],
        "produit: MULTIRISQUES HABITATIONS OCCUPANT": [
            "DEFENSE ET RECOURS: Dans le cadre du produit MULTIRISQUES HABITATIONS OCCUPANT, garantie défense et recours : elle prend en charge les frais de procédure et d’assistance pour défendre l’assuré ou exercer un recours contre un responsable après un sinistre.",
            "INCENDIE: Dans le cadre du produit MULTIRISQUES HABITATIONS OCCUPANT, garantie incendie : elle indemnise les dommages causés par le feu, la foudre, l’explosion ou la chute de la foudre aux bâtiments et contenus assurés.",
            "VOL : Dans le cadre du produit MULTIRISQUES HABITATIONS OCCUPANT, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier.",
            "BRIS DE GLACES: Dans le cadre du produit MULTIRISQUES HABITATIONS OCCUPANT, garantie bris de glaces : elle couvre la réparation ou le remplacement des vitres, vitrines, miroirs ou surfaces en verre endommagés.",
            "DEGATS DES EAUX: Dans le cadre du produit MULTIRISQUES HABITATIONS OCCUPANT, garantie dégâts des eaux : elle prend en charge les dommages causés par des fuites, ruptures de conduites, débordements ou infiltrations accidentelles d’eau.",
            "RESPONSABILITE CIVILE: Dans le cadre du produit MULTIRISQUES HABITATIONS OCCUPANT, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport.",
            "ASSISTANCE DOMICILIAIRE: Dans le cadre du produit MULTIRISQUES HABITATIONS OCCUPANT, garantie assistance domiciliaire : elle organise l’envoi de professionnels (plombier, serrurier, électricien…) et prend en charge certains frais pour les petites interventions urgentes au domicile."
        ],
        "produit: MULTIRISQUES HABITATIONS NON OCCUPANT": [
            "INCENDIE: Dans le cadre du produit MULTIRISQUES HABITATIONS NON OCCUPANT, garantie incendie : elle indemnise les dommages causés par le feu, la foudre, l’explosion ou la chute de la foudre aux bâtiments et contenus assurés.",
            "VOL : Dans le cadre du produit MULTIRISQUES HABITATIONS NON OCCUPANT, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier.",
            "BRIS DE GLACES: Dans le cadre du produit MULTIRISQUES HABITATIONS NON OCCUPANT, garantie bris de glaces : elle couvre la réparation ou le remplacement des vitres, vitrines, miroirs ou surfaces en verre endommagés.",
            "DEGATS DES EAUX: Dans le cadre du produit MULTIRISQUES HABITATIONS NON OCCUPANT, garantie dégâts des eaux : elle prend en charge les dommages causés par des fuites, ruptures de conduites, débordements ou infiltrations accidentelles d’eau.",
            "RESPONSABILITE CIVILE: Dans le cadre du produit MULTIRISQUES HABITATIONS NON OCCUPANT, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport.",
            "ASSISTANCE DOMICILIAIRE: Dans le cadre du produit MULTIRISQUES HABITATIONS NON OCCUPANT, garantie assistance domiciliaire : elle organise l’envoi de professionnels (plombier, serrurier, électricien…) et prend en charge certains frais pour les petites interventions urgentes au domicile."
        ],
        "produit: MULTIRISQUES HABITATIONS OCCUPANT AMICALE": [
            "DEFENSE ET RECOURS: Dans le cadre du produit MULTIRISQUES HABITATIONS OCCUPANT AMICALE, garantie défense et recours : elle prend en charge les frais de procédure et d’assistance pour défendre l’assuré ou exercer un recours contre un responsable après un sinistre.",
            "INCENDIE: Dans le cadre du produit MULTIRISQUES HABITATIONS OCCUPANT AMICALE, garantie incendie : elle indemnise les dommages causés par le feu, la foudre, l’explosion ou la chute de la foudre aux bâtiments et contenus assurés.",
            "VOL : Dans le cadre du produit MULTIRISQUES HABITATIONS OCCUPANT AMICALE, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier.",
            "BRIS DE GLACES: Dans le cadre du produit MULTIRISQUES HABITATIONS OCCUPANT AMICALE, garantie bris de glaces : elle couvre la réparation ou le remplacement des vitres, vitrines, miroirs ou surfaces en verre endommagés.",
            "DEGATS DES EAUX: Dans le cadre du produit MULTIRISQUES HABITATIONS OCCUPANT AMICALE, garantie dégâts des eaux : elle prend en charge les dommages causés par des fuites, ruptures de conduites, débordements ou infiltrations accidentelles d’eau.",
            "RESPONSABILITE CIVILE: Dans le cadre du produit MULTIRISQUES HABITATIONS OCCUPANT AMICALE, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport.",
            "ASSISTANCE DOMICILIAIRE: Dans le cadre du produit MULTIRISQUES HABITATIONS OCCUPANT AMICALE, garantie assistance domiciliaire : elle organise l’envoi de professionnels (plombier, serrurier, électricien…) et prend en charge certains frais pour les petites interventions urgentes au domicile."
        ],
        "produit: MULTIRISQUES HABITATIONS NON OCCUPANT AMICALE": [
            "INCENDIE: Dans le cadre du produit MULTIRISQUES HABITATIONS NON OCCUPANT AMICALE, garantie incendie : elle indemnise les dommages causés par le feu, la foudre, l’explosion ou la chute de la foudre aux bâtiments et contenus assurés.",
            "VOL : Dans le cadre du produit MULTIRISQUES HABITATIONS NON OCCUPANT AMICALE, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier.",
            "BRIS DE GLACES: Dans le cadre du produit MULTIRISQUES HABITATIONS NON OCCUPANT AMICALE, garantie bris de glaces : elle couvre la réparation ou le remplacement des vitres, vitrines, miroirs ou surfaces en verre endommagés.",
            "DEGATS DES EAUX: Dans le cadre du produit MULTIRISQUES HABITATIONS NON OCCUPANT AMICALE, garantie dégâts des eaux : elle prend en charge les dommages causés par des fuites, ruptures de conduites, débordements ou infiltrations accidentelles d’eau.",
            "RESPONSABILITE CIVILE: Dans le cadre du produit MULTIRISQUES HABITATIONS NON OCCUPANT AMICALE, garantie responsabilité civile transporteur : couvre la responsabilité du transporteur en cas de dommages causés aux marchandises transportées ou aux tiers pendant le transport.",
            "ASSISTANCE DOMICILIAIRE: Dans le cadre du produit MULTIRISQUES HABITATIONS NON OCCUPANT AMICALE, garantie assistance domiciliaire : elle organise l’envoi de professionnels (plombier, serrurier, électricien…) et prend en charge certains frais pour les petites interventions urgentes au domicile."
        ],
        "produit: PERTES D EXPLOITATION APRES INCENDIE": [
            "INCENDIE: Dans le cadre du produit PERTES D EXPLOITATION APRES INCENDIE, garantie incendie : elle indemnise les dommages causés par le feu, la foudre, l’explosion ou la chute de la foudre aux bâtiments et contenus assurés.",
            "PERTE EXPLOITATION APRES INCENDIE: Dans le cadre du produit PERTES D EXPLOITATION APRES INCENDIE, garantie perte d’exploitation après incendie : indemnisation de la perte de marge brute résultant d’un arrêt d’activité à la suite d’un incendie."
        ],
        "produit: INCENDIE RISQUES AGRICOLES": [
            "INCENDIE: Dans le cadre du produit INCENDIE RISQUES AGRICOLES, garantie incendie : elle indemnise les dommages causés par le feu, la foudre, l’explosion ou la chute de la foudre aux bâtiments et contenus assurés.",
            "TOUTES EXPLOSIONS ET CHUTE DE LA FOUDRE: Dans le cadre du produit INCENDIE RISQUES AGRICOLES, garantie toutes explosions et chute de la foudre : elle couvre les dommages résultant d’une explosion ou d’une chute de foudre sur le bâtiment assuré.",
            "RECOURS DES VOISINS ET TIERS: Dans le cadre du produit INCENDIE RISQUES AGRICOLES, garantie recours des voisins et tiers : elle couvre la responsabilité de l’assuré vis‑à‑vis des voisins et des tiers en cas de dommages provoqués par un sinistre survenu dans le bâtiment assuré."
        ],
        "produit: INCENDIE AUTRES": [
            "INCENDIE: Dans le cadre du produit INCENDIE AUTRES, garantie incendie : elle indemnise les dommages causés par le feu, la foudre, l’explosion ou la chute de la foudre aux bâtiments et contenus assurés.",
            "VOL : Dans le cadre du produit INCENDIE AUTRES, garantie vol : elle indemnise l’assuré en cas de vol ou tentative de vol des matériels ou équipements de chantier.",
            "DOMMAGES AUX APPAREILS ELECTRIQUES: Dans le cadre du produit INCENDIE AUTRES, garantie dommages aux appareils électriques : elle couvre la détérioration des appareils électriques due à un incendie, une surtension ou un court‑circuit."
        ],
        "produit: INCENDIE LOGEMENTS": [
            "INCENDIE: Dans le cadre du produit INCENDIE LOGEMENTS, garantie incendie : elle indemnise les dommages causés par le feu, la foudre, l’explosion ou la chute de la foudre aux bâtiments et contenus assurés.",
            "DEGATS DES EAUX: Dans le cadre du produit INCENDIE LOGEMENTS, garantie dégâts des eaux : elle prend en charge les dommages causés par des fuites, ruptures de conduites, débordements ou infiltrations accidentelles d’eau.",
            "TOUTES EXPLOSIONS ET CHUTE DE LA FOUDRE: Dans le cadre du produit INCENDIE LOGEMENTS, garantie toutes explosions et chute de la foudre : elle couvre les dommages résultant d’une explosion ou d’une chute de foudre sur le bâtiment assuré.",
            "CHUTE D APPAREILS DE NAVIGATION AERIENNE: Dans le cadre du produit INCENDIE LOGEMENTS, indemnisation des dommages causés par la chute d’appareils de navigation aérienne ou de parties de ceux‑ci sur les biens assurés.",
            "TEMPÊTES, OURAGANS, CYCLONES,GRÊLES: Dans le cadre du produit INCENDIE LOGEMENTS, garantie tempêtes, ouragans, cyclones et grêles : indemnisation des dommages causés par des vents violents ou des chutes de grêle.",
            "TREMBLEMENT DE TERRE: Dans le cadre du produit INCENDIE LOGEMENTS, garantie tremblement de terre : elle couvre les dommages causés aux biens assurés par un séisme reconnu comme catastrophe naturelle.",
            "RECOURS DES VOISINS ET TIERS: Dans le cadre du produit INCENDIE LOGEMENTS, garantie recours des voisins et tiers : elle couvre la responsabilité de l’assuré vis‑à‑vis des voisins et des tiers en cas de dommages provoqués par un sinistre survenu dans le bâtiment assuré.",
            "INONDATIONS: Dans le cadre du produit INCENDIE LOGEMENTS, garantie inondations : elle indemnise les dommages causés par une inondation, une remontée de nappe phréatique ou un ruissellement.",
            "CHOC DE VEHICULES TERRESTRES IDENTIFIES: Dans le cadre du produit INCENDIE LOGEMENTS, indemnisation des dommages causés aux biens assurés par la collision d’un véhicule terrestre identifié."
        ]
    },
    "GROUPE-MALADIE": {
        "produit: SANTE ET PREVOYANCE": [
            "DECES TRIPLEMENT: Dans le cadre du produit SANTE ET PREVOYANCE, garantie décès triplée (transport) : versement d’un capital triple en cas de décès accidentel",
            "DECES: Dans le cadre du produit SANTE ET PREVOYANCE, garantie décès : en cas de décès de l’assuré durant la période couverte, un capital est versé au bénéficiaire désigné.",
            "MALADIE: Dans le cadre du produit SANTE ET PREVOYANCE, garantie frais médicaux : prise en charge des dépenses de santé (consultations, médicaments, hospitalisation) engagées par l’assuré.",
            "INVALIDITE: Dans le cadre du produit SANTE ET PREVOYANCE, garantie invalidité : versement d’une rente ou d’un capital en cas d’invalidité reconnue réduisant la capacité de travail de l’assuré.",
            "INCAPACITE: Dans le cadre du produit SANTE ET PREVOYANCE, garantie incapacité de travail : versement d’indemnités journalières en cas d’incapacité temporaire de l’assuré à exercer son activité professionnelle.",
            "DECES - I.D.T: Dans le cadre du produit SANTE ET PREVOYANCE, garantie décès et invalidité totale et définitive : elle verse le capital prévu au contrat en cas de décès de l’assuré ou d’invalidité définitive totale l’empêchant d’exercer toute activité rémunérée.",
            "EPARGNE: Dans le cadre du produit SANTE ET PREVOYANCE, garantie épargne : elle permet de constituer un capital grâce aux primes versées, capital qui est restitué à l’assuré ou aux bénéficiaires au terme du contrat ou en cas de décès."
        ]
    }
}



def search_tool(query: str, k: int = 3):
    """Recherche des produits d'assurance en fonction de la requête pour le format 'liste de garanties'."""
    
    docs = []
    
    # 1. Création des documents
    for secteur, produits in bh_products.items():
        for nom, garanties in produits.items():
            garanties_text = "\n- ".join(garanties)
            
            text = f"Produit: {nom}\nSecteur: {secteur}\nGaranties:\n- {garanties_text}"
            
            docs.append(Document(
                page_content=text,
                metadata={
                    "secteur": secteur,
                    "produit": nom,
                    "type": "produit_assurance"
                }
            ))

    # 2. Embeddings
    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': False}
    )

    # 3. Base vectorielle
    db = FAISS.from_documents(docs, embedding)

    # 4. Recherche
    results = db.similarity_search(query, k=k)
    output = []
    
    for i, doc in enumerate(results, 1):
        result = {
            "rank": i,
            "produit": doc.metadata['produit'],
            "secteur": doc.metadata['secteur'],
            "content": doc.page_content[:500] + ("..." if len(doc.page_content) > 500 else ""),
            "score": None
        }
        output.append(result)
    
    return output


