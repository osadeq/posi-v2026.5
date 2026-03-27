import requests
import json

base_url = "http://127.0.0.1:5000"

def run():
    s = requests.Session()
    
    # 1. Identification
    data = {
        "nom": "Test",
        "prenom": "Auto",
        "email": "test@test.com",
        "formation": "1",
        "objectifs": "Test",
        "action_niveau": "test"
    }
    r = s.post(f"{base_url}/identification", data=data, allow_redirects=False)
    if 'irt_engine' not in s.cookies.get_dict().get('session', ''):
        print("Session was not created properly!")
    
    # 2. Get first question from /test-adaptatif pages
    r = s.get(f"{base_url}/test-adaptatif")
    # Actually the easiest is to just hit /api/answer and get the next question
    # But wait, we need the first question ID. It's rendered in the HTML.
    # Let's extract it from HTML...
    html = r.text
    if 'questionId = "' in html:
        q_id = html.split('questionId = "')[1].split('"')[0]
    else:
        print("Could not find questionId in HTML")
        return
    
    # Let's answer perfectly using the local JSON files.
    import os
    qpath = 'db/questions'
    
    print("Starting session...")
    
    for i in range(15):
        # find correct answer
        with open(os.path.join(qpath, f"{q_id}.json"), 'r', encoding='utf-8') as f:
            qd = json.load(f)
            correct_ans = qd.get('reponseCorrecte')
            
        print(f"Q: {q_id} | Sending answer: {correct_ans}")
        # Send API request
        ans_data = {"questionId": q_id, "answer": correct_ans}
        r = s.post(f"{base_url}/api/answer", json=ans_data)
        res = r.json()
        
        if res.get('finished'):
            print("Finished!")
            print(res.get('results'))
            break
        else:
            q_id = res['next_question']['_id']
            print(f"  -> theta: {res['theta']}, SE: {res['se']}")

if __name__ == '__main__':
    run()
