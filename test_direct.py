import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'webapp'))
from app import IRTEngine

QUESTIONS_PATH = os.path.join(os.path.dirname(__file__), 'db', 'questions')

irt = IRTEngine(QUESTIONS_PATH)
irt.theta = -0.5
irt.se = 2.5
irt.niveau_depart = 'debutant'

print("Starting fake session for N3 question..")
q_id = "EXCEL-N3-CALCUL-C06-Q07"
q = next((q for q in irt.all_questions if q['_id'] == q_id), None)
print(f"Question: {q['question']}")
print(f"Correct: {q['reponseCorrecte']}")
print(f"Options keys: {list(q['reponses'].keys())}")

# Attempt to answer correctly
irt.answer_question(q_id, q['reponseCorrecte'])

print(f"Theta after correct answer: {irt.theta}")
print(f"SE after correct answer: {irt.se}")
print(f"Is Correct tracked? {irt.answers[q_id]['correct']}")
