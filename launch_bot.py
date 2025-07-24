#!/usr/bin/env python3
"""
Fichier principal - Lance le bot Telegram et le serveur Flask sur Render.com
"""

import os
import logging
import threading

# Configuration des variables d’environnement
os.environ["TELEGRAM_BOT_TOKEN"] = "7749786995:AAGr9rk_uuykLLp5g7Hi3XwIlsdMfW9pWFw"
os.environ["PORT"] = "10000"

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Import du bot Telegram et de l'application Flask
    from render_web import app  # Flask app
    from render_bot import start_bot  # Fonction pour démarrer le bot

    # Démarrage du bot Telegram dans un thread
    threading.Thread(target=start_bot).start()
    logger.info("🤖 Bot Telegram lancé avec succès.")

    # Lancement du serveur Flask
    logger.info(f"🌐 Lancement du serveur Flask sur le port {os.environ['PORT']}...")
    app.run(host="0.0.0.0", port=int(os.environ["PORT"]))

except Exception as e:
    logger.error(f"❌ Erreur au démarrage : {e}")
