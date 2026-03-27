import os
import json
import re

DB_PATH = r"C:\Users\sadeq\Desktop\posi-v2026.5\db"
BANK_FILE = os.path.join(DB_PATH, "banque-questions-excel.json")
QUESTIONS_DIR = os.path.join(DB_PATH, "questions")

DOMAINS_MAP = {
    "Environnement / Méthodes": "ENV",
    "Calculs & Formules": "CALCUL",
    "Gestion des données": "GDONNEES",
    "Mise en forme": "MFORME"
}

DIFFICULTY_MAP = {
    "N1": 35,
    "N2": 50,
    "N3": 75
}

def clean_html(text):
    if not text:
        return ""
    # Remove MS Office specific tags and standard wrapper p tags if they are trivial
    text = re.sub(r'</?o:p>', '', text)
    text = re.sub(r'class="[^"]*"', '', text)
    text = re.sub(r'style="[^"]*"', '', text)
    # optionally remove empty p tags
    text = re.sub(r'<p>\s*</p>', '', text)
    return text.strip()

def process():
    if not os.path.exists(BANK_FILE):
        print(f"Error: {BANK_FILE} not found.")
        return

    with open(BANK_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions = data.get('questions', [])
    count = 0

    for q in questions:
        niveau = q.get('niveau', 'N1')
        title_dom = q.get('title_domaine', '')
        
        # Determine short domain
        domaine = "INCONNU"
        for key, val in DOMAINS_MAP.items():
            if key in title_dom:
                domaine = val
                break
        
        diff = DIFFICULTY_MAP.get(niveau, 50)
        
        # Build options mapping
        choices = q.get('choices', [])
        reponses = {}
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        id_to_letter = {}
        
        for idx, choice in enumerate(choices):
            if idx < len(letters):
                l = letters[idx]
                reponses[l] = clean_html(choice.get('text', ''))
                id_to_letter[choice.get('id')] = l
        
        correct_ids = q.get('correct_response', [])
        if not correct_ids:
            continue
        correct_l = id_to_letter.get(correct_ids[0], 'A')
        
        feedback = "C'est la bonne réponse."
        fb_dict = q.get('feedback', {})
        if fb_dict and 'correct' in fb_dict:
            feedback = clean_html(fb_dict['correct'])

        # Name format
        qid = str(q.get('id')).zfill(2)
        filename = f"EXCEL-{niveau}-{domaine}-BQ-{qid}.json"
        
        irt_question = {
            "question": clean_html(q.get('text', '')).replace('src="images/', 'src="/images/bq/'),
            "reponses": {k: clean_html(v).replace('src="images/', 'src="/images/bq/') for k, v in reponses.items()},
            "reponseCorrecte": correct_l,
            "feedbackPedagogique": feedback,
            "competencesCibles": [q.get('id_comp', f"EXCEL-{niveau}-{domaine}")] ,
            "difficulty": diff,
            "discrimination": 1.5,
            "guessing": 1.0 / len(choices) if choices else 0.25
        }
        
        # Write file
        out_path = os.path.join(QUESTIONS_DIR, filename)
        with open(out_path, 'w', encoding='utf-8') as out_f:
            json.dump(irt_question, out_f, ensure_ascii=False, indent=2)
            
        count += 1

    print(f"Import finished. {count} new questions written to {QUESTIONS_DIR}.")

if __name__ == "__main__":
    process()
