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

## Auto-Positionnement et Génération (v2.1)
- **UI Matricielle Premium** : Navigation par accordéons avec sélecteurs circulaires colorés (Rouge, Jaune, Vert pour l'Acquis / Noir pour le Besoin).
- **Cascade Asymétrique** : Automatisme intelligent de l'Acquisition vers le Besoin (override autorisé sans casser la déclaration initiale).
- **Réflexivité & Sécurité** : Conservation des saisies en session Flask (anti-rafraîchissement) et purge automatique inter-candidats pour la confidentialité.
- **Générateur JSON Structuré** : Compilation d'un plan de formation complet avec devis (45€/h) et durées, mappé sur `programmes.json`.

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