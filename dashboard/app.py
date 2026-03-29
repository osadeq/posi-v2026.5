"""
Dashboard Admin - Application de gestion des positionnements TOSA
Interface locale pour analyser les tests et générer des programmes personnalisés
"""
import json
import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dashboard-admin-key'

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DASHBOARD_DIR = os.path.join(BASE_DIR, 'dashboard')
DB_PATH = os.path.join(BASE_DIR, 'db')
DATA_FILE = os.path.join(DASHBOARD_DIR, 'data', 'data.json')

def load_data():
    """Charge les données du dashboard"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"candidats": [], "tests_recus": [], "programmes_generes": [], "config": {}}

def save_data(data):
    """Sauvegarde les données du dashboard"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_db(filename):
    """Charge un fichier de la base de données"""
    path = os.path.join(DB_PATH, filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def load_question(question_id):
    """Charge une question depuis le dossier db/questions"""
    q_path = os.path.join(DB_PATH, 'questions', f'{question_id}.json')
    if os.path.exists(q_path):
        with open(q_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def build_programme_from_test(test):
    """Construit un programme de formation basé sur les résultats du test"""
    niveau = test.get('level', test.get('niveau', 'n1'))
    formation = test.get('formation', 'excel')
    reponses = test.get('reponses', [])
    theta = test.get('theta', 0)
    
    level_map = {
        'novice': 'EXCEL-INIT',
        'n0': 'EXCEL-INIT',
        'debutant': 'EXCEL-INTER', 
        'n1': 'EXCEL-INTER',
        'n2': 'EXCEL-PERF',
        'n3': 'CERTIFICATION_TOSA_EXPERT'
    }
    
    prog_id = level_map.get(niveau, 'EXCEL-INTER')
    
    programmes = load_db('programmes.json') or []
    target_prog = next((p for p in programmes if p.get('id') == prog_id), None)
    if not target_prog and programmes:
        target_prog = programmes[0]
    if not target_prog:
        return None
    
    questions_data = {}
    for rep in reponses:
        qid = rep.get('questionId', '')
        if qid:
            q_data = load_question(qid)
            if q_data:
                questions_data[qid] = q_data
    
    domaines_map = {
        'ENV': {'id': 'D1', 'nom': 'Environnement / Méthodes'},
        'CALCUL': {'id': 'D2', 'nom': 'Calculs & Formules'},
        'MFORME': {'id': 'D3', 'nom': 'Mise en forme'},
        'GDONNEES': {'id': 'D4', 'nom': 'Gestion des données'}
    }
    
    correct_competences = []
    for rep in reponses:
        qid = rep.get('questionId', '')
        if qid in questions_data:
            q = questions_data[qid]
            if rep.get('reponse') == q.get('reponseCorrecte'):
                for comp in q.get('competencesCibles', []):
                    if comp not in correct_competences:
                        correct_competences.append(comp)
    
    themes_a_former = []
    themes_par_domaine_dict = {}
    
    for theme in target_prog.get('themes', []):
        theme_competences = []
        theme_code = theme.get('id', '')
        
        for cibl in theme.get('competencesCibles', []):
            if cibl not in correct_competences:
                competence = {
                    'code': cibl,
                    'nom': cibl,
                    'maitrise': 'Non acquise',
                    'souhait': 'Oui'
                }
                if competence not in theme_competences:
                    theme_competences.append(competence)
        
        if not theme_competences:
            continue
        
        dom_codes_in_theme = set()
        for c in theme_competences:
            parts = c['code'].split('-')
            dc = parts[2] if len(parts) > 2 else 'ENV'
            dom_codes_in_theme.add(dc)
        
        theme_dict = {
            "id_theme": theme.get('id', ''),
            "nom": theme.get('titre', ''),
            "niveau_besoin": "fort",
            "duree_estimee": len(theme_competences) * 0.5,
            "nb_questions": len(theme_competences),
            "contenu_programme": theme.get('activites', []),
            "description": theme.get('description', ''),
            "domaine_tosa": [domaines_map.get(dc, {'id': 'D1', 'nom': 'Environnement'})['id'] for dc in dom_codes_in_theme],
            "domaine_noms": [domaines_map.get(dc, {'id': 'D1', 'nom': 'Environnement'})['nom'] for dc in dom_codes_in_theme],
            "competences_tosa": [f"[{c['code']}]" for c in theme_competences],
            "competences_noms": [c['nom'] for c in theme_competences],
            "comp_par_domaine": []
        }
        
        for dc in dom_codes_in_theme:
            d_info = domaines_map.get(dc, {'id': 'D1', 'nom': 'Environnement'})
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
    
    duree_totale = sum(t['duree_estimee'] for t in themes_a_former)
    cout_total = duree_totale * 45
    
    programme = {
        'id': f"PROG-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        'test_id': test.get('id', ''),
        'candidat': test.get('candidat', {}),
        'formation': formation,
        'niveau': niveau,
        'theta': theta,
        'score': test.get('score', 0),
        'programme_id': target_prog.get('id', ''),
        'programme_nom': target_prog.get('titre', ''),
        'themes': themes_a_former,
        'themes_par_domaine': list(themes_par_domaine_dict.values()),
        'duree_estimee': round(duree_totale, 1),
        'cout_estime': round(cout_total, 2),
        'objectifs': test.get('candidat', {}).get('objectifs', ''),
        'timestamp': datetime.now().isoformat()
    }
    
    return programme

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Tableau de bord principal"""
    data = load_data()
    tests_count = len(data.get('tests_recus', []))
    candidats_count = len(data.get('candidats', []))
    programmes_count = len(data.get('programmes_generes', []))
    
    besoins_count = {'fort': 0, 'moyen': 0, 'faible': 0}
    for prog in data.get('programmes_generes', []):
        for theme in prog.get('themes', []):
            niveau = theme.get('niveau_besoin', 'moyen')
            if niveau in besoins_count:
                besoins_count[niveau] += 1
    
    total_besoins = sum(besoins_count.values())
    besoins_pct = {
        'fort': round(besoins_count['fort'] / total_besoins * 100, 1) if total_besoins > 0 else 0,
        'moyen': round(besoins_count['moyen'] / total_besoins * 100, 1) if total_besoins > 0 else 0,
        'faible': round(besoins_count['faible'] / total_besoins * 100, 1) if total_besoins > 0 else 0
    }
    
    return render_template('dashboard.html',
                         tests_count=tests_count,
                         candidats_count=candidats_count,
                         programmes_count=programmes_count,
                         tests=data.get('tests_recus', []),
                         besoins_count=besoins_count,
                         besoins_pct=besoins_pct)

@app.route('/candidats')
def candidats():
    """Liste des candidats"""
    data = load_data()
    return render_template('candidats.html', candidats=data.get('candidats', []))

@app.route('/tests')
def tests():
    """Liste des tests reçus"""
    data = load_data()
    tests_list = data.get('tests_recus', [])
    
    time_periods = []
    for test in tests_list:
        ts = test.get('timestamp', '')
        if ts:
            try:
                from datetime import datetime
                dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                period = dt.strftime('%Y-%m')
                if period not in time_periods:
                    time_periods.append(period)
            except:
                pass
    time_periods.sort(reverse=True)
    
    return render_template('tests.html', tests=tests_list, time_periods=time_periods)

@app.route('/programmes')
def programmes():
    """Liste des programmes générés"""
    data = load_data()
    return render_template('programmes.html', programmes=data.get('programmes_generes', []))

@app.route('/analyser/<test_id>')
def analyser(test_id):
    """Affiche les détails d'un test avec le programme généré"""
    data = load_data()
    
    test = None
    for t in data.get('tests_recus', []):
        if t.get('id') == test_id:
            test = t
            break
    
    if not test:
        return "Test non trouvé", 404
    
    existing_prog = next((p for p in data.get('programmes_generes', []) if p.get('test_id') == test_id), None)
    
    if not existing_prog:
        existing_prog = build_programme_from_test(test)
        if existing_prog:
            data.setdefault('programmes_generes', []).append(existing_prog)
            save_data(data)
    
    theta_history = test.get('theta_history', [])
    correct_history = test.get('correct_history', [])
    
    return render_template('test_detail.html', 
                         test=test,
                         programme=existing_prog,
                         theta_history=theta_history,
                         correct_history=correct_history)

@app.route('/generer-programme/<test_id>')
def generer_programme(test_id):
    """Génère un programme pour un test"""
    data = load_data()
    
    test = None
    for t in data.get('tests_recus', []):
        if t.get('id') == test_id:
            test = t
            break
    
    if not test:
        return "Test non trouvé", 404
    
    resultat = build_programme_from_test(test)
    
    if not resultat:
        resultat = {
            'id': f"PROG-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'test_id': test_id,
            'candidat': test.get('candidat', {}),
            'formation': test.get('formation', ''),
            'niveau': test.get('niveau', ''),
            'score': test.get('score', 0),
            'themes': [],
            'duree_estimee': 0,
            'cout_estime': 0,
            'timestamp': datetime.now().isoformat()
        }
    
    data.setdefault('programmes_generes', []).append(resultat)
    save_data(data)
    
    return redirect(url_for('programmes'))

@app.route('/importer', methods=['GET', 'POST'])
def importer():
    """Import de tests via CSV"""
    if request.method == 'POST':
        file = request.files.get('fichier')
        if file:
            try:
                import csv
                import io
                data = load_data()
                
                stream = io.StringIO(file.stream.read().decode('UTF-8'), newline=None)
                reader = csv.reader(stream)
                header = next(reader, None)
                
                if not header:
                    return "Fichier CSV vide"
                
                imported = 0
                for row in reader:
                    if len(row) >= 6:
                        test = {
                            'id': f"TEST-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{imported}",
                            'candidat': {
                                'nom': row[0].strip() if len(row) > 0 else '',
                                'prenom': row[1].strip() if len(row) > 1 else '',
                                'email': row[2].strip() if len(row) > 2 else ''
                            },
                            'formation': row[3].strip().lower() if len(row) > 3 else 'excel',
                            'niveau': row[4].strip().lower() if len(row) > 4 else 'n1',
                            'type': row[5].strip() if len(row) > 5 else 'testPositionnement',
                            'reponses': [],
                            'timestamp': datetime.now().isoformat()
                        }
                        
                        for i, col in enumerate(row[6:], start=1):
                            if col.strip():
                                test['reponses'].append({
                                    'questionId': f'Q{i:02d}',
                                    'reponse': col.strip()
                                })
                        
                        data.setdefault('tests_recus', []).append(test)
                        imported += 1
                
                save_data(data)
                return render_template('importer.html', message=f"{imported} test(s) importé(s) avec succès!")
            except Exception as e:
                return render_template('importer.html', error=f"Erreur: {str(e)}")
    
    return render_template('importer.html')

@app.route('/generer-pdf/<programme_id>')
def generer_pdf(programme_id):
    """Génère un PDF du programme"""
    data = load_data()
    programme = next((p for p in data.get('programmes_generes', []) if p.get('id') == programme_id), None)
    
    if not programme:
        return "Programme non trouvé", 404
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Programme de formation - {programme.get('candidat', {}).get('nom', '')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 40px; }}
        h1 {{ color: #2563EB; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background: #2563EB; color: white; }}
        .badge {{ padding: 4px 8px; border-radius: 4px; font-size: 12px; }}
        .fort {{ background: #FEE2E2; color: #991B1B; }}
        .moyen {{ background: #FEF3C7; color: #92400E; }}
        .faible {{ background: #D1FAE5; color: #065F46; }}
    </style>
</head>
<body>
    <h1>Programme de Formation</h1>
    <p><strong>Candidat:</strong> {programme.get('candidat', {}).get('nom', '')} {programme.get('candidat', {}).get('prenom', '')}</p>
    <p><strong>Formation:</strong> {programme.get('formation', '').upper()}</p>
    <p><strong>Date:</strong> {programme.get('timestamp', '')[:10]}</p>
    
    <h2>Themes</h2>
    <table>
        <tr>
            <th>Theme</th>
            <th>Description</th>
            <th>Durée</th>
            <th>Coût</th>
            <th> Niveau Besoin</th>
        </tr>
"""
    
    total_duree = 0
    total_cout = 0
    
    for theme in programme.get('themes', []):
        duree = theme.get('duree_estimee', 0) or 0
        cout = duree * 45
        total_duree += duree
        total_cout += cout
        besoin = theme.get('niveau_besoin', 'moyen')
        desc = theme.get('description', '')[:100] if theme.get('description') else ''
        
        html += f"""        <tr>
            <td>{theme.get('nom', '')}</td>
            <td>{desc}...</td>
            <td>{duree}h</td>
            <td>{cout}€</td>
            <td><span class="badge {besoin}">{besoin.upper()}</span></td>
        </tr>
"""
    
    total_cout = total_duree * 45
    html += f"""    </table>
    <h3 style="margin-top: 20px;">Total: {total_duree}h - {total_cout}€</h3>
</body>
</html>"""
    
    from flask import make_response
    response = make_response(html)
    response.headers['Content-Type'] = 'text/html'
    response.headers['Content-Disposition'] = f'attachment; filename=programme_{programme_id}.html'
    return response

@app.route('/generer-excel/<programme_id>')
def generer_excel(programme_id):
    """Génère un Excel du programme"""
    import csv
    import io
    from flask import make_response
    
    data = load_data()
    programme = next((p for p in data.get('programmes_generes', []) if p.get('id') == programme_id), None)
    
    if not programme:
        return "Programme non trouvé", 404
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['Programme de Formation TOSA'])
    writer.writerow(['Candidat', f"{programme.get('candidat', {}).get('nom', '')} {programme.get('candidat', {}).get('prenom', '')}"])
    writer.writerow(['Formation', programme.get('formation', '').upper()])
    writer.writerow(['Date', programme.get('timestamp', '')[:10]])
    writer.writerow([])
    writer.writerow(['Thème', 'Description', 'Durée (h)', 'Coût (€)', 'Niveau Besoin'])
    
    total_duree = 0
    total_cout = 0
    
    for theme in programme.get('themes', []):
        duree = theme.get('duree_estimee', 0) or 0
        cout = duree * 45
        total_duree += duree
        total_cout += cout
        
        writer.writerow([
            theme.get('nom', ''),
            theme.get('description', '').replace('\n', ' ')[:100] if theme.get('description') else '',
            duree,
            cout,
            theme.get('niveau_besoin', 'moyen').upper()
        ])
    
    total_cout = total_duree * 45
    writer.writerow([])
    writer.writerow(['TOTAL', '', total_duree, total_cout, ''])
    
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename=programme_{programme_id}.csv'
    return response

@app.route('/stats')
def stats():
    """Statistiques globales"""
    data = load_data()
    return jsonify({
        'total_tests': len(data.get('tests_recus', [])),
        'total_candidats': len(data.get('candidats', [])),
        'total_programmes': len(data.get('programmes_generes', []))
    })

# ==================== FONCTIONS UTILITAIRES ====================

@app.route('/api/charger-tests')
def api_charger_tests():
    """Charge les tests soumis depuis la webapp"""
    tests_file = os.path.join(BASE_DIR, 'tests_soumis.json')
    if os.path.exists(tests_file):
        with open(tests_file, 'r', encoding='utf-8') as f:
            submitted_tests = json.load(f)
        
        # Ajouter à la liste des tests reçus
        data = load_data()
        for test in submitted_tests:
            # Vérifier si pas déjà présent
            existing = [t for t in data.get('tests_recus', []) if t.get('id') == test.get('id')]
            if not existing:
                data.setdefault('tests_recus', []).append(test)
        
        save_data(data)
        
        return jsonify({'success': True, 'count': len(submitted_tests)})
    
    return jsonify({'success': True, 'count': 0})

# ==================== CRUD CANDIDATS ====================

@app.route('/candidat/nouveau', methods=['GET', 'POST'])
def candidat_nouveau():
    """Créer un nouveau candidat"""
    if request.method == 'POST':
        data = load_data()
        candidat = {
            'id': f"CAND-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'nom': request.form.get('nom', ''),
            'prenom': request.form.get('prenom', ''),
            'email': request.form.get('email', ''),
            'telephone': request.form.get('telephone', ''),
            'entreprise': request.form.get('entreprise', ''),
            'objectifs': request.form.get('objectifs', ''),
            'timestamp': datetime.now().isoformat()
        }
        data.setdefault('candidats', []).append(candidat)
        save_data(data)
        return redirect(url_for('candidats'))
    
    return render_template('candidat_edit.html', candidat=None)

@app.route('/candidat/<candidat_id>', methods=['GET', 'POST'])
def candidat_edit(candidat_id):
    """Modifier un candidat"""
    data = load_data()
    candidat = next((c for c in data.get('candidats', []) if c.get('id') == candidat_id), None)
    
    if request.method == 'POST':
        if candidat:
            candidat['nom'] = request.form.get('nom', '')
            candidat['prenom'] = request.form.get('prenom', '')
            candidat['email'] = request.form.get('email', '')
            candidat['telephone'] = request.form.get('telephone', '')
            candidat['entreprise'] = request.form.get('entreprise', '')
            candidat['objectifs'] = request.form.get('objectifs', '')
            save_data(data)
        return redirect(url_for('candidats'))
    
    return render_template('candidat_edit.html', candidat=candidat)

@app.route('/candidat/<candidat_id>/supprimer', methods=['POST'])
def candidat_delete(candidat_id):
    """Supprimer un candidat"""
    data = load_data()
    data['candidats'] = [c for c in data.get('candidats', []) if c.get('id') != candidat_id]
    save_data(data)
    return redirect(url_for('candidats'))

# ==================== CRUD TESTS ====================

@app.route('/test/nouveau', methods=['GET', 'POST'])
def test_nouveau():
    """Créer un nouveau test"""
    if request.method == 'POST':
        data = load_data()
        test = {
            'id': f"TEST-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'candidat': {
                'nom': request.form.get('nom', ''),
                'prenom': request.form.get('prenom', ''),
                'email': request.form.get('email', '')
            },
            'formation': request.form.get('formation', 'excel'),
            'niveau': request.form.get('niveau', 'n1'),
            'type': request.form.get('type', 'testPositionnement'),
            'reponses': [],
            'timestamp': datetime.now().isoformat()
        }
        data.setdefault('tests_recus', []).append(test)
        save_data(data)
        return redirect(url_for('tests'))
    
    return render_template('test_edit.html', test=None)

@app.route('/test/<test_id>', methods=['GET', 'POST'])
def test_edit(test_id):
    """Modifier un test"""
    data = load_data()
    test = next((t for t in data.get('tests_recus', []) if t.get('id') == test_id), None)
    
    if request.method == 'POST':
        if test:
            test['candidat']['nom'] = request.form.get('nom', '')
            test['candidat']['prenom'] = request.form.get('prenom', '')
            test['candidat']['email'] = request.form.get('email', '')
            test['formation'] = request.form.get('formation', 'excel')
            test['niveau'] = request.form.get('niveau', 'n1')
            test['type'] = request.form.get('type', 'testPositionnement')
            save_data(data)
        return redirect(url_for('tests'))
    
    return render_template('test_edit.html', test=test)

@app.route('/test/<test_id>/supprimer', methods=['POST'])
def test_delete(test_id):
    """Supprimer un test"""
    data = load_data()
    data['tests_recus'] = [t for t in data.get('tests_recus', []) if t.get('id') != test_id]
    data['programmes_generes'] = [p for p in data.get('programmes_generes', []) if p.get('test_id') != test_id]
    save_data(data)
    return redirect(url_for('tests'))

# ==================== CRUD PROGRAMMES ====================

@app.route('/programme/<programme_id>', methods=['GET', 'POST'])
def programme_edit(programme_id):
    """Modifier un programme"""
    data = load_data()
    programme = next((p for p in data.get('programmes_generes', []) if p.get('id') == programme_id), None)
    
    if request.method == 'POST':
        if programme:
            programme['duree_estimee'] = float(request.form.get('duree_estimee', 0))
            programme['cout_estime'] = float(request.form.get('cout_estime', 0))
            save_data(data)
        return redirect(url_for('programmes'))
    
    return render_template('programme_edit.html', programme=programme)

@app.route('/programme/<programme_id>/supprimer', methods=['POST'])
def programme_delete(programme_id):
    """Supprimer un programme"""
    data = load_data()
    data['programmes_generes'] = [p for p in data.get('programmes_generes', []) if p.get('id') != programme_id]
    save_data(data)
    return redirect(url_for('programmes'))

@app.route('/programme/<programme_id>/dupliquer', methods=['POST'])
def programme_dupliquer(programme_id):
    """Dupliquer un programme"""
    data = load_data()
    programme = next((p for p in data.get('programmes_generes', []) if p.get('id') == programme_id), None)
    
    if programme:
        import copy
        new_prog = copy.deepcopy(programme)
        new_prog['id'] = f"PROG-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        new_prog['timestamp'] = datetime.now().isoformat()
        data.setdefault('programmes_generes', []).append(new_prog)
        save_data(data)
    
    return redirect(url_for('programmes'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='127.0.0.1', port=port, debug=True)