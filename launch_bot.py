#!/usr/bin/env python3
"""
Fichier principal de lancement du bot et du serveur Flask sur Render.com
"""

import os
from dotenv import load_dotenv
from renderbot import run_bot
from renderweb import run_web

# Charger les variables d'environnement
load_dotenv()

# Configurer manuellement le token et le port si besoin
os.environ["TELEGRAM_BOT_TOKEN"] = os.getenv("TELEGRAM_BOT_TOKEN", "7749786995:AAGr9rk_uuykLLp5g7Hi3XwIlsdMfW9pWFw")
port = int(os.environ.get("PORT", 10000))  # Port par défaut : 10000

if __name__ == "__main__":
    run_bot()
    run_web(port)
