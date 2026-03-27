# Dashboard Admin - Point d'entree portable
# Ce fichier permet de lancer le dashboard sans installation
# Double-cliquez ou lancez: python main.py

import os
import sys

# Ajouter le dossier courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

if __name__ == '__main__':
    print("=" * 50)
    print("  Dashboard Admin - TOSA Positionnement")
    print("=" * 50)
    print()
    print("  Lancement du serveur local...")
    print("  Acces: http://localhost:5001")
    print()
    print("  Pour arreter: Ctrl+C")
    print("=" * 50)
    
    # Port 5001 pour eviter conflit avec webapp
    app.run(host='127.0.0.1', port=5001, debug=True)