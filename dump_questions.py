import json
import os

qpath = 'db/questions'
with open('questions_dump.txt', 'w', encoding='utf-8') as out:
    for f in sorted(os.listdir(qpath)):
        if not f.endswith('.json'):
            continue
        p = os.path.join(qpath, f)
        with open(p, 'r', encoding='utf-8') as jf:
            d = json.load(jf)
            out.write(f"=== {f} ===\n")
            out.write(f"Q: {d.get('titre')}\n")
            out.write("Options:\n")
            for i, opt in enumerate(d.get('options', [])):
                out.write(f"  - {opt}\n")
            out.write(f"Correct: {d.get('reponseCorrecte')}\n\n")
