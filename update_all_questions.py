import json
import os

updates = {
    "EXCEL-N1-CALCUL-C21-Q07": {
        "question": "Que signifie le symbole #DIV/0! dans une cellule ?",
        "reponses": {
            "A": "La formule tente de diviser un nombre par zéro.",
            "B": "La cellule contient du texte au lieu d'un nombre.",
            "C": "L'espace disponible dans la colonne est insuffisant.",
            "D": "Une erreur de syntaxe empêche l'exécution."
        },
        "reponseCorrecte": "A",
        "feedbackPedagogique": "L'erreur #DIV/0! apparaît spécifiquement lorsqu'une division par zéro est demandée."
    },
    "EXCEL-N1-CALCUL-C22-Q06": {
        "question": "Quelle formule native permet d'additionner rapidement une plage verticale de cellules (ex: A1 à A10) ?",
        "reponses": {
            "A": "=TOTAL(A1:A10)",
            "B": "=AJOUT(A1:A10)",
            "C": "=SOMME(A1:A10)",
            "D": "=PLUS(A1:A10)"
        },
        "reponseCorrecte": "C",
        "feedbackPedagogique": "La fonction =SOMME() est la fonction standard native d'Excel pour additionner plusieurs valeurs ou plages."
    },
    "EXCEL-N1-ENV-C01-Q01": {
        "question": "Quelle est l'approche la plus directe pour ouvrir le menu d'ouverture d'un fichier existant ?",
        "reponses": {
            "A": "Cliquer sur l'onglet Fichier, puis Ouvrir.",
            "B": "Cliquer sur l'onglet Affichage, puis Nouvel Onglet.",
            "C": "Cliquer sur Insertion, puis Fichier existant.",
            "D": "Cliquer sur Formules, puis Gestionnaire de fichiers."
        },
        "reponseCorrecte": "A",
        "feedbackPedagogique": "Le menu Fichier (Backstage) regroupe toutes les opérations principales de gestion des documents."
    },
    "EXCEL-N1-ENV-C02-Q02": {
        "question": "Quel raccourci clavier universel permet d'enregistrer instantanément son document actif ?",
        "reponses": {
            "A": "Ctrl + E",
            "B": "Ctrl + S (Save)",
            "C": "Ctrl + P",
            "D": "Ctrl + R"
        },
        "reponseCorrecte": "B",
        "feedbackPedagogique": "Le raccourci Ctrl + S déclenche la sauvegarde du document actif."
    },
    "EXCEL-N1-ENV-C05-Q03": {
        "question": "Comment figer la première ligne (les en-têtes) pour qu'elle reste visible en faisant défiler le tableau ?",
        "reponses": {
            "A": "Onglet 'Affichage' > 'Figer les volets' > 'Figer la ligne supérieure'.",
            "B": "Onglet 'Données' > 'Verrouiller'.",
            "C": "Onglet 'Mise en page' > 'Bloquer les marges'.",
            "D": "Clic droit sur la ligne > 'Cacher'."
        },
        "reponseCorrecte": "A",
        "feedbackPedagogique": "L'option Figer les volets dans l'onglet Affichage est spécialement conçue pour maintenir les en-têtes visibles."
    },
    "EXCEL-N1-ENV-C13-Q04": {
        "question": "Comment ajuster la largeur d'une colonne pour qu'elle s'adapte automatiquement au contenu le plus long ?",
        "reponses": {
            "A": "En double-cliquant sur la bordure droite de l'en-tête de la colonne (ex. entre A et B).",
            "B": "En cliquant-glissant la bordure depuis la cellule la plus longue.",
            "C": "En fusionnant la cellule longue avec celle d'à côté.",
            "D": "Il faut aller dans les options globales d'Excel."
        },
        "reponseCorrecte": "A",
        "feedbackPedagogique": "Le double-clic sur la bordure d'en-tête est l'astuce la plus rapide pour déclencher l'ajustement automatique."
    },
    "EXCEL-N1-ENV-C15-Q05": {
        "question": "Lorqu'on fait Clic droit > 'Insérer' sur une cellule isolée, que propose Excel ?",
        "reponses": {
            "A": "De supprimer la ligne correspondante.",
            "B": "De décaler les cellules existantes vers le bas ou vers la droite.",
            "C": "De dupliquer la feuille entière.",
            "D": "De réinitialiser la couleur de la cellule."
        },
        "reponseCorrecte": "B",
        "feedbackPedagogique": "L'insertion d'une cellule isolée oblige Excel à déplacer le reste des données environnantes sans toucher aux lignes."
    },
    "EXCEL-N1-GDONNEES-C39-Q09": {
        "question": "Comment trier rapidement une colonne de texte par ordre alphabétique (de A à Z) ?",
        "reponses": {
            "A": "Via l'onglet 'Données', cliquer sur le bouton 'Trier de A à Z'.",
            "B": "Via l'onglet 'Insertion', cliquer sur 'Ordre'.",
            "C": "Via l'onglet 'Formules', insérer la fonction =ALPHABETIQUE().",
            "D": "Excel trie toujours par ordre alphabétique implicitement."
        },
        "reponseCorrecte": "A",
        "feedbackPedagogique": "Les boutons de tri rapide A-Z ou Z-A se trouvent très facilement dans l'onglet Données."
    },
    "EXCEL-N1-GDONNEES-C41-Q10": {
        "question": "Visuellement, à quoi correspond un graphique de type 'Histogramme' standard dans Excel ?",
        "reponses": {
            "A": "Une corbeille de répartition circulaire.",
            "B": "Des barres verticales qui montrent la hauteur des valeurs.",
            "C": "Une courbe continue dessinant une tendance temporelle.",
            "D": "Des bulles dispersées sur deux axes."
        },
        "reponseCorrecte": "B",
        "feedbackPedagogique": "L'histogramme classique affiche toujours des barres verticales."
    },
    "EXCEL-N1-MFORME-C30-Q08": {
        "question": "Quelle méthode permet d'appliquer un format pourcentage (ex: transformer 0,15 en 15%) à une cellule ?",
        "reponses": {
            "A": "Sélectionner la cellule et cliquer sur le symbole '%' dans l'onglet Accueil.",
            "B": "Multiplier la cellule par 100 manuellement.",
            "C": "Écrire 'pourcentage' à côté de la cellule.",
            "D": "Appuyer sur F1 et demander de l'aide."
        },
        "reponseCorrecte": "A",
        "feedbackPedagogique": "L'icône '%' située dans l'onglet Accueil applique instantanément le format Pourcentage."
    },
    "EXCEL-N2-CALCUL-C01-Q05": {
        "question": "Dans la formule '=A1*$B$1', que signifie le symbole '$' autour de B1 ?",
        "reponses": {
            "A": "Il s'agit d'une référence absolue : la référence à B1 restera fixe si la formule est copiée ailleurs.",
            "B": "Il indique que la valeur de B1 est une devise (euros, dollars...).",
            "C": "Il met B1 en gras automatiquement.",
            "D": "Il signale une erreur de saisie dans l'adresse."
        },
        "reponseCorrecte": "A",
        "feedbackPedagogique": "Le $ 'verrouille' la colonne et la ligne concernée pour empêcher le décalage lors d'une recopie."
    },
    "EXCEL-N2-CALCUL-C04-Q07": {
        "question": "À quoi correspond l'erreur #NOM? dans une cellule de résultat ?",
        "reponses": {
            "A": "La plage de données est trop grande pour être calculée.",
            "B": "La cellule contient un texte pur que Excel confond.",
            "C": "Excel ne reconnaît pas un texte présent dans la formule (ex: erreur de frappe sur le nom de la fonction).",
            "D": "Le fichier n'a pas été enregistré sous un nom valide."
        },
        "reponseCorrecte": "C",
        "feedbackPedagogique": "#NOM? survient quasi-toujours si on tape mal le nom de la fonction (ex. =SOMM au lieu de =SOMME)."
    },
    "EXCEL-N2-CALCUL-C06-Q09": {
        "question": "Quelle fonction permet d'obtenir la valeur moyenne d'une plage de données A1:A10 ?",
        "reponses": {
            "A": "=MOY(A1:A10)",
            "B": "=MOYENNE(A1:A10)",
            "C": "=MEDIANE(A1:A10)",
            "D": "=AVERAGE(A1:A10) (uniquement en version française)"
        },
        "reponseCorrecte": "B",
        "feedbackPedagogique": "En version française, c'est =MOYENNE(). L'abréviation 'MOY' n'existe pas en tant que fonction native."
    },
    "EXCEL-N2-ENV-C01-Q01": {
        "question": "Comment accéder aux paramètres pour afficher un onglet caché du Ruban (comme l'onglet Développeur) ?",
        "reponses": {
            "A": "Maintenir Maj et cliquer sur le ruban.",
            "B": "Fichier > Options > Personnaliser le Ruban (puis cocher la case de l'onglet).",
            "C": "Double-cliquer au centre du ruban.",
            "D": "Il faut télécharger un module complémentaire en ligne."
        },
        "reponseCorrecte": "B",
        "feedbackPedagogique": "L'option Personnaliser le Ruban dans les options Excel gère l'affichage de tous les onglets."
    },
    "EXCEL-N2-ENV-C02-Q02": {
        "question": "Quel raccourci clavier permet de se déplacer à la fin de la zone de données de la feuille active ?",
        "reponses": {
            "A": "Ctrl + Fin",
            "B": "Maj + Fin",
            "C": "Alt + F4",
            "D": "Ctrl + Entrée"
        },
        "reponseCorrecte": "A",
        "feedbackPedagogique": "Ctrl+Fin (ou Ctrl+End) amène la sélection à la toute dernière intersection utilisée."
    },
    "EXCEL-N2-ENV-C03-Q03": {
        "question": "Quel est le rôle principal de la 'Poignée de recopie' (le petit carré noir en bas à droite de la cellule active) ?",
        "reponses": {
            "A": "Verrouiller la cellule pour empêcher sa suppression.",
            "B": "Copier rapidement le contenu/formule de la cellule vers les cellules adjacentes en faisant glisser.",
            "C": "Agrandir physiquement la taille de la cellule à l'écran.",
            "D": "Insérer instantanément un graphique associé."
        },
        "reponseCorrecte": "B",
        "feedbackPedagogique": "La poignée de recopie permet d'automatiser la recopie logique de vos données ou formules."
    },
    "EXCEL-N2-ENV-C05-Q04": {
        "question": "Comment sélectionner plusieurs onglets (feuilles de calcul) qui ne sont PAS adjacents ?",
        "reponses": {
            "A": "En maintenant la touche 'Ctrl' enfoncée, puis en cliquant sur chaque onglet.",
            "B": "En maintenant la touche 'Maj' enfoncée, puis en cliquant sur chaque onglet.",
            "C": "En cliquant à droite, -> 'Prendre'.",
            "D": "Seuls les onglets contigus peuvent être sélectionnés en même temps."
        },
        "reponseCorrecte": "A",
        "feedbackPedagogique": "La touche Ctrl permet d'ajouter spécifiquement des feuilles isolées à sa sélection."
    },
    "EXCEL-N2-ENV-C08-Q06": {
        "question": "Après avoir copié un tableau vertical (5 lignes, 2 colonnes), comment le coller pour qu'il devienne horizontal ?",
        "reponses": {
            "A": "Clic droit > Collage spécial > Option 'Transposer'.",
            "B": "Utiliser le raccourci classique Ctrl+V, puis appuyer sur H (Horizontal).",
            "C": "Onglet Accueil > Coller en tant qu'image.",
            "D": "Il n'y a pas d'option native, il faut retaper toutes les valeurs."
        },
        "reponseCorrecte": "A",
        "feedbackPedagogique": "Le collage spécial 'Transposer' permute l'orientation d'une plage ligne/colonne."
    },
    "EXCEL-N2-ENV-C12-Q08": {
        "question": "Où trouver l'option native pour gérer l'En-tête et le Pied de page d'une impression ?",
        "reponses": {
            "A": "Par le menu 'Fichier', onglet 'Historique'.",
            "B": "Via l'onglet 'Insertion' (groupe Texte) ou directement dans 'Mise en page'.",
            "C": "Uniquement en appuyant sur F12 au clavier.",
            "D": "Cliquer droit sur une cellule > Insérer > Pied de page."
        },
        "reponseCorrecte": "B",
        "feedbackPedagogique": "L'en-tête et le pied de page relèvent des réglages d'impression/pagination (Mise en Page)."
    },
    "EXCEL-N2-MFORME-C31-Q10": {
        "question": "Dans l'onglet Accueil, que permet de faire la commande 'Mettre sous forme de tableau' sur une plage de données ?",
        "reponses": {
            "A": "Elle fige instantanément les volets de la ligne supérieure.",
            "B": "Elle convertit la plage en Tableau structuré Excel (filtres intégrés, style automatisé, références variables fluides).",
            "C": "Elle nettoie toutes les couleurs du document.",
            "D": "Elle crée automatiquement un Graphique statique."
        },
        "reponseCorrecte": "B",
        "feedbackPedagogique": "La mise sous forme de tableau (ou Tableau Officiel) est incontournable pour sécuriser un set de données."
    },
    "EXCEL-N3-CALCUL-C03-Q04": {
        "question": "Quelle est la syntaxe valide combinant INDEX et EQUIV pour une recherche multi-critère ?",
        "reponses": {
            "A": "=INDEX(colonne_resultat; EQUIV(critere; colonne_recherche; 0))",
            "B": "=RECHERCHEV(INDEX(critere; 0); EQUIV())",
            "C": "=EQUIV(colonne_resultat; INDEX(critere; 0))",
            "D": "=INDEX_EQUIV(critere; colonne_recherche; colonne_resultat)"
        },
        "reponseCorrecte": "A",
        "feedbackPedagogique": "EQUIV trouve la position relative, et INDEX retourne l'élément situé à cette position dans la matrice de résultats."
    },
    "EXCEL-N3-CALCUL-C06-Q07": {
        "question": "Quelle fonction permet de compter le nombre exact de fois où une valeur spécifique (ex: 'Paris') apparaît dans une plage ?",
        "reponses": {
            "A": "=COMPTE('Paris'; A1:A100)",
            "B": "=NBVAL(A1:A100; = 'Paris')",
            "C": "=NB.SI(A1:A100; 'Paris')",
            "D": "=NBCAR(A1:A100) / 'Paris'"
        },
        "reponseCorrecte": "C",
        "feedbackPedagogique": "=NB.SI() compte le nombre de cellules remplissant une condition stricte."
    },
    "EXCEL-N3-CALCUL-C08-Q03": {
        "question": "Quelle formule de recherche verticale (RECHERCHEV) est syntaxiquement correcte avec correspondance exacte ?",
        "reponses": {
            "A": "=RECHERCHEV(valeur_cherche; matrice_tableau; no_index_col; FAUX)",
            "B": "=RECHERCHEV(matrice_tableau; valeur_cherche; no_index_col; VRAI)",
            "C": "=RECHERCHE(matrice_tableau; valeur_cherche)",
            "D": "=RECHERCHEV(valeur_cherche; no_index_col; matrice_tableau)"
        },
        "reponseCorrecte": "A",
        "feedbackPedagogique": "L'argument logique FAUX (ou 0) à la fin garantit une correspondance strictement exacte."
    },
    "EXCEL-N3-CALCUL-C09-Q05": {
        "question": "Hors l'opérateur '&', quelle est la fonction la plus souple sous Office 365 pour fusionner des cellules textuelles en ignorant les cases vides ?",
        "reponses": {
            "A": "=ASSOCIATION.MOTS(' '; A1; B1)",
            "B": "=JOINDRE.TEXTE(' '; VRAI; A1:D1)",
            "C": "=FUSION_CELLS(A1; B1)",
            "D": "=CONCATENER_IGNORER_VIDE(A1:D1)"
        },
        "reponseCorrecte": "B",
        "feedbackPedagogique": "La fonction JOINDRE.TEXTE permet très facilement d'inclure un délimiteur (ex l'espace) et de sauter les vides."
    },
    "EXCEL-N3-CALCUL-C11-Q08": {
        "question": "Quelle est la syntaxe et l'ordre des arguments de la fonction SOMME.SI.ENS ?",
        "reponses": {
            "A": "=SOMME.SI.ENS(plage_critere1; critere1; plage_somme)",
            "B": "=SOMME(SI_ENS(plage_somme; critere1))",
            "C": "=ENS.SOMMESI(plage_somme; critere1)",
            "D": "=SOMME.SI.ENS(plage_somme; plage_critere1; critere1; plage_critere2; critere2...)"
        },
        "reponseCorrecte": "D",
        "feedbackPedagogique": "SOMME.SI.ENS démarre toujours par la Plage Globale à Sommer, avant d'enchaîner les filtres (Plage Critère; Critère)."
    },
    "EXCEL-N3-ENV-C14-Q01": {
        "question": "Si un classeur Excel est hébergé sur OneDrive/SharePoint, comment restaurer une version précédente du document ?",
        "reponses": {
            "A": "Fichier > Informations > Historique des versions, puis ouvrir la version désirée.",
            "B": "Demander un accord technique à Microsoft via le portail F1.",
            "C": "Restaurer via l'onglet 'Développeur' > 'Macros'.",
            "D": "C'est impossible, les sauvegardes en ligne écrasent tout."
        },
        "reponseCorrecte": "A",
        "feedbackPedagogique": "Les fichiers dans le cloud Office 365 bénéficient de l'historique de versions intégré directement dans l'outil Fichier."
    },
    "EXCEL-N3-ENV-C17-Q02": {
        "question": "Comment verrouiller une feuille de calcul afin d'empêcher un utilisateur d'effacer les cellules contenant des formules ?",
        "reponses": {
            "A": "Cacher physiquement le ruban.",
            "B": "Il n'y a pas de protection sauf convertir le fichier en PDF / Lecture seule brute.",
            "C": "Onglet 'Révision' > 'Protéger la feuille' (après avoir déverrouillé les cellules de saisie).",
            "D": "Sélectionner tout et utiliser 'Cacher des données'."
        },
        "reponseCorrecte": "C",
        "feedbackPedagogique": "Protéger la feuille (via Révision) sécurise l'architecture et les formules d'un fichier Excel."
    },
    "EXCEL-N3-GDONNEES-C06-Q10": {
        "question": "Qu'est-ce qu'un 'Segment' (Slicer) pour un Tableau Croisé Dynamique ou Structuré ?",
        "reponses": {
            "A": "C'est une macro qui tronque les lignes de valeurs impaires.",
            "B": "C'est un outil graphique interactif basé sur un champ de boutons pour filtrer vos données rapidement.",
            "C": "C'est une nouvelle ligne de total automatiquement générée par Excel en bas.",
            "D": "C'est un diagramme radar."
        },
        "reponseCorrecte": "B",
        "feedbackPedagogique": "Les Segments offrent un filtrage visuel par clics très ergonomique dans un tableau de bord."
    },
    "EXCEL-N3-GDONNEES-C08-Q09": {
        "question": "Comment imposer strictement la saisie de 'Oui', 'Non', ou 'Inactif' dans une colonne pour garantir l'intégrité des données ?",
        "reponses": {
            "A": "Transformer la colonne en Format Textuel à restriction.",
            "B": "En ajoutant une cellule de mode d'emploi en rouge.",
            "C": "Onglet 'Données' > 'Validation des données' > Autoriser 'Liste'.",
            "D": "En utilisant l'outil Clic Droit > 'Interdire la saisie libre'."
        },
        "reponseCorrecte": "C",
        "feedbackPedagogique": "La Validation des Données bloque l'utilisateur en générant une contrainte avec menu déroulant de ces 3 choix."
    },
    "EXCEL-N3-MFORME-C06-Q06": {
        "question": "Comment changer la couleur d'une LIGNE ENTIÈRE (Plage A2:J20) seulement si la cellule en B (B2, B3...) contient 'Terminé' ?",
        "reponses": {
            "A": "Sélectionner la plage, puis Mise en forme conditionnelle > Nouvelle règle > Utiliser une formule > `=$B2=\"Terminé\"`.",
            "B": "Sélectionner la plage, Mise en forme conditionnelle > Règles de surbrillance > Texte qui contient > `Terminé`.",
            "C": "Il est impossible d'influencer la cellule A2 depuis la valeur B2, la couleur colore unique la cellule concernée.",
            "D": "Copier le mot Terminé avec le Pinceau Formateur et balayer chaque ligne adéquate."
        },
        "reponseCorrecte": "A",
        "feedbackPedagogique": "L'utilisation de la formule couplée à une notion de ligne absolue/colonne relative (=$B2) colore toute une ligne visuelle."
    }
}

path = 'db/questions'
updated = 0
for fname in os.listdir(path):
    if not fname.endswith('.json'): continue
    q_id = fname.replace('.json', '')
    if q_id in updates:
        fpath = os.path.join(path, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        upd = updates[q_id]
        data['question'] = upd['question']
        data['reponses'] = upd['reponses']
        data['reponseCorrecte'] = upd['reponseCorrecte']
        data['feedbackPedagogique'] = upd['feedbackPedagogique']
        
        with open(fpath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[{q_id}] Updated successfully.")
        updated += 1
    else:
        print(f"[{q_id}] Not found in updates mapping.")

print(f"\nTotal updated: {updated}/30")
