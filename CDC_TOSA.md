# Cahier des Charges - Application TOSA de Positionnement

## 1. Contexte et Objectifs du Projet

### 1.1 Contexte
Ce projet consiste à développer une application complète de gestion des tests de positionnement TOSA pour les formations bureautiques (Excel, Word, PowerPoint, etc.). L'application se compose de deux modules distincts :

- **Webapp Candidate** : Application stateless hébergée sur Vercel/Moodle permettant aux candidats de passer les tests de positionnement
- **Dashboard Admin** : Application locale portable pour l'équipe pédagogique

### 1.2 Objectifs
- Permettre aux candidats de s'auto-évaluer sur les compétences TOSA
- Générer des programmes de formation personnalisés basés sur les résultats
- Faciliter le suivi et l'analyse des positionnements par l'équipe pédagogique
- **Nouveau** : Test adaptatif IRT avec sélection intelligente des questions

---

## 2. Architecture Technique

### 2.1 Architecture Générale

```
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION TOSA                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────┐      ┌──────────────────────┐      │
│  │   WEBAPP CANDIDATE    │      │   DASHBOARD ADMIN    │      │
│  │   (Vercel/Moodle)     │      │   (Local Portable)   │      │
│  │                      │      │                      │      │
│  │  - Identification     │      │  - Tableau de bord  │      │
│  │  - Test Adaptatif IRT │      │  - Analyse tests    │      │
│  │  - Resultats          │      │  - Génération PDF    │      │
│  │  - Auto-positionnement│      │  - Import CSV        │      │
│  │                      │ ──►  │  - CRUD candidats    │      │
│  └──────────────────────┘      └──────────────────────┘      │
│              │                              │                   │
│              ▼                              ▼                   │
│     [Envoi results]              [Analyse & Programme]          │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                         DONNEES                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  db/                                                      │   │
│  │  ├── database.json     (Référentiel compétences TOSA)     │   │
│  │  ├── programmes.json   (Programmes de formation)          │   │
│  │  └── questions/        (30 questions avec IRT)            │   │
│  │                                                                 │
│  │  dashboard/data/                                           │   │
│  │  └── data.json        (Candidats, tests, programmes)     │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Composition des Modules

#### 2.2.1 Webapp Candidate

| Composant | Description |
|-----------|-------------|
| `app.py` | Application Flask principale |
| `templates/` | Templates HTML |
| `static/styles.css` | Feuille de styles CSS |
| `requirements.txt` | Dépendances Python |

**Pages disponibles :**
- `/` - Page d'accueil
- `/identification` - Formulaire candidat
- `/test/<formation>/<niveau>` - Test QCM
- `/auto-positionnement` - Auto-évaluation
- `/confirmation` - Confirmation après soumission
- `/api/niveaux/<formation_id>` - API niveaux
- `/api/test/<formation_id>/<niveau_id>` - API questions
- `/soumettre` - Soumission des réponses
- `/api/auto-questions/<formation_id>/<niveau_id>` - API auto-évaluation

#### 2.2.2 Dashboard Admin

| Composant | Description |
|-----------|-------------|
| `main.py` | Point d'entrée portable |
| `app.py` | Application Flask principale |
| `data/data.json` | Base de données locale |
| `templates/` | Templates HTML |
| `utils/` | Utilitaires (analyser, generator, importer) |

**Pages disponibles :**
- `/` - Tableau de bord
- `/candidats` - Liste des candidats
- `/tests` - Liste des tests reçus
- `/programmes` - Programmes générés
- `/importer` - Import CSV
- `/analyser/<test_id>` - Analyse et génération programme
- `/generer-pdf/<programme_id>` - Génération PDF
- `/generer-excel/<programme_id>` - Génération Excel

### 2.3 Technologies Utilisées

| Element | Technologie |
|---------|-------------|
| Langage | Python 3.x |
| Framework Web | Flask 2.3+ |
| Templates | HTML5 + CSS3 |
| Base de données | JSON (fichiers plats) |
| Police | Inter (Google Fonts) |

---

## 3. Structure des Données

### 3.1 Base de Données Référentiel (db/database.json)

**Voir section 3.1 dans la version precedente**

```json
{
  "formations": [
    {
      "id": "excel",
      "nom": "Excel",
      "description": "Tableur Microsoft Excel",
      "niveaux": [
        {
          "id": "n1",
          "nom": "Initiation",
          "score_min": 1,
          "score_max": 350,
          "niveau_tosa": "Initial",
          "domaines": [
            {
              "id": "env",
              "nom": "Environnement / Méthodes",
              "competences": [
                {
                  "id": "EXCEL-N1-ENV-C01",
                  "code": "EXCEL-N1-ENV-C01",
                  "nom": "Ouvrir un document Excel"
                }
              ]
            }
          ]
        }
      ],
      "positionnements": {
        "autoPositionnement": {
          "description": "Questionnaire d'auto-évaluation par compétences",
          "niveaux": [...]
        },
        "testPositionnement": {
          "description": "Test d'évaluation par questions",
          "niveaux": [
            {
              "id": "n1",
              "nom": "Initiation",
              "questions": [
                {
                  "id": "EXCEL-N1-ENV-C01-Q01",
                  "formationId": "EXCEL",
                  "competencesCibles": ["EXCEL-N1-ENV-C01"],
                  "contenu": "EXCEL-N1-ENV-C01-Q01.json"
                }
              ]
            }
          ]
        }
      }
    }
  ]
}
```

### 3.2 Questions Externes (db/questions/)

Fichier : `EXCEL-N1-ENV-C01-Q01.json`

```json
{
  "competencesCibles": ["EXCEL-N1-ENV-C01"],
  "question": "Comment ouvrir un document Excel existant ?",
  "reponses": {
    "A": "Fichier > Nouveau",
    "B": "Fichier > Ouvrir et parcourir le fichier",
    "C": "Fichier > Enregistrer sous",
    "D": "Fichier > Imprimer"
  },
  "reponseCorrecte": "B",
  "feedbackPedagogique": "Pour ouvrir un document existant..."
}
```

### 3.3 Programmes de Formation (db/programmes.json)

```json
[
  {
    "id": "EXCEL-ATELIER",
    "formationId": "EXCEL",
    "type": "ATELIER_TUTORE_INDIVIDUALISE",
    "titre": "Exploiter les fonctionnalités de Microsoft Excel...",
    "duree": null,
    "dureeNote": "Planifié par demi-journée de 3h30 ou journée de 7h",
    "tarifHoraire": 45,
    "objectifs": [...],
    "themes": [
      {
        "id": "T01",
        "titre": "Environnement Excel / Interface",
        "description": "...",
        "activites": [...],
        "competencesCibles": ["EXCEL-N1-ENV-C01", "EXCEL-N2-ENV-C01"]
      }
    ]
  }
]
```

### 3.4 Données Dashboard (dashboard/data/data.json)

```json
{
  "candidats": [...],
  "tests_recus": [...],
  "programmes_generes": [...],
  "config": {
    "tarif_horaire_defaut": 45,
    "email_organisation": "contact@formation-tosa.fr",
    "nom_organisation": "Formation TOSA"
  }
}
```

---

## 4. Spécifications Fonctionnelles

### 4.1 Webapp Candidate

#### 4.1.1 Page d'Accueil
- Présentation de l'application
- Accès au test de positionnement
- Accès à l'auto-évaluation

#### 4.1.2 Identification Candidat
- Sélection de la formation (Excel, Word, etc.)
- Sélection du niveau (Initiation, Intermédiaire, Perfectionnement)
- Saisie des informations personnelles (nom, prénom, email)
- Validation et passage au test

#### 4.1.3 Test de Positionnement QCM
- Affichage progressif des questions (une par page)
- Barre de progression
- Navigation (précédent/suivant)
- Validation de toutes les réponses
- Soumission finale

#### 4.1.4 Auto-Positionnement
- Évaluation par compétence
- Réponses : Maîtrise (Aucune/Moyenne/Acquise)
- Souhait de formation (Oui/Non)
- Soumission des réponses

#### 4.1.5 Confirmation
- Message de confirmation
- Indication du traitement à venir

### 4.2 Dashboard Admin

#### 4.2.1 Tableau de Bord
- Statistiques globales (tests, candidats, programmes)
- Liste des derniers tests reçus
- Accès rapide aux actions

#### 4.2.2 Gestion des Candidats
- Liste des candidats
- Information de contact

#### 4.2.3 Tests Reçus
- Liste complète des tests
- Bouton de chargement des tests (import depuis webapp)
- Action d'analyse

#### 4.2.4 Analyse et Génération de Programme
- Analyse du test
- Identification des besoins
- Sélection des thèmes appropriés
- Calcul de la durée et du coût

#### 4.2.5 Programmes Générés
- Liste des programmes personnalisés
- Génération PDF du programme
- Génération Excel du programme

#### 4.2.6 Import CSV
- Import de tests saisis hors webapp
- Format attendu : nom,prenom,email,formation,niveau,type_test,reponses

---

## 5. Spécifications d'Interface

### 5.1 Design Global

#### Palette de Couleurs
| Element | Couleur |
|---------|---------|
| Primaire | #2563EB |
| Secondaire | #10B981 |
| Accent | #F59E0B |
| Fond | #F8FAFC |
| Texte | #1E293B |
| Bordure | #E2E8F0 |

#### Typographie
- Police : Inter (Google Fonts)
- Titres : 700, 24-32px
- Corps : 400, 14-16px

#### Style
- Coins arrondis : 8px
- Ombres légères
- Transitions fluides

### 5.2 Composants UI

#### Boutons
- Primaire : fond bleu, texte blanc
- Secondaire : fond vert
- Outline : bordure bleue, transparent

#### Cartes Questions
- Fond blanc, bordure légère
- Options de réponse avec lettrage (A, B, C, D)
- Sélection visuelle lors du choix

#### Progress Bar
- Dégradé bleu → vert
- Pourcentage affiché

#### Badges de Niveau
- N1 (Initiation) : bleu
- N2 (Intermédiaire) : vert
- N3 (Perfectionnement) : orange

---

## 6. Spécifications Techniques

### 6.1 Déploiement Webapp

#### Vercel
- Fichier `vercel.json` nécessaire
- Commandes de build incluses
- Variables d'environnement configurables

#### Moodle
- Intégration possible via LTI
- Authentification gérée par Moodle

### 6.2 Portabilité Dashboard

#### Caractéristiques
- Pas d'installation requise
- Fonctionne sur clé USB
- Python portable (pas de droits admin)
- Données au format JSON

#### Lancement
- Double-cliquer sur `starter_dashboard.bat`
- Création automatique de l'environnement virtuel

---

## 7. Conventions de Nommage

| Element | Format | Exemple |
|---------|--------|---------|
| Code compétence | Nx-DOMAINE-Cxx | EXCEL-N1-ENV-C01 |
| ID formation | Majuscules | EXCEL |
| Niveaux | n1, n2, n3 | n1 |
| Domaines | env, calcul, mforme, gdonnees | env |
| Questions externes | FORMATION-NIVEAU-DOMAINE-COMP-QNN.json | EXCEL-N1-ENV-C01-Q01.json |
| Programmes | FORMATION-TYPE | EXCEL-ATELIER |
| Thèmes | T01, T02... | T01 |

---

## 8. Livrables

### 8.1 Fichiers du Projet

```
Modeles/
├── webapp/                    # Application candidate
│   ├── app.py                 # Application Flask avec IRT
│   ├── irt_engine.py          # Moteur IRT (optionnel)
│   ├── requirements.txt
│   ├── static/
│   │   └── styles.css
│   ├── templates/
│   │   ├── index.html
│   │   ├── identification.html
│   │   ├── test_adaptatif.html  # NOUVEAU - Test IRT
│   │   ├── resultats.html        # NOUVEAU - Resultats avec programme
│   │   ├── confirmation.html
│   │   └── auto_positionnement.html
│   └── starter_webapp.bat
│
├── dashboard/                 # Dashboard admin
│   ├── main.py
│   ├── app.py
│   ├── data/
│   │   └── data.json
│   ├── templates/
│   │   ├── dashboard.html
│   │   ├── candidats.html
│   │   ├── tests.html
│   │   ├── programmes.html
│   │   └── importer.html
│   └── starter_dashboard.bat
│
├── db/                       # Base de données
│   ├── database.json         # Referentiel TOSA
│   ├── programmes.json       # 4 programmes
│   └── questions/            # 30 questions avec parametres IRT
│       ├── EXCEL-N1-*.json
│       ├── EXCEL-N2-*.json
│       └── EXCEL-N3-*.json
│
├── archives/                  # Documents sources
│   └── *.txt, *.xlsx
│
├── prd.txt                   # Document de conception
└── CDC_TOSA.md              # Cahier des charges
```

### 8.2 Documentation

- README.md (webapp)
- README.md (dashboard)
- CDC (ce document)

---

## 9. Test Adaptatif IRT (Item Response Theory)

### 9.1 Principe
Le test adaptatif IRT selectionne chaque question en fonction du niveau de competence estime (theta) du candidat. Chaque question posee modifie l'estimation du niveau, et la question suivante est choisie pour maximiser l'information collectee.

### 9.2 Parametres IRT des questions
Chaque question contient trois parametres IRT :
- **difficulty** (0-100) : Difficulte de la question. Conversion moteur : `d = (difficulty - 50) / 10`
- **discrimination** (0.5-2.0) : Pouvoir discriminant (capacite a distinguer les niveaux)
- **guessing** (0-0.25) : Probabilite de deviner juste par chance (4 choix = 0.25)

### 9.2.1 Calibrage IRT des 30 questions

Les valeurs de `difficulty` sont calibrees pour que chaque groupe de questions
discimine precisement aux seuils theta de la regle de positionnement :

| Niveau | Theta cible | Difficulty | Discrimination |
|--------|-------------|------------|----------------|
| N1 - Initiation | -1.2 a -0.4 | 38 a 46 | 1.2 |
| N2 - Intermediaire | -0.2 a +0.5 | 48 a 55 | 1.4 |
| N3 - Perfectionnement | +0.8 a +1.5 | 58 a 65 | 1.6 |

Gaps volontaires entre niveaux (46->48 et 55->58) pour creer des zones de
discrimination nettes aux seuils theta = -0.8, 0 et +1.

La discrimination croissante (1.2 -> 1.4 -> 1.6) garantit que :
- Les questions N1 restent accessibles sans sur-penaliser les vrais debutants
- Les questions N3 separent efficacement les vrais experts des candidats qui se surestiment

### 9.3 Algorithme de selection des questions
1. **Initialisation** : theta = valeur initiale selon niveau declare (voir section 9.4)
2. **Selection** : Choisir la question dont la difficulte est la plus proche de theta
3. **Mise a jour** : Apres chaque reponse, recalculer theta et SE (Standard Error)
4. **Arret** : Le test s'arrete si :
   - SE < 0.3 (precision suffisante) ET 10 questions minimum
   - 30 questions maximum atteintes

### 9.4 Logique de Positionnement (Regles Metier)

#### Etape 1 : Declaration du niveau actuel
Le candidat declare son niveau actuel via un menu deroulant.
Ce choix sert **uniquement** a initialiser theta de depart pour le test adaptatif :
- **Novice** : "Je n'ai jamais utilise Excel" -> pas de test, EXCEL-INIT direct
- **Debutant** : "Je connais les bases (saisie, mise en forme et formules simples)" -> theta_init = -0.5
- **Intermediaire** : "Je maitrise les tableaux, le tri/filtre et fonctions usuelles" -> theta_init = +0.5
- **Perfectionnement** : "Je maitrise les tableaux croises et fonctions avancees" -> theta_init = +1.5

#### Etape 2 : Traitement special Novice
Si le candidat declare etre **Novice** :
- Pas de test a passer
- Resultat direct : Niveau = N0 Novice, Programme = EXCEL-INIT

#### Etape 3 : Test adaptatif (Debutant, Intermediaire, Perfectionnement)
Pour les autres niveaux, un test adaptatif est propose (SE_init = 2.5 pour tous) :
- **Debutant** : theta_init = -0.5
- **Intermediaire** : theta_init = +0.5
- **Perfectionnement** : theta_init = +1.5

#### Etape 4 : Determination du programme
A la fin du test (10 questions minimum ou SE < 0.3), la regle est **unifiee et independante du niveau declare** : theta seul determine le niveau actuel, puis le niveau actuel determine le programme.

| ThetaResult | Niveau actuel | Programme |
|-------------|---------------|-----------|
| theta < -0.8 | N0 — Novice | **EXCEL-INIT** |
| -0.8 <= theta < 0 | N1 — Debutant | **EXCEL-INTER** |
| 0 <= theta < 1 | N2 — Intermediaire | **EXCEL-PERF** |
| theta >= 1 | N3 — Avance | **CERTIFICATION_TOSA_EXPERT** |

**Cas special Novice (etape 1)** : le candidat qui declare ne pas connaitre Excel est oriente directement en EXCEL-INIT sans passer le test.

**Notes importantes** :
- Le niveau declare sert uniquement a initialiser theta de depart (theta_init) pour le test adaptatif
- Le resultat final depend exclusivement de theta mesure par l'IRT
- N3 ne donne pas lieu a une formation mais a une preparation et passage de la certification TOSA Expert

### 9.5 Affichage pendant le test
L'interface affiche en temps reel :
- **THETA** : Niveau de competence actuel
- **SE** : Incertitude (plus elle est basse, plus le resultat est sur)
- **Confiance** : Pourcentage de confiance calcule (100 - SE*20)

---

## 10. Glossaire

| Terme | Définition |
|--------|-------------|
| TOSA | Test On Software Applications - Certification des compétences numériques |
| IRT | Item Response Theory - Théorie de réponse à l_ITEM |
| Theta | Estimation du niveau de compétence du candidat |
| SE | Standard Error - Incertitude de l'estimation |
| QCM | Questionnaire à Choix Multiples |
| Auto-positionnement | Évaluation par le candidat lui-même de ses compétences |
| Test de positionnement | Évaluation structurée par questions QCM |
| Programme de formation | Ensemble de thèmes et activités pour atteindre un niveau |
| Dashboard | Interface d'administration et de gestion |
| Stateless | Sans conservation de données côté client |

---

*Document genere le 24 mars 2026*
*Version 1.2 - Calibrage IRT corrige et regle de positionnement unifiee*
*Version 1.1 - Ajout du test adaptatif IRT*
*Version 1.0*