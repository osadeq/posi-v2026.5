# TOSA - Dashboard Admin

## Description
Application locale de gestion des tests de positionnement TOSA.
Portable - fonctionne sans installation, données au format JSON.

## Utilisation

### Methode 1 - Starter (Recommandée)
```bash
Double-cliquez sur: starter_dashboard.bat
```

### Methode 2 - Manuelle
```bash
cd dashboard
pip install flask
python main.py
```

## Accès
- URL: http://localhost:5001

## Fonctionnalités

### Tableau de bord
- Nombre de tests reçus
- Nombre de candidats
- Nombre de programmes générés
- **Répartition des Besoins** : graphique-barres Fort/Moyen/Faible avec pourcentages

### Gestion des candidats (CRUD)
- Liste des candidats
- **Créer** : nouveau candidat avec nom, prénom, email, téléphone, entreprise, objectifs
- **Modifier** : éditer les informations
- **Supprimer** : supprimer un candidat

### Tests reçus (CRUD)
- Liste des tests soumis via la webapp
- **Filtre temporel** : navigation par mois/année
- Bouton "Charger les tests" pour importer depuis `tests_soumis.json`
- **Créer** : nouveau test manuellement
- **Analyser** : voir détails + programme auto-généré avec courbe IRT
- **Modifier / Supprimer**
- Niveau détecté affiché : Novice, Débutant, Intermédiaire, Avancé
- Objectifs du candidat affichés
- Dates : affichage date/heure

### Programmes générés (CRUD)
- Liste des programmes personnalisés
- **Génération auto** : à l'analyse du test
- **Génération PDF** (format HTML)
- **Génération Excel** (format CSV)
- **Modifier** : durée, coût
- **Dupliquer** : copier un programme
- **Supprimer**
- Détail du programme :
  - Ligne 1 : Titre du programme
  - Ligne 2 : Durée, Coût, Nombre de thèmes
  - Détail : Thème + Durée + Besoin (FORT/MOYEN/FAIBLE) + Compétences + Activités

### Import CSV
- Importer des tests saisis hors webapp
- Format attendu: nom,prenom,email,formation,niveau,type_test,reponses...
- Gestion des erreurs robuste

## Données
Les données sont stockées dans `data/data.json`:
- candidats
- tests_recus
- programmes_generes

Les tests sont automatiquement chargés depuis `../tests_soumis.json` (webapp).

## Configuration
Modifier `data/data.json` pour changer:
- tarif_horaire_defaut (par défaut 45€)
- email_organisation
- nom_organisation