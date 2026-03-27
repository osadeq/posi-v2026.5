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

### Gestion des candidats
- Liste des candidats
- Rechercher par nom/email

### Tests reçus
- Liste des tests soumis via la webapp
- Bouton "Charger les tests" pour importer
- Analyser un test → générer un programme

### Programmes générés
- Liste des programmes personnalisés
- Génération PDF
- Génération Excel
- Détail: durée estimée, coût estimé, thèmes

### Import CSV
- Importer des tests saisis hors webapp
- Format attendu: nom,prenom,email,formation,niveau,reponses

## Données
Les données sont stockées dans `data/data.json`:
- candidats
- tests_recus
- programmes_generes

## Configuration
Modifier `data/data.json` pour changer:
- tarif_horaire_defaut (par défaut 45€)
- email_organisation
- nom_organisation