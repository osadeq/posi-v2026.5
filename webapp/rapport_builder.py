import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(os.path.dirname(BASE_DIR), 'db')

def build_auto_rapport(data):
    """
    Construit un objet JSON de compte-rendu d'auto-positionnement structuré 
    sur le modèle 'themes_a_former', 'themes_par_domaine', 'reponses_par_bloc'.
    """
    candidat = data.get('candidat', {})
    formation_id = data.get('formation', '')
    niveau_id = data.get('niveau', '')
    reponses = data.get('reponses', [])

    level_map = {'n1': 'EXCEL-INIT', 'n2': 'EXCEL-INTER', 'n3': 'EXCEL-PERF'}
    prog_id = level_map.get(niveau_id, 'EXCEL-INIT')

    prog_path = os.path.join(DB_DIR, 'programmes.json')
    all_progs = []
    if os.path.exists(prog_path):
        with open(prog_path, 'r', encoding='utf-8') as f:
            all_progs = json.load(f)

    target_prog = next((p for p in all_progs if p['id'] == prog_id), None)
    if not target_prog and all_progs:
        target_prog = all_progs[0]
    elif not target_prog:
        target_prog = {}

    domaines_map = {
        'ENV': {'id': 'D1', 'nom': 'Environnement / Méthodes'},
        'CALCUL': {'id': 'D2', 'nom': 'Calculs & Formules'},
        'MFORME': {'id': 'D3', 'nom': 'Mise en forme'},
        'GDONNEES': {'id': 'D4', 'nom': 'Gestion des données'},
        'AUTRE': {'id': 'UNK', 'nom': 'Autres'}
    }

    # "Besoins" = Souhait Oui et Maitrise != Acquise
    reponses_a_former = [r for r in reponses if r.get('souhait') == 'Oui' and r.get('maitrise') != 'Acquise']
    codes_retenus = [r['code'] for r in reponses_a_former]
    
    themes_a_former = []
    themes_par_domaine_dict = {}

    for theme in target_prog.get('themes', []):
        theme_competences = []
        for cibl in theme.get('competencesCibles', []):
            if cibl in codes_retenus:
                r = next((resp for resp in reponses_a_former if resp['code'] == cibl), None)
                if r:
                    theme_competences.append(r)
        
        if not theme_competences:
            continue

        dom_codes_in_theme = set()
        for c in theme_competences:
            parts = c['code'].split('-')
            dc = parts[2] if len(parts) > 2 else 'AUTRE'
            dom_codes_in_theme.add(dc)
        
        theme_dict = {
            "id_theme": theme.get('id', ''),
            "nom": theme.get('titre', ''),
            "niveau_besoin": "fort",
            "duree_estimee": len(theme_competences) * 0.5,
            "nb_questions": len(theme_competences),
            "contenu_programme": theme.get('activites', []),
            "domaine_tosa": [domaines_map.get(dc, domaines_map['AUTRE'])['id'] for dc in dom_codes_in_theme],
            "domaine_noms": [domaines_map.get(dc, domaines_map['AUTRE'])['nom'] for dc in dom_codes_in_theme],
            "competences_tosa": [f"[{c['code']}]" for c in theme_competences],
            "competences_noms": [c['nom'] for c in theme_competences],
            "comp_par_domaine": []
        }
        
        for dc in dom_codes_in_theme:
            d_info = domaines_map.get(dc, domaines_map['AUTRE'])
            comps_in_d = [c['nom'] for c in theme_competences if dc in c.get('code', '')]
            theme_dict["comp_par_domaine"].append({
                "id_domaine": d_info['id'],
                "nom_domaine": d_info['nom'],
                "competences": comps_in_d
            })
            
            if dc not in themes_par_domaine_dict:
                themes_par_domaine_dict[dc] = {
                    "id_domaine": d_info['id'],
                    "nom_domaine": d_info['nom'],
                    "themes": []
                }
            themes_par_domaine_dict[dc]["themes"].append(theme_dict)
        
        themes_a_former.append(theme_dict)

    themes_par_domaine = list(themes_par_domaine_dict.values())

    rep_formatted = []
    for r in reponses:
        rep_formatted.append({
            "id_question": f"[{r.get('code', '')}]",
            "acquisition": r.get('maitrise'),
            "besoin": r.get('souhait'),
            "nom": r.get('nom')
        })

    duree_totale = sum(t['duree_estimee'] for t in themes_a_former)
    prix_total = duree_totale * 45

    timestamp = datetime.now()
    nom_cand = candidat.get('nom', 'X').replace(' ', '_')
    prenom_cand = candidat.get('prenom', 'Y').replace(' ', '_')
    
    report = {
        "id_candidat": f"CAND_{nom_cand}_{prenom_cand}_{timestamp.strftime('%Y%m%d_%H%M%S')}",
        "nom_candidat": candidat.get('nom', ''),
        "prenom_candidat": candidat.get('prenom', ''),
        "email_candidat": candidat.get('email', ''),
        "objectifs": candidat.get('objectifs', ''),
        "id_questionnaire": f"AUTO_{formation_id.upper()}_{niveau_id.upper()}",
        "programme_id": target_prog.get('id', ''),
        "programme_nom": target_prog.get('titre', ''),
        "duree_totale_estimee": duree_totale,
        "prix_total_estime": prix_total,
        "orientation_expert": False,
        "themes_a_former": themes_a_former,
        "themes_par_domaine": themes_par_domaine,
        "reponses_par_domaine": [],
        "reponses_par_bloc": [
            {
                "id_bloc": "B1",
                "nom_bloc": "Parcours complet Auto-Positionnement",
                "reponses": rep_formatted
            }
        ]
    }
    
    save_dir = os.path.join(DB_DIR, "rapports_autoposi")
    os.makedirs(save_dir, exist_ok=True)
    filename = f"Rapport_Auto_{nom_cand}_{prenom_cand}_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
    with open(os.path.join(save_dir, filename), 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    return report
