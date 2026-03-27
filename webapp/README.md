# TOSA - Test de Positionnement Webapp

## Description
Application web candidate pour les tests de positionnement TOSA.
Stateless - pas de stockage local, envoi des résultats après soumission.

## Utilisation

### Methode 1 - Starter (Recommandée)
```bash
Double-cliquez sur: starter_webapp.bat
```

### Methode 2 - Manuelle
```bash
cd webapp
pip install -r requirements.txt
python app.py
```

- Accès
- URL: http://localhost:5000
- Pages disponibles:
  - `/` - Page d'accueil
  - `/identification` - Formulaire candidat simplifié (Infos, Objectifs et choix Novice/Test)
  - `/test-adaptatif` - Test QCM intelligent avec graphique d'évolution animé (Chart.js)
  - `/resultats` - Résultats avec programme recommandé
  - `/auto-positionnement` - Auto-évaluation
  - `/confirmation` - Confirmation après soumission

## Nouveautés Visuelles et Outils de QA (v1.3)
- L'évaluation affiche désormais la progression du niveau (Novice -> Expert) en direct via une **courbe tracée par Chart.js**.
- Les points de la courbe sont colorisés en temps réel selon la justesse de la réponse (Vert / Rouge).
- **Mode Debug intégré** : Les bonnes réponses et retours pédagogiques s'affichent sous chaque question QCM dans un encart jaune spécifique pour permettre la validation de l'algorithme sans chercher les solutions.

## Moteur IRT et Banque de Questions (v1.4)
- **Algorithme Aléatoire Pondéré** : Le moteur IRT choisit désormais les questions au hasard parmi les 5 meilleures questions adaptées au niveau actuel du candidat. Fin des examens monotones.
- **Débridage de la Note Maximale** : Le seuil de chute mathématique lié à la convergence a été corrigé pour laisser la possibilité naturelle d'accéder à la `CERTIFICATION_TOSA_EXPERT` avec un parcours parfait.
- **Base de 111 questions** : La base locale JSON compte 111 questions qui maillent l'intégralité des secteurs d'expertise (Calculs, Données, Mise en Forme, Environnement) du Novice à l'Expert.

## Auto-Positionnement et Génération (v1.5)
- **UX Adaptative et Ergonomique** : Le candidat navigue via un système d'accordéons de domaine. Bouton maître "Tout déclarer Acquis", format condensé sur une seule ligne.
- **Règles Métier Intelligentes** : Si la maîtrise est définie sur "Aucune" ou "Moyenne", le choix de formation s'active automatiquement ("Oui"). Saisie en cascade automatique.
- **Générateur JSON Structuré** : Le bouton de soumission compile via l'API un plan de formation rigoureux calqué sur l'organisation des programmes `programmes.json`, incluant devis 45€/h et durées estimées.

## Configuration pour Vercel
Déployer sur Vercel en'ajoutant un fichier `vercel.json`:
```json
{
  "build": {
    "command": "pip install -r requirements.txt"
  },
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/app.py"
    }
  ]
}
```

## Format d'envoi des résultats
Les résultats sont sauvegardés dans `../tests_soumis.json`
(déplacé vers le dashboard pour analyse)