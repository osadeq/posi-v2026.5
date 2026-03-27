import json
import os

qpath = 'db/questions'
with open('questions_dump_v2.txt', 'w', encoding='utf-8') as out:
    for f in sorted(os.listdir(qpath)):
        if not f.endswith('.json'):
            continue
        p = os.path.join(qpath, f)
        with open(p, 'r', encoding='utf-8') as jf:
            d = json.load(jf)
            out.write(f"=== {f} ===\n")
            out.write(f"Q: {d.get('question')}\n")
            out.write("Reponses:\n")
            for k, v in d.get('reponses', {}).items():
                out.write(f"  {k}: {v}\n")
            out.write(f"Correct: {d.get('reponseCorrecte')}\n")
            out.write(f"Feedback: {d.get('feedbackPedagogique')}\n\n")
