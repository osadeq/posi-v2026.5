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

## Niveaux IRT (v1.4)
Le test adaptatif détecte 4 niveaux :
- **Novice** : theta < -0.8 (Aucune connaissance du logiciel)
- **Débutant** : -0.8 ≤ theta < 0 (Connaît les bases essentielles)
- **Intermédiaire** : 0 ≤ theta < 1 (Maîtrise les fonctions courantes)
- **Avancé** : theta ≥ 1 (Expert, certification recommandée)

## Moteur IRT et Banque de Questions
- **Algorithme Aléatoire Pondéré** : Le moteur IRT choisit les questions au hasard parmi les 5 meilleures adaptées au niveau.
- **Affichage du niveau** : Le badge au-dessus de la question affiche "Débutant", "Intermédiaire" ou "Avancé" (au lieu du % de difficulté).
- **Base de 111 questions** : Questions sur Calculs, Données, Mise en Forme, Environnement.

## Nouveautés Visuelles et Outils de QA
- L'évaluation affiche la progression du niveau (Novice -> Expert) via une **courbe Chart.js**.
- Les points sont colorisés selon la justesse (Vert / Rouge).
- **Mode Debug intégré** : Bonnes réponses et feedbacks sous chaque question.

## Auto-Positionnement et Génération
- **UI Matricielle Premium** : Sélecteurs circulaires colorés.
- **Générateur JSON** : Plan de formation complet avec devis (45€/h).

## Format d'envoi des résultats
Les résultats sont sauvegardés dans `../tests_soumis.json` avec :
- candidat (nom, prénom, email, objectifs)
- formation, niveau, type
- réponses
- theta, level (n0/n1/n2/n3)
- timestamp

## Configuration pour Vercel
Déployer sur Vercel en ajoutant un fichier `vercel.json`:
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