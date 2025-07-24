#!/usr/bin/env python3
"""
Fichier principal : configure l’environnement, le TOKEN, le PORT, et lance l’app Flask
"""
import os
import logging

# Définir manuellement les variables d’environnement
os.environ["TELEGRAM_BOT_TOKEN"] = "7749786995:AAGr9rk_uuykLLp5g7Hi3XwIlsdMfW9pWFw"
os.environ["PORT"] = "10000"
os.environ["WEBHOOK_URL"] = "https://ton-app.onrender.com/webhook"  # à adapter

# Logger
logging.basicConfig(level=logging.INFO)

# Lancer l'app Flask
from render_web import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
