"""
Module IRT - Test Adaptatif
Algorithme de Item Response Theory pour test adaptatif
"""
import math
import json
import os

class IRTEngine:
    """Moteur IRT pour test adaptatif"""
    
    def __init__(self, questions_db_path, max_questions=30, min_se=0.3):
        self.questions_db_path = questions_db_path
        self.max_questions = max_questions
        self.min_se = min_se
        
        # Load all questions
        self.all_questions = self._load_all_questions()
        self.answered_questions = []
        
        # Initial estimates
        self.theta = 0.0  # Ability estimate
        self.se = 5.0    # Standard error
        
    def _load_all_questions(self):
        """Charge toutes les questions depuis le dossier db/questions/"""
        questions = []
        if os.path.exists(self.questions_db_path):
            for filename in os.listdir(self.questions_db_path):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.questions_db_path, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        q = json.load(f)
                        q['_id'] = filename.replace('.json', '')
                        questions.append(q)
        return questions
    
    def _prob_correct(self, theta, difficulty, discrimination=1.0, guessing=0.25):
        """Calcule la probabilité de bonne réponse (modèle 2PL)"""
        # logistic function
        z = discrimination * (theta - difficulty / 100.0 * 10 - 5)  # Scale difficulty to -5 to 5
        # Bound z to prevent overflow
        z = max(-10, min(10, z))
        p = guessing + (1 - guessing) / (1 + math.exp(-z))
        return p
    
    def _update_theta_se(self, question, is_correct):
        """Met à jour THETA et SE après une réponse (MAP estimation)"""
        b = question.get('difficulty', 50) / 100.0 * 10 - 5  # Scale to -5 to 5
        a = question.get('discrimination', 1.0)
        c = question.get('guessing', 0.25)
        
        p = self._prob_correct(self.theta, question.get('difficulty', 50), a, c)
        q = 1 - p
        
        # Information at this point
        I = a**2 * (p - c) * (q) / (c + (1 - c) * p * q)
        
        # Update SE
        if I > 0:
            new_se = 1 / math.sqrt(1 / (self.se**2) + I)
        else:
            new_se = self.se
        
        # Update theta with a minimum learning rate of 0.1
        learning_rate = max(0.1, min(new_se**2, 0.5))
        if is_correct:
            self.theta += learning_rate * a * (1 - p) / p
        else:
            self.theta -= learning_rate * a * (p - c) / (1 - p)
        
        self.se = new_se
        
        # Clamp theta to reasonable range
        self.theta = max(-5, min(5, self.theta))
    
    def get_next_question(self):
        """Sélectionne la prochaine question optimisant l'information"""
        import random
        # Filter out already answered questions
        available = [q for q in self.all_questions if q['_id'] not in self.answered_questions]
        
        if not available:
            return None
        
        scored_questions = []
        for q in available:
            difficulty = q.get('difficulty', 50) / 100.0 * 10 - 5
            distance = abs(difficulty - self.theta)
            
            # Weight: closer to theta = better, but also consider SE
            # If SE is large, prefer questions closer to theta
            # If SE is small, can afford to explore
            score = -distance + self.se * 0.5
            scored_questions.append((score, q))
            
        scored_questions.sort(key=lambda x: x[0], reverse=True)
        top_candidates = [item[1] for item in scored_questions[:5]]
        
        return random.choice(top_candidates)
    
    def answer_question(self, question_id, answer):
        """Enregistre une réponse et met à jour les estimations"""
        # Find question
        question = next((q for q in self.all_questions if q['_id'] == question_id), None)
        if not question:
            return
        
        self.answered_questions.append(question_id)
        
        # Check if correct
        is_correct = answer == question.get('reponseCorrecte', '')
        
        # Update theta and SE
        self._update_theta_se(question, is_correct)
    
    def is_finished(self):
        """Vérifie si le test doit s'arrêter"""
        # Stop if SE is small enough (confident)
        if self.se <= self.min_se:
            return True
        
        # Stop if max questions reached
        if len(self.answered_questions) >= self.max_questions:
            return True
        
        return False
    
    def get_level(self):
        """Convertit THETA en niveau TOSA"""
        # Theta range: -5 (very low) to 5 (very high)
        # Map to N1/N2/N3
        if self.theta < -1.5:
            return "n1", "Initiation"
        elif self.theta < 1.5:
            return "n2", "Intermédiaire"
        else:
            return "n3", "Perfectionnement"
    
    def get_results(self):
        """Retourne les résultats du test"""
        level_id, level_name = self.get_level()
        
        return {
            "theta": round(self.theta, 3),
            "se": round(self.se, 3),
            "questions_answered": len(self.answered_questions),
            "level": level_id,
            "level_name": level_name,
            "confidence": max(0, min(100, 100 - self.se * 20))
        }
    
    def get_all_questions(self):
        """Retourne toutes les questions avec leur statut de réponse"""
        result = []
        for q in self.all_questions:
            answered = q['_id'] in self.answered_questions
            # Find the answer if answered
            answer = None
            is_correct = None
            if answered:
                # We'd need to track answers separately - for now mark as answered
                answer = "answered"
            
            result.append({
                "id": q['_id'],
                "question": q.get('question', ''),
                "difficulty": q.get('difficulty', 50),
                "answered": answered
            })
        return result


def create_engine(questions_path):
    """Factory function to create IRT engine"""
    return IRTEngine(questions_path)