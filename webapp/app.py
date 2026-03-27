"""
Webapp Candidate - Test de Positionnement TOSA
Application avec test adaptatif IRT
"""
import json
import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory
from datetime import datetime
from rapport_builder import build_auto_rapport

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tosa-positionnement-key-irt-2024'

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'db')
QUESTIONS_PATH = os.path.join(DB_PATH, 'questions')

def load_json(filename):
    """Charge un fichier JSON depuis le dossier db"""
    path = os.path.join(DB_PATH, filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

# Import IRT Engine
import math

class IRTEngine:
    """Moteur IRT pour test adaptatif"""
    
    def __init__(self, questions_path, max_questions=30, min_se=0.0, min_questions=30):
        self.questions_path = questions_path
        self.max_questions = max_questions
        self.min_se = min_se
        self.min_questions = min_questions
        self.all_questions = self._load_all_questions()
        self.answered_questions = []
        self.theta = 0.0
        self.se = 5.0
        self.theta_history = []
        self.correct_history = []
        self.answers = {}
        self.niveau_depart: str = ""
        
    def _load_all_questions(self):
        questions = []
        if os.path.exists(self.questions_path):
            for filename in os.listdir(self.questions_path):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.questions_path, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        q = json.load(f)
                        q['_id'] = filename.replace('.json', '')
                        questions.append(q)
        return questions
    
    def _prob_correct(self, theta, difficulty, discrimination=1.0, guessing=0.25):
        d = (difficulty - 50) / 10.0
        z = discrimination * (theta - d)
        z = max(-7, min(7, z))
        p = guessing + (1 - guessing) / (1 + math.exp(-z))
        return p
    
    def _update_theta_se(self, question, is_correct):
        difficulty = question.get('difficulty', 50)
        a = question.get('discrimination', 1.0)
        c = question.get('guessing', 0.25)
        
        p = self._prob_correct(self.theta, difficulty, a, c)
        q = 1 - p
        
        if p > 0.001 and p < 0.999:
            info = (a ** 2) * ((p - c) ** 2) / ((1 - c) * p * q + 1e-10)
        else:
            info = 0.001
        
        if info > 0.0001:
            new_se = 1 / math.sqrt(1 / (self.se ** 2) + info)
        else:
            new_se = self.se
        
        learning_rate = max(0.1, min(new_se ** 2, 0.5))
        delta = learning_rate * a * (1 - p) if is_correct else -learning_rate * a * p
        self.theta += delta
        
        self.se = max(0.2, min(3.0, new_se))
        self.theta = max(-3.0, min(3.0, self.theta))
        self.theta_history.append(float(round(self.theta, 3)))
        self.correct_history.append(bool(is_correct))
    
    def get_next_question(self):
        import random
        available = [q for q in self.all_questions if q['_id'] not in self.answered_questions]
        if not available:
            return None
        
        scored_questions = []
        for q in available:
            difficulty = (q.get('difficulty', 50) - 50) / 10.0
            distance = abs(difficulty - self.theta)
            score = -distance + self.se * 0.3
            scored_questions.append((score, q))
            
        scored_questions.sort(key=lambda x: x[0], reverse=True)
        top_candidates = [item[1] for item in scored_questions[:5]]
        
        return random.choice(top_candidates)
    
    def answer_question(self, question_id, answer):
        question = next((q for q in self.all_questions if q['_id'] == question_id), None)
        if not question:
            return
        
        self.answered_questions.append(question_id)
        is_correct = answer == question.get('reponseCorrecte', '')
        self.answers[question_id] = {'answer': answer, 'correct': is_correct}
        self._update_theta_se(question, is_correct)
    
    def is_finished(self):
        if len(self.answered_questions) >= self.max_questions:
            return True
        if self.se <= self.min_se and len(self.answered_questions) >= self.min_questions:
            return True
        return False
    
    def get_level(self):
        """
        Règle unifiée basée uniquement sur theta :
          theta < -0.8  → N0 Novice      → EXCEL-INIT
          theta < 0     → N1 Débutant    → EXCEL-INTER
          theta < 1     → N2 Intermédiaire → EXCEL-PERF
          theta >= 1    → N3 Avancé      → CERTIFICATION_TOSA_EXPERT
        """
        if self.theta < -0.8:
            return "n0", "Novice", "EXCEL-INIT"
        elif self.theta < 0:
            return "n1", "Débutant", "EXCEL-INTER"
        elif self.theta < 1:
            return "n2", "Intermédiaire", "EXCEL-PERF"
        else:
            return "n3", "Avancé", "CERTIFICATION_TOSA_EXPERT"
    
    def get_results(self):
        level_id, level_name, programme = self.get_level()
        return {
            "theta": round(self.theta, 3),
            "se": round(self.se, 3),
            "questions_answered": len(self.answered_questions),
            "level": level_id,
            "level_name": level_name,
            "programme": programme,
            "confidence": max(0, min(100, 100 - self.se * 30))
        }
    
    def to_dict(self):
        """Sérialiser pour la session"""
        return {
            'theta': self.theta,
            'se': self.se,
            'answered_questions': self.answered_questions,
            'theta_history': self.theta_history,
            'correct_history': getattr(self, 'correct_history', []),
            'answers': self.answers,
            'niveau_depart': self.niveau_depart
        }
    
    @classmethod
    def from_dict(cls, data, questions_path):
        """Désérialiser depuis la session"""
        engine = cls(questions_path)
        engine.theta = data.get('theta', 0.0)
        engine.se = data.get('se', 5.0)
        engine.answered_questions = data.get('answered_questions', [])
        engine.theta_history = data.get('theta_history', [])
        engine.correct_history = data.get('correct_history', [])
        engine.answers = data.get('answers', {})
        engine.niveau_depart = data.get('niveau_depart', '')
        return engine


# Load reference data
def get_formations():
    db = load_json('database.json')
    if db and 'formations' in db:
        return [{'id': f['id'], 'nom': f['nom']} for f in db['formations']]
    return []

# Routes
@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'webapp', 'images'), filename)

@app.route('/')
def index():
    return render_template('index.html', formations=get_formations())

@app.route('/identification', methods=['GET', 'POST'])
def identification():
    # Nettoyage pour confidentialité (éviter que le candidat suivant ne voie les données)
    session.pop('last_auto_data', None)
    if request.method == 'POST':
        action = request.form.get('action_niveau', 'test')
        niveau = 'novice' if action == 'novice' else 'debutant'
        
        session['candidat'] = {
            'nom': request.form.get('nom', ''),
            'prenom': request.form.get('prenom', ''),
            'email': request.form.get('email', ''),
            'formation': request.form.get('formation', ''),
            'niveau': niveau,
            'objectifs': request.form.get('objectifs', ''),
            'timestamp': datetime.now().isoformat()
        }
        
        if niveau == 'novice':
            results = {
                "theta": -2.0,
                "se": 0.0,
                "questions_answered": 0,
                "level": "n1",
                "level_name": "Novice",
                "programme": "EXCEL-INIT",
                "confidence": 100
            }
            return render_template('resultats.html', results=results, candidat=session.get('candidat', {}))
        
        irt = IRTEngine(QUESTIONS_PATH)
        irt.niveau_depart = niveau
        
        if niveau == 'debutant':
            irt.theta = -0.5
            irt.se = 2.5
        elif niveau == 'intermediaire':
            irt.theta = 0.5
            irt.se = 2.5
        elif niveau == 'perfectionnement':
            irt.theta = 1.5
            irt.se = 2.5
        
        irt.theta_history = [float(irt.theta)]
        irt.correct_history = [None]
        
        session['irt_engine'] = irt.to_dict()
        return redirect(url_for('test_adaptatif'))
    
    formations = get_formations()
    return render_template('identification.html', formations=formations, niveau_par_defaut='n1')

@app.route('/test-adaptatif')
def test_adaptatif():
    irt_data = session.get('irt_engine')
    if not irt_data:
        return redirect(url_for('identification'))
    
    irt = IRTEngine.from_dict(irt_data, QUESTIONS_PATH)
    question = irt.get_next_question()
    
    if not question or irt.is_finished():
        results = irt.get_results()
        return render_template('resultats.html', 
                            results=results, 
                            candidat=session.get('candidat', {}))
    
    ch = getattr(irt, 'correct_history', [])
    correct_count = sum(1 for c in ch if c is True)
    wrong_count = sum(1 for c in ch if c is False)
    
    return render_template('test_adaptatif.html',
                          question=question,
                          irt_data=irt.to_dict(),
                          progress=len(irt.answered_questions),
                          max_questions=irt.max_questions,
                          theta_history=irt.theta_history,
                          correct_history=ch,
                          correct_count=correct_count,
                          wrong_count=wrong_count,
                          confidence=max(0, min(100, round((1 - irt.se / 5) * 100))))

@app.route('/api/answer', methods=['POST'])
def api_answer():
    data = request.get_json()
    question_id = data.get('questionId')
    answer = data.get('answer')
    
    irt_data = session.get('irt_engine')
    if not irt_data:
        return jsonify({'error': 'Session expirée'}), 400
    
    irt = IRTEngine.from_dict(irt_data, QUESTIONS_PATH)
    irt.answer_question(question_id, answer)
    
    # Save updated engine
    session['irt_engine'] = irt.to_dict()
    
    # Check if finished
    if irt.is_finished():
        results = irt.get_results()
        return jsonify({'finished': True, 'results': results})
    
    # Get next question
    next_q = irt.get_next_question()
    return jsonify({
        'finished': False,
        'theta': irt.theta,
        'se': irt.se,
        'next_question': next_q
    })

@app.route('/resultats')
def resultats():
    irt_data = session.get('irt_engine')
    if not irt_data:
        return redirect(url_for('identification'))
    
    irt = IRTEngine.from_dict(irt_data, QUESTIONS_PATH)
    results = irt.get_results()
    return render_template('resultats.html', 
                        results=results, 
                        candidat=session.get('candidat', {}))

@app.route('/api/niveaux/<formation_id>')
def api_niveaux(formation_id):
    niveaux = []
    db = load_json('database.json')
    if db and 'formations' in db:
        for f in db['formations']:
            if f['id'] == formation_id:
                for n in f.get('niveaux', []):
                    niveaux.append({'id': n['id'], 'nom': n['nom'], 'niveau_tosa': n.get('niveau_tosa', '')})
    return jsonify(niveaux)

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

@app.route('/auto-positionnement')
def auto_positionnement():
    last_data = session.get('last_auto_data', {})
    return render_template('auto_positionnement.html', 
                         formations=get_formations(),
                         last_data=last_data)

@app.route('/soumettre', methods=['POST'])
def soumettre():
    data = request.get_json()
    test_data = {
        'id': f"TEST-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        'candidat': data.get('candidat', {}),
        'formation': data.get('formation', ''),
        'niveau': data.get('niveau', ''),
        'type': data.get('type', 'testPositionnement'),
        'reponses': data.get('reponses', []),
        'timestamp': datetime.now().isoformat()
    }
    
    tests_file = os.path.join(BASE_DIR, 'tests_soumis.json')
    tests = []
    if os.path.exists(tests_file):
        with open(tests_file, 'r', encoding='utf-8') as f:
            tests = json.load(f)
    tests.append(test_data)
    with open(tests_file, 'w', encoding='utf-8') as f:
        json.dump(tests, f, ensure_ascii=False, indent=2)
    
    return jsonify({'success': True})

@app.route('/resultats-auto')
def resultats_auto():
    program = session.get('auto_program')
    if not program:
        return redirect(url_for('auto_positionnement'))
    return render_template('resultats_auto.html', **program)

@app.route('/api/submit-auto', methods=['POST'])
def submit_auto():
    data = request.get_json()
    
    # Save for reflexivity
    session['last_auto_data'] = data
    
    # Generate structured JSON report
    report = build_auto_rapport(data)
    
    session['auto_program'] = report
    return jsonify({'redirect': url_for('resultats_auto')})

@app.route('/api/clear-auto-session', methods=['POST'])
def clear_auto_session():
    session.pop('last_auto_data', None)
    return jsonify({'success': True})

@app.route('/api/auto-questions/<formation_id>/<niveau_id>')
def api_auto_questions(formation_id, niveau_id):
    db = load_json('database.json')
    if db and 'formations' in db:
        for f in db['formations']:
            if f['id'] == formation_id:
                pos = f.get('positionnements', {})
                auto = pos.get('autoPositionnement', {})
                for niv in auto.get('niveaux', []):
                    if niv['id'] == niveau_id:
                        competences = niv.get('competences', [])
                        domaines_map = {
                            'ENV': 'Environnement / Méthodes',
                            'CALCUL': 'Calculs (Formules, Fonctions)',
                            'MFORME': 'Mise en forme',
                            'GDONNEES': 'Gestion des données'
                        }
                        grouped = {}
                        for c in competences:
                            parts = c['code'].split('-')
                            dom_code = parts[2] if len(parts) > 2 else 'AUTRE'
                            dom_name = domaines_map.get(dom_code, dom_code)
                            if dom_name not in grouped:
                                grouped[dom_name] = []
                            grouped[dom_name].append(c)
                        return jsonify(grouped)
    return jsonify({})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)