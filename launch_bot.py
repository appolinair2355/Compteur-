#!/usr/bin/env python3
"""
Fichier principal - Lance le bot et le serveur Flask pour Render
"""

import os
import logging
import threading

# TOKEN directement ici
TOKEN = "7749786995:AAGr9rk_uuykLLp5g7Hi3XwIlsdMfW9pWFw"
PORT = "10000"

os.environ["TELEGRAM_BOT_TOKEN"] = TOKEN
os.environ["PORT"] = PORT

# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from render_web import app  # Flask app
    from render_bot import start_bot  # Fonction de démarrage du bot

    # Lancer le bot dans un thread séparé
    threading.Thread(target=start_bot).start()

    # Lancer Flask
    logger.info("🚀 Serveur Flask en cours d'exécution...")
    app.run(host="0.0.0.0", port=int(PORT))

except Exception as e:
    logger.error(f"❌ Erreur au démarrage : {e}")
