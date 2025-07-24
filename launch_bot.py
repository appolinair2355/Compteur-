#!/usr/bin/env python3
"""
Fichier principal : configure l'environnement et démarre Flask ou Bot
"""
import os
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

# Forcer le port Render
os.environ['PORT'] = '10000'

# Démarrage du serveur Flask (Webhook)
from render_web import app  # app = Flask app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
