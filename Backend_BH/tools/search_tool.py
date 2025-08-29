from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
bh_products = {
    "1/ vie": {
        "amali": {
            "summary": "une épargne pour financer des études ou une rente éducation, avec des garanties en cas de décès ou d’invalidité absolue et définitive avant le terme.",
            "target_audience": "Les personnes souhaitant assurer l’éducation ou le financement de ses enfants avec un âge maximum de souscription fixé à 55 ans pour l’assuré.",
            "key_coverages": [
                "Capital décès : versement d’un montant en cas de décès ou d’I.A.D. de l’assuré avant le terme, représentant 10 fois la prime annuelle.",
                "Capital en cas d’invalidité absolue et définitive (I.A.D.) : prise en charge en cas d’invalidité totale empêchant l’exercice d’une activité rémunérée.",
                "Constitution d’épargne pour financer les études ou une rente éducation.",
                "Garantie de rachat ou de versement d’une rente à 18 ans."
            ],
            "exclusions_limits": ["Suicide conscient de l’assuré (non couvert)."]
        },
        "assur senior": {
            "summary": "Elle offre une protection financière en cas de décès, de maladies graves ou de perte totale de la capacité à accomplir les besoins quotidiens.",
            "target_audience": "Personnes physiques âgées de 55 à 75 ans.",
            "key_coverages": [
                "Versement d’un capital en cas de décès de l’assuré au profit du bénéficiaire.",
                "Versement d’une prestation mensuelle temporaire à l’assuré en cas de perte totale d’autonomie, jusqu’à ses 85 ans, sous réserve qu’il soit en vie à cette date.",
                "Couverture de maladies graves spécifiques, confirmées par des rapports médicaux émis par des médecins spécialisés."
            ],
            "exclusions_limits": [
                "La couverture ne s’applique pas en cas d’accident ou de maladie non listée comme maladie grave dans le contrat.",
                "La couverture n’est pas valide si le dossier médical n’est pas complété dans le délai imparti ou si les informations fournies ne correspondent pas à la documentation médicale.",
                "La couverture ne s’applique pas pendant la période de carence ou « non-souscription » entre l’adhésion et le début des prestations, sauf en cas de renouvellement automatique."
            ]
        },
        "dhamen": {},
        "dhamen compte": {},
        "dhamen retraite": {},
        "hana": {},
        "horizon": {
            "summary": "Un contrat d'assurance vie qui permet de constituer une épargne retraite par des versements périodiques ou libres, offrant un capital ou une rente à l'âge de la retraite. Propose également des garanties facultatives décès et invalidité avec remboursement de frais médicaux.",
            "target_audience": "Personnes actives âgées de 18 à 60 ans planifiant leur retraite, salariés et indépendants souhaitant compléter leurs revenus de retraite au-delà du régime obligatoire.",
            "key_coverages": [
                "Constitution d'épargne retraite avec taux minimum garanti.",
                "Capital décès avant l'âge de retraite.",
                "Garantie facultative invalidité absolue et définitive.",
                "Indemnités temporaires en cas d'incapacité de travail.",
                "Remboursement frais d'hospitalisation (jusqu'à 5 000 DT/an).",
                "Doublement/triplement du capital en cas de décès accidentel."
            ],
            "exclusions_limits": [
                "Suicide conscient.",
                "Accidents volontaires.",
                "Événements nucléaires.",
                "Guerre/terrorisme (sauf légitime défense/devoir professionnel).",
                "Accidents aéronautiques/compétitions automobiles.",
                "Maladies antérieures à la souscription.",
                "Affections psychiatriques.",
                "Congés de maternité pour garanties incapacité.",
                "Hospitalisation esthétique/psychiatrique."
            ]
        },
        "horizon +": {},
        "indemnite de depart a la retaite": {},
        "rahma": {
            "summary": "Contrat d'assurance vie garantissant le versement d'un capital en cas de décès ou d'invalidité absolue et définitive de l'assuré.",
            "target_audience": "Personnes physiques jusqu'à 70 ans (garanties facultatives jusqu'à 60 ans).",
            "key_coverages": [
                "Capital décès ou invalidité absolue et définitive.",
                "Doublement ou triplement du capital en cas d'accident (facultatif).",
                "Exonération des primes en cas d'incapacité de travail > 90 jours (facultatif)."
            ],
            "exclusions_limits": []
        },
        "temporiare deces en couverture des prets": {
            "summary": "Assurance temporaire décès spécialement conçue pour couvrir les montants de prêt restants en cas de décès ou d'invalidité absolue et définitive de l'emprunteur. Verse le solde restant du prêt à l'organisme prêteur au décès/invalidité de l'assuré.",
            "target_audience": "Emprunteurs âgés jusqu'à 75 ans à la fin du contrat (couverture invalidité s'arrête à 65 ans).",
            "key_coverages": [
                "Capital décès: verse le solde restant du prêt au prêteur.",
                "Couverture invalidité absolue et définitive (identique au décès).",
                "Couverture invalidité cesse à 65 ans, âge max 75 ans à la fin du contrat.",
                "Arrêt du paiement des primes au décès/invalidité.",
                "Remboursement anticipé du prêt permet remboursement de prime.",
                "Modification du contrat autorisée pour changements de prêt."
            ],
            "exclusions_limits": [
                "Suicide conscient.",
                "Actes intentionnels de l'assuré/bénéficiaire.",
                "Conditions préexistantes non déclarées.",
                "Explosions/radiations nucléaires.",
                "Guerre, émeutes, terrorisme (sauf légitime défense/devoir professionnel).",
                "Accidents aériens/maritimes en compétition.",
                "Courses automobiles/rallyes."
            ]
        }
    },
    "2/santé": {
        "assurance groupe maladie": {
            "summary": "Contrat d'assurance collective couvrant les risques de santé, décès et invalidité pour le personnel d'entreprise.",
            "target_audience": "Personnel d'entreprise âgé de plus de 18 ans, actif au travail, jusqu'à 60 ans.",
            "key_coverages": [
                "Capital décès avec majoration charges de famille.",
                "Invalidité absolue et définitive.",
                "Décès accidentel (capital supplémentaire).",
                "Incapacité temporaire de travail.",
                "Invalidité permanente (totale/partielle).",
                "Frais médicaux et pharmaceutiques.",
                "Hospitalisation.",
                "Chirurgie.",
                "Maternité.",
                "Soins dentaires.",
                "Optique/Prothèses."
            ],
            "exclusions_limits": [
                "Suicide conscient.",
                "Accidents volontaires.",
                "Guerre/émeutes.",
                "Sports à risque.",
                "Malformations congénitales.",
                "Soins esthétiques.",
                "Cures thermales.",
                "Voyages hors Tunisie (limitations)."
            ]
        }
    },
    "3/transport": {
        "assurance des marchandises transportées par voie aerienne": {},
        "assurance des marchandises transportées par voie terrestre": {},
        "assurance maritime sur corps de plaisance": {},
        "assurance maritime sur faculte": {},
        "assurance sur corps de navires de peche": {},
        "corps de tous navires": {
            "summary": "Police d'assurance couvrant les dommages et pertes subis par les navires commerciaux dus aux fortunes de mer.",
            "target_audience": "Propriétaires et armateurs de navires commerciaux (à l'exclusion des navires de pêche, de plaisance, des voiliers et des navires à moteur auxiliaire).",
            "key_coverages": [
                "Dommages par tempête, naufrage, échouement, abordage, jet, feu, explosion, pillage.",
                "Baraterie de patron, fautes du capitaine et équipage.",
                "Fautes des préposés terrestres (sans dol/fraude).",
                "Vice caché du corps ou appareils moteurs.",
                "Recours de tiers pour abordage.",
                "Avaries communes et frais de sauvetage.",
                "Dommages par ancres et chaînes."
            ],
            "exclusions_limits": [
                "Dol et fraude du capitaine.",
                "Violation de blocus, contrebande.",
                "Vice propre, vétusté, piqûre des vers.",
                "Frais d'hivernage, quarantaine.",
                "Faits de l'équipage à terre.",
                "Recours liés au chargement.",
                "Accidents corporels.",
                "Risques de guerre, hostilités, captures.",
                "Grèves, émeutes, mouvements populaires.",
                "Certaines navigations spéciales (zones polaires, etc.)."
            ]
        },
        "police francaise corps de tous navires": {
            "summary": "Police d'assurance couvrant les dommages, pertes, recours de tiers et dépenses résultant de fortunes de mer et d'accidents maritimes pour navires commerciaux.",
            "target_audience": "Propriétaires et armateurs de navires commerciaux (à l'exclusion des navires de pêche, de plaisance, des voiliers et des navires à moteur auxiliaire).",
            "key_coverages": [
                "Dommages et pertes du navire (limite : valeur agréée).",
                "Recours de tiers pour abordage et heurts (limite : valeur agréée).",
                "Contribution aux avaries communes.",
                "Indemnités d'assistance et frais de sauvetage.",
                "Frais de procédure avec accord des assureurs.",
                "Dépenses préventives pour préserver le navire.",
                "Dommages résultant de décisions d'autorités publiques anti-pollution."
            ],
            "exclusions_limits": [
                "Violation de blocus, contrebande, amendes.",
                "Faute intentionnelle de l'assuré ou personnel de direction.",
                "Vice propre, vétusté.",
                "Destruction d'épave, quarantaine, immobilisation.",
                "Dommages corporels.",
                "Risques de guerre, hostilités, terrorisme politique.",
                "Captures, saisies par autorités.",
                "Grèves, émeutes, piraterie politique.",
                "Risques nucléaires.",
                "Recours environnementaux et pollution.",
                "Navigations spéciales sans déclaration."
            ]
        }
    },
    "4/IARD": {
        "assurance multirisque informatique": {},
        "carte yasmine": {},
        "assurance assistance de la protection juridique et lettre CGA 27 juillet 2016": {},
        "assurance bris de glaces": {
            "summary": "couvre les dommages causés aux glaces, verres, marbres et autres objets similaires contre le bris.",
            "target_audience": "couvre les dommages causés aux glaces, verres, marbres et autres objets similaires contre le bris.",
            "key_coverages": [
                "Bris de glaces, verres, marbres par fait de l'assuré, préposés ou tiers.",
                "Bris par imprudence ou malveillance de tiers.",
                "Bris par tassement d'immeubles ou jet d'objets.",
                "Bris par suite de rixe.",
                "Effets de chaleur artificielle, gaz et électricité.",
                "Inscriptions, décorations, gravures (stipulation spéciale).",
                "Dégâts aux devantures et marchandises (stipulation spéciale)."
            ],
            "exclusions_limits": [
                "Dommages lors de travaux (autres que nettoyage), pose, dépose, transfert.",
                "Défaut d'entretien des encadrements.",
                "Rayures, ébrèchements, écaillements.",
                "Incendie, explosion.",
                "Grèves, émeutes (rachetable).",
                "Tempêtes, ouragans (rachetable).",
                "Vols, tentatives de vol (rachetable).",
                "Chute de grêle (rachetable).",
                "Tremblements de terre, inondations.",
                "Dommages nucléaires.",
                "Franchissement du mur du son."
            ]
        },
        "assurance bris de machines": {
            "summary": "couvre les machines et installations contre les dommages matériels survenus de manière soudaine et imprévisible.",
            "target_audience": "Entreprises et industriels possédant des machines et installations.",
            "key_coverages": ["Entreprises et industriels possédant des machines et installations."],
            "exclusions_limits": [
                "Dommages pendant montage/essais.",
                "Outils interchangeables (forets, matrices, etc.).",
                "Bandes transporteuses, pneumatiques, cordes.",
                "Combustibles, lubrifiants, filtres.",
                "Usure normale.",
                "Vol, tentative de vol.",
                "Incendie, explosion, foudre.",
                "Surcharges intentionnelles.",
                "Dommages indirects.",
                "Catastrophes naturelles.",
                "Guerre, terrorisme, grèves.",
                "Dommages nucléaires."
            ]
        },
        "assurance contre le vol": {
            "summary": "Cette assurance protège contre différents types de vols incluant les marchandises en magasins, les biens mobiliers dans les habitations, le contenu des coffres-forts et les vols sur la personne.",
            "target_audience": "Professionnels et particuliers possédant des locaux commerciaux, habitations, coffres-forts ou transportant des fonds.",
            "key_coverages": [
                "Vol avec effraction des marchandises en magasins et locaux professionnels.",
                "Vol avec effraction des biens mobiliers dans les habitations.",
                "Vol du contenu des coffres-forts et chambres fortes.",
                "Vol sur la personne et perte par cas de force majeure.",
                "Détournements d'espèces, billets de banque, titres et valeurs par les préposés.",
                "Extensions possibles : détériorations causées par les voleurs, reconstitution d'archives."
            ],
            "exclusions_limits": [
                "Vol avec effraction des marchandises en magasins et locaux professionnels.",
                "Vol avec effraction des biens mobiliers dans les habitations.",
                "Vol du contenu des coffres-forts et chambres fortes.",
                "Vol sur la personne et perte par cas de force majeure.",
                "Détournements d'espèces, billets de banque, titres et valeurs par les préposés.",
                "Extensions possibles : détériorations causées par les voleurs, reconstitution d'archives."
            ]
        },
        "assurance dégats des eaux": {
            "summary": "couvre les dommages causés par les fuites d'eau accidentelles provenant des installations hydrauliques intérieures, chauffage, gouttières et appareils à effet d'eau.",
            "target_audience": "Propriétaires et locataires de biens immobiliers (habitations, locaux professionnels).",
            "key_coverages": [
                "Dommages aux biens immobiliers et mobiliers de l'assuré.",
                "Dommages aux marchandises professionnelles.",
                "Privation de jouissance et perte de loyers.",
                "Honoraires d'expert (5% de l'indemnité).",
                "Responsabilité civile (recours propriétaire, locataires, voisins).",
                "Extensions optionnelles : réparations gel, infiltrations pluie/grêle toitures."
            ],
            "exclusions_limits": [
                "Défaut d'entretien.",
                "Glissements/affaissements de terrain.",
                "Coût de l'eau perdue.",
                "Pertes d'exploitation/chômage.",
                "Bâtiment non surveillé/abandonné.",
                "Guerre civile, grèves, émeutes.",
                "Catastrophes naturelles.",
                "Infiltrations terrasses/toits-terrasses.",
                "Inondations, refoulements égouts.",
                "Humidité naturelle, condensation.",
                "Manuscrits et documents."
            ]
        },
        "assurance incendie": {
            "summary": "garantit l'assuré contre les dommages causés par l'incendie, la foudre et les explosions sur les biens immobiliers et mobiliers.",
            "target_audience": "Propriétaires, locataires, fermiers, métayers et exploitants de biens immobiliers et mobiliers.",
            "key_coverages": [
                "Incendie des biens immobiliers et mobiliers.",
                "Responsabilité locative et recours des voisins/tiers.",
                "Foudre et explosions.",
                "Privation de jouissance et perte de loyers.",
                "Extensions possibles : tempête, grêle, choc de véhicules, dommages électriques.",
                "Frais de déblais et démolition (jusqu'à 5% de l'indemnité)."
            ],
            "exclusions_limits": [
                "Dommages intentionnels ou corporels.",
                "Guerre étrangère et civile.",
                "Terrorisme, sabotage, émeutes.",
                "Catastrophes naturelles (volcan, tremblement de terre, inondation).",
                "Effets nucléaires et radioactivité.",
                "Vol pendant incendie (sauf preuve contraire).",
                "Destruction d'espèces monétaires et titres."
            ]
        },
        "assurance individuelle contre les accidents corporels": {
            "summary": "couvrant les conséquences d'accidents corporels non intentionnels survenus dans la vie professionnelle ou privée. Garantit le versement de capitaux et indemnités en cas de décès, d'incapacité permanente ou temporaire, ainsi que le remboursement des frais de traitement.",
            "target_audience": "Personnes physiques (âge non spécifié dans le document) souhaitant se protéger contre les accidents corporels dans leur vie professionnelle et privée.",
            "key_coverages": [
                "Décès (capital versé si décès dans les 18 mois suivant l'accident).",
                "Invalidité totale ou partielle permanente (selon barème d'incapacité).",
                "Incapacité temporaire (indemnité journalière max 300 jours).",
                "Frais de traitement (médicaux, pharmaceutiques, hospitalisation).",
                "Assurance recours (réclamation aux responsables, frais jusqu'à 500 DT).",
                "Couverture mondiale (90 jours max hors Tunisie)."
            ],
            "exclusions_limits": [
                "Guerre, terrorisme, émeutes.",
                "Faute intentionnelle, ivresse, drogues.",
                "Sports professionnels, compétitions automobiles, sports aériens.",
                "Motocyclette >50cm³, escalade, spéléologie.",
                "Service militaire, manipulation d'engins de guerre.",
                "Maladies (syncope, épilepsie, affections cardiaques).",
                "Infirmités antérieures non déclarées.",
                "Catastrophes naturelles."
            ]
        },
        "assurance pertes d'exploitation apres incendie": {},
        "multirisque habitation": {
            "summary": "Ce contrat couvre les dommages aux biens immobiliers et mobiliers, ainsi que les responsabilités civiles liées à l'habitation. Il inclut également des garanties pour les pertes de loyers et les recours des locataires ou voisins.",
            "target_audience": "Propriétaires ou locataires en Tunisie, sans restriction d'âge spécifique, mais généralement destiné aux adultes responsables d'un logement.",
            "key_coverages": [
                "Biens immobiliers : Couverture de l’ensemble de la construction, annexes, dépendances, et parties communes en cas d’immeuble collectif, contre les dommages spécifiés.",
                "Mobilier : Protection du mobilier meublant, appareils ménagers, vêtements, effets personnels, bijoux, tableaux, collections, avec une limite d’indemnisation de 30% du capital assuré pour ces objets.",
                "Embellissements : Garantie pour les travaux d’embellissement réalisés aux frais de l’occupant, comme peintures ou décorations.",
                "Perte de loyers : Indemnisation en cas de sinistre empêchant la perception des loyers ou engendrant la responsabilité des locataires envers le propriétaire.",
                "Privation de jouissance : Couverture des situations où l’occupant se voit privé de l’usage de son logement suite à un sinistre.",
                "Responsabilité locative : Responsabilité du locataire envers le propriétaire, notamment en application de la loi."
            ],
            "exclusions_limits": [
                "Exclusions liées au comportement de l'Assuré Fraude, faute intentionnelle ou dolosive de l'Assuré. Négligence grave ou complicité dans la survenance du sinistre.",
                "Catastrophes naturelles et événements majeurs Tremblements de terre, séismes. Éruptions volcaniques, raz-de-marée. Inondations (sauf si couverture spécifique ajoutée).",
                "Risques politiques et conflits Guerre étrangère ou civile. Actes de terrorisme, sabotage. Émeutes, mouvements populaires.",
                "Risques technologiques et nucléaires Dommages dus à la radioactivité. Explosions ou accidents nucléaires.",
                "Biens non couverts Clôtures non intégrées aux bâtiments. Véhicules automobiles (couverts par l'assurance auto obligatoire). Bateaux de plaisance.",
                "Situations spécifiques Défaut d'entretien prolongé du logement. Sinistres survenus pendant des travaux non déclarés. Valeur locative des locaux vacants (non indemnisée).",
                "Limitations sur les objets de valeur Bijoux, pierres précieuses, œuvres d'art (plafonnés à 30% du capital mobilier)."
            ]
        },
        "multirisuqe professionnelle des commerçants, artisans et prestataires de services": {
            "summary": "Contrat d’assurance destiné à protéger les professionnels contre les dommages matériels, incendie, vol, dégâts des eaux, bris de glace et responsabilité civile liés à leur activité professionnelle. Il offre une protection complète sur leurs locaux, contenus et responsabilités encourues dans leur exploitation.",
            "target_audience": "Commerçants, artisans et prestataires de services exerçant une activité professionnelle, propriétaires ou locataires de locaux professionnels, sans limite d’âge spécifique mentionnée.",
            "key_coverages": [
                "Incendie, explosions, foudre.",
                "Vol et vandalisme.",
                "Responsabilité civile exploitation.",
                "Dégâts des eaux.",
                "Bris de glaces.",
                "Défense et recours.",
                "Protection des locaux professionnels et du contenu (mobilier, matériel, marchandises, fonds et valeurs)."
            ],
            "exclusions_limits": [
                "Dommages dus à la guerre, actes terroristes.",
                "Dommages intentionnels ou en état d’ivresse.",
                "Dommages nucléaires.",
                "Dommages corporels exclus.",
                "Explosions se produisant dans des dépôts d’explosifs.",
                "Vols commis par complicité interne (famille, employés).",
                "Dommages causés par tempêtes exceptionnelles, inondations et marées.",
                "Dommages électriques hors incendie.",
                "Matériaux légers non garantis.",
                "Locaux non fermés ou en construction non close."
            ]
        },
        "perte d'exploitation apres bris de machines": {},
        "responsabilité civiles": {
            "summary": "Ce contrat garantit la responsabilité civile de l’assuré en couvrant les conséquences pécuniaires des dommages corporels, matériels et immatériels causés à des tiers dans le cadre de son activité professionnelle. La couverture inclut également certains dommages accessoires comme les incendies ou explosions consécutifs à un accident garanti.",
            "target_audience": "Toute personne physique ou morale exerçant une activité professionnelle, y compris les dirigeants, associées et employés, sans restriction d’âge spécifique.",
            "key_coverages": [
                "Responsabilité civile professionnelle couvrant les dommages causés à des tiers (corporels, matériels, immatériels).",
                "Dommages accessoires liés à des incendies ou explosions.",
                "Prise en charge des frais de procès et assistance juridique.",
                "Couvrant les faits générateurs dans la période de garantie."
            ],
            "exclusions_limits": [
                "Dommages intentionnels.",
                "Dommages aux membres de la famille ou salariés.",
                "Dommages aux biens détenus.",
                "Intoxications alimentaires.",
                "Pollution.",
                "Troubles de voisinage non liés à un accident.",
                "Exclusions liées à certains secteurs (mines, industrie pétrolière, aéronautique).",
                "Dommages liés à la guerre, actes terroristes, catastrophes naturelles.",
                "Dommages dus à l’usage des véhicules terrestres à moteur.",
                "Exclusion des dommages professionnels inévitables liés à la nature du travail."
            ]
        },
        "notice d'information carte bh gold nationale et internationale": {}
    },
    "5/ engineering": {
        "assurance tous risque montage": {
            "summary": "Ce contrat couvre les dommages accidentels aux biens assurés pendant les travaux de montage, ainsi que la responsabilité civile de l’assuré pour les dommages matériels et corporels causés à des tiers durant l’exécution des travaux. Il prend également en charge les frais liés au démontage et déblaiement après sinistre.",
            "target_audience": "Personnes physiques ou morales réalisant des travaux de montage, incluant les souscripteurs, leurs représentants et collaborateurs.",
            "key_coverages": [
                "Dommages accidentels, pertes, vols des machines et installations lors du montage et de la période de maintenance.",
                "Responsabilité civile pour dommages corporels et matériels causés à des tiers.",
                "Frais de procédure et défense juridique.",
                "Remboursement des frais de déblaiement et enlèvement des débris."
            ],
            "exclusions_limits": [
                "Pertes immatérielles (amendes, pénalités, pertes d’usage).",
                "Dommages liés aux guerres, actes terroristes, radiations nucléaires.",
                "Dommages intentionnels.",
                "Pollution environnementale.",
                "Dommages liés à inobservation des règles de l’art.",
                "Biens non couverts (avions, véhicules à moteur assurés légalement).",
                "Matériels détériorés par vétusté, usure, corrosion.",
                "Vols internes (famille, employés).",
                "Certains dommages liés aux engins ou machines de chantier."
            ]
        },
        "contrat d'assurance unique par chantier de la responsabilité decennale dans le domaine de la construction": {
            "summary": "Ce contrat d’assurance couvre la responsabilité décennale pour des dommages matériels survenus durant la construction, notamment ceux liés au gros œuvre, pour une période de 10 ans après la réception. Il précise les obligations des acteurs, les modalités de déclaration des travaux et des sinistres, et exclut certains dommages comme ceux dus à la force majeure ou aux tiers.",
            "target_audience": "les intervenants dans le secteur de la construction, qui souhaitent être couvert contre les dommages liés à la responsabilité décennale durant et après la réalisation de leurs ouvrages.",
            "key_coverages": [
                "Responsabilité pour les dommages matériels affectant la stabilité et la solidité de l’ouvrage.",
                "Indemnisation des frais de remise en état des dommages matériels à l’ouvrage, dus au gros-œuvre.",
                "Garantie pendant la période de 10 ans à compter de la réception de l’ouvrage, couvrant les désordres liés à la responsabilité décennale.",
                "Prise en charge des travaux de démolition et de déblaiement nécessaires suite à un sinistre.",
                "Couverture des dommages causés par la menace d’effondrement du gros-œuvre.",
                "Protection contre les risques de responsabilité liés à la stabilité ou la solidité de l’ouvrage."
            ],
            "exclusions_limits": [
                "Les dommages résultant des causes suivantes : Force majeure (cyclone, inondation, tremblement de terre).",
                "Faille due à la faute d’un tiers ou à l’application d’instructions contraires du maître d’ouvrage.",
                "Les dommages causés par : Incendie ou explosion.",
                "Mouvement du sol provenant d’exploitations minières.",
                "Effets directs ou indirects d’explosion, radiations, radioactivité, ou transmutation nucléaire.",
                "Fait de guerre étrangère, guerre civile, actes de terrorisme, sabotage, rébellion, révolte, émeute ou confiscation par une autorité.",
                "Les dommages spécifiques non garantis : Dommages affectant uniquement la partie second-œuvre ou équipements non liés au gros-œuvre.",
                "Dommages dus à l’entretien, à l’usure normale ou à un usage non approprié de l’ouvrage.",
                "Modifications ultérieures ou réparations non prévues lors de la réception.",
                "Dommages liés à des réserves techniques non levées lors de la réception.",
                "Les dommages hors champ de la responsabilité décennale ou non couverts par la loi."
            ]
        },
        "engins de chantiers": {
            "summary": "Ce contrat couvre les engins et machines de chantier contre les dommages matériels soudains et imprévus nécessitant réparation ou remplacement. La garantie s’applique sur chantier ou au parc, sous réserve des exclusions prévues.",
            "target_audience": "Entreprises de construction, BTP et exploitants de chantiers possédant des engins lourds (adultes professionnels, sociétés du secteur).",
            "key_coverages": [
                "Dommages matériels dus à accidents fortuits (opération, chargement/déchargement, montage/démontage).",
                "Incendie, explosion, foudre, vol ou tentative de vol.",
                "Erreurs de montage ou négligence du conducteur.",
                "Catastrophes naturelles : ouragans, tempêtes, inondations, tremblements de terre, glissements de terrain.",
                "Collisions, chutes, renversements.",
                "Tout autre accident non exclu."
            ],
            "exclusions_limits": [
                "Usure normale, vétusté, corrosion, défauts matériels ou vices de construction.",
                "Pannes mécaniques/électriques, manque d’huile/eau, graissage défectueux.",
                "Dommages existant avant la souscription.",
                "Dommages garantis par constructeurs/fournisseurs.",
                "Véhicules immatriculés pour route publique (sauf usage exclusivement chantier).",
                "Consommables (carburants, lubrifiants, batteries, pièces interchangeables non métalliques).",
                "Guerre, guerre civile, rébellion, terrorisme.",
                "Dommages nucléaires ou radioactifs.",
                "Pertes d’exploitation ou chômage."
            ]
        },
        "tous risques chantier": {
            "summary": "Ce contrat couvre les dommages accidentels subis par les biens d’un chantier (ouvrages, matériaux, équipements) ainsi que la responsabilité civile de l’assuré pour les dommages causés à des tiers. La couverture s’étend pendant la période de construction et éventuellement la période de maintenance.",
            "target_audience": "Maîtres d’ouvrage, entreprises de construction, promoteurs immobiliers et sociétés du BTP responsables de projets (adultes professionnels).",
            "key_coverages": [
                "Dommages matériels accidentels aux biens du chantier (ouvrages, matériaux, équipements).",
                "Pertes et vols sur site.",
                "Frais de déblaiement après sinistre.",
                "Dommages pendant la période de maintenance dus à négligence ou fausse manœuvre.",
                "Responsabilité civile pour dommages corporels, matériels et frais de procédure liés à l’exécution des travaux."
            ],
            "exclusions_limits": [
                "pertes immatérielles (retards, chômage, privation de jouissance).",
                "guerre, émeutes, terrorisme.",
                "risques nucléaires.",
                "dommages intentionnels.",
                "pollution et nuisances environnementales.",
                "vices connus avant souscription.",
                "Exclusions particulières : véhicules soumis à assurance obligatoire, avions, navires, documents, espèces et valeurs, erreurs de conception ou malfaçons, usure et corrosion, pannes mécaniques/électriques des engins de chantier, vols commis par salariés, dommages dus à réparations provisoires ou expérimentations, obligations contractuelles non imposées par la loi."
            ]
        }
    },
    "6/automobile": {
        "assurance des vehicules terrestres à moteurs": {}
    }
}


# 1. Créer une liste de documents
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document

# Your bh_products dictionary remains the same...



def search_tool(query: str, k: int = 3):
    """Recherche des produits d'assurance en fonction de la requête.
    
    Args:
        query: La requête de recherche textuelle selon le raisonnement que vous déja fait.
        k: Nombre de résultats à retourner (par défaut 3)
        
    Returns:
        Une liste de dictionnaires contenant les résultats
    """
    # 1. Création des documents avec gestion des champs manquants
    docs = []
    for secteur, produits in bh_products.items():
        for nom, infos in produits.items():
            # Gestion des champs optionnels
            summary = infos.get('summary', 'Aucun résumé disponible')
            target = infos.get('target_audience', 'Public cible non spécifié')
            
            text = f"Produit: {nom}\nSecteur: {secteur}\nRésumé: {summary}\nPublic cible: {target}"
            
            # Ajout des garanties si disponibles
            if 'key_coverages' in infos and infos['key_coverages']:
                text += f"\nGaranties principales:\n- " + "\n- ".join(infos['key_coverages'])
                
            # Ajout des exclusions si disponibles
            if 'exclusions_limits' in infos and infos['exclusions_limits']:
                text += f"\nExclusions:\n- " + "\n- ".join(infos['exclusions_limits'])
                
            docs.append(Document(
                page_content=text, 
                metadata={
                    "secteur": secteur, 
                    "produit": nom,
                    "type": "produit_assurance"
                }))

    # 2. Initialisation du modèle d'embedding gratuit
    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},  # Utilisez 'cuda' si vous avez un GPU
        encode_kwargs={'normalize_embeddings': False}
    )

    # 3. Création de la base vectorielle
    db = FAISS.from_documents(docs, embedding)

    results = db.similarity_search(query, k=k)
    output = []
    
    for i, doc in enumerate(results, 1):
        result = {
            "rank": i,
            "produit": doc.metadata['produit'],
            "secteur": doc.metadata['secteur'],
            "content": doc.page_content[:500] + ("..." if len(doc.page_content) > 500 else ""),
            "score": None  # FAISS ne retourne pas de score par défaut
        }
        output.append(result)
    
    return output

# Exemple d'utilisation