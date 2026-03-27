import sys
import os
import json

# Add webapp to path to import app
sys.path.append(os.path.join(os.path.dirname(__file__), 'webapp'))
from app import IRTEngine

QUESTIONS_PATH = os.path.join(os.path.dirname(__file__), 'db', 'questions')

def simulate_test(niveau_depart, answer_strategy):
    engine = IRTEngine(QUESTIONS_PATH)
    engine.niveau_depart = niveau_depart
    
    if niveau_depart == 'novice':
        print(f"--- Simulation: {niveau_depart.upper()} ---")
        print(" => Résultat direct depuis identification: Novice / EXCEL-INIT (theta = -2.0)")
        print()
        return

    if niveau_depart == 'debutant':
        engine.theta = -0.5
    elif niveau_depart == 'intermediaire':
        engine.theta = 0.5
    elif niveau_depart == 'perfectionnement':
        engine.theta = 1.5
    engine.se = 2.5
    
    print(f"--- Simulation: {niveau_depart.upper()} (Strategies: {answer_strategy.__name__}) ---")
    print(f"Initial: theta = {engine.theta}, SE = {engine.se}")
    
    while not engine.is_finished():
        question = engine.get_next_question()
        if not question:
            break
        answer = answer_strategy(question)
        engine.answer_question(question['_id'], answer)
        
    res = engine.get_results()
    print(f"Final: theta = {res['theta']}, SE = {res['se']}, questions = {res['questions_answered']}")
    print(f"Positionnement: {res['level_name']} ({res['level']}) -> Programme: {res['programme']}")
    print()

def strategy_all_wrong(q): return "WRONG_ANSWER"
def strategy_all_correct(q): return q['reponseCorrecte']
def strategy_mixed_easy_good(q):
    # Repond juste si diff <= 50 (N1, N2 easy)
    if q.get('difficulty', 50) <= 50:
        return q['reponseCorrecte']
    return "WRONG_ANSWER"
def strategy_mixed_hard_good(q):
    # Repond juste si diff > 50 (N2 diff, N3)
    if q.get('difficulty', 50) > 50:
        return q['reponseCorrecte']
    return "WRONG_ANSWER"

def run_tests():
    simulate_test('novice', strategy_all_wrong)
    
    simulate_test('debutant', strategy_all_wrong)
    simulate_test('debutant', strategy_all_correct)
    simulate_test('debutant', strategy_mixed_easy_good)
    
    simulate_test('intermediaire', strategy_all_wrong)
    simulate_test('intermediaire', strategy_all_correct)
    simulate_test('intermediaire', strategy_mixed_easy_good)
    
    simulate_test('perfectionnement', strategy_all_wrong)
    simulate_test('perfectionnement', strategy_all_correct)
    simulate_test('perfectionnement', strategy_mixed_hard_good)

if __name__ == '__main__':
    run_tests()
