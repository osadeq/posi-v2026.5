import subprocess
import time
import requests
import json
import os

def run_live_test():
    # Démarrer le serveur
    print("Démarrage du serveur Flask...")
    python_exe = os.path.abspath(os.path.join('webapp', 'venv', 'Scripts', 'python.exe'))
    server = subprocess.Popen([python_exe, 'app.py'], cwd='webapp', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(3) # Wait for startup
    
    base_url = "http://127.0.0.1:5000"
    s = requests.Session()
    
    # Etape 1: Identification (Je passe le test -> debutant)
    data = {"nom": "Test", "prenom": "User", "email": "test@test.com", "formation": "1", "action_niveau": "test", "objectifs": ""}
    r = s.post(f"{base_url}/identification", data=data)
    
    # Etape 2: Get HTML of first test question
    r = s.get(f"{base_url}/test-adaptatif")
    html = r.text
    if 'questionId = "' not in html:
        print("Erreur HTML:", html[:200])
        server.terminate()
        return
        
    q_id = html.split('questionId = "')[1].split('"')[0]
    print(f"Premiere question: {q_id}")
    
    qpath = 'db/questions'
    for i in range(15):
        # Find correct answer
        fpath = os.path.join(qpath, f"{q_id}.json")
        with open(fpath, 'r', encoding='utf-8') as f:
            qd = json.load(f)
            correct_ans = qd.get('reponseCorrecte')
            
        print(f"[{i+1}] Répondre {correct_ans} à la {q_id}...")
        res = s.post(f"{base_url}/api/answer", json={"questionId": q_id, "answer": correct_ans}).json()
        
        if res.get('finished'):
            print("FIN DU TEST !")
            r2 = s.get(f"{base_url}/resultats")
            print("NIVEAU:", "Novice" if "Novice" in r2.text else "Autre")
            break
        else:
            print(f"  -> Theta: {res['theta']}, SE: {res['se']}")
            q_id = res['next_question']['_id']

    server.terminate()
    print("Test terminé.")

if __name__ == '__main__':
    run_live_test()
