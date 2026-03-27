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

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Tableau de bord principal"""
    data = load_data()
    tests_count = len(data.get('tests_recus', []))
    candidats_count = len(data.get('candidats', []))
    programmes_count = len(data.get('programmes_generes', []))
    
    return render_template('dashboard.html',
                         tests_count=tests_count,
                         candidats_count=candidats_count,
                         programmes_count=programmes_count,
                         tests=data.get('tests_recus', []))

@app.route('/candidats')
def candidats():
    """Liste des candidats"""
    data = load_data()
    return render_template('candidats.html', candidats=data.get('candidats', []))

@app.route('/tests')
def tests():
    """Liste des tests reçus"""
    data = load_data()
    return render_template('tests.html', tests=data.get('tests_recus', []))

@app.route('/programmes')
def programmes():
    """Liste des programmes générés"""
    data = load_data()
    return render_template('programmes.html', programmes=data.get('programmes_generes', []))

@app.route('/analyser/<test_id>')
def analyser(test_id):
    """Analyse un test et génère un programme"""
    data = load_data()
    
    # Trouver le test
    test = None
    for t in data.get('tests_recus', []):
        if t.get('id') == test_id:
            test = t
            break
    
    if not test:
        return "Test non trouvé", 404
    
    # Charger les données de référence
    db = load_db('database.json')
    programmes = load_db('programmes.json')
    
    # Analyse simple - à améliorer avec le vrai algorithme
    resultat = {
        'id': f"PROG-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        'test_id': test_id,
        'candidat': test.get('candidat', {}),
        'formation': test.get('formation', ''),
        'niveau': test.get('niveau', ''),
        'score': test.get('score', 0),
        'themes_proposes': [],
        'duree_estimee': 14,
        'tarif_estime': 14 * 45,
        'timestamp': datetime.now().isoformat()
    }
    
    # Sauvegarder le programme généré
    data.setdefault('programmes_generes', []).append(resultat)
    save_data(data)
    
    return redirect(url_for('programmes'))

@app.route('/importer', methods=['GET', 'POST'])
def importer():
    """Import de tests via CSV"""
    if request.method == 'POST':
        # Traitement de l'import CSV
        file = request.files.get('fichier')
        if file:
            # TODO: implémenter le parsing CSV
            return "Import CSV à implémenter"
    
    return render_template('importer.html')

@app.route('/generer-pdf/<programme_id>')
def generer_pdf(programme_id):
    """Génère un PDF du programme"""
    # TODO: implémenter la génération PDF
    return "Génération PDF à implémenter"

@app.route('/generer-excel/<programme_id>')
def generer_excel(programme_id):
    """Génère un Excel du programme"""
    # TODO: implémenter la génération Excel
    return "Génération Excel à implémenter"

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='127.0.0.1', port=port, debug=True)