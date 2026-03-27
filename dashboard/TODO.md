# TODO - Dashboard Admin (Prochaines Étapes)

## 1. Intégration des Données 
- [ ] Connecter le Dashboard au fichier `tests_soumis.json` généré par la Webapp.
- [ ] Valider la récupération de l'information `objectifs` fraîchement ajoutée côté candidat.

## 2. Tableaux de Bord et Statistiques
- [ ] Réparer ou améliorer le composant graphique de "Répartition des Besoins" (vérifier l'affichage des pourcentages des besoins Fort/Moyen/Faible).
- [ ] Mettre en place et finaliser le filtre "esadeq_timeTravel" (navigation temporelle en spirale) pour le tri innovant des candidats.

## 3. Gestion des imports / exports
- [ ] S'assurer que la fonction d'importation de questionnaires depuis des fichiers Excel (`.xlsx`) via `parse_excel_questionnaire` est 100% robuste.
- [ ] Finaliser l'outil de génération de Programmes d'apprentissage au format PDF / Excel pour les candidats traités.

## 4. Affinage UI / UX
- [ ] S'aligner avec le design system (Primaire #2563EB, styles modernes, animations) défini dans le PRD.
- [ ] Implémenter les vues de détails d'un Test (pour voir la nouvelle courbe d'évaluation IRT d'un candidat depuis l'interface admin).
