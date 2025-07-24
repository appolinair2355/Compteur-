#!/usr/bin/env python3
"""
Fichier principal - Lance le bot et le serveur Flask
"""

import os
import logging

# Configuration des variables d’environnement
os.environ["TELEGRAM_BOT_TOKEN"] = "7749786995:AAGr9rk_uuykLLp5g7Hi3XwIlsdMfW9pWFw"
os.environ["PORT"] = "10000"

# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lancement du bot et du serveur Flask
try:
    from render_web import app  # App Flask
    from render_bot import start_bot  # Fonction pour démarrer le bot Telegram

    import threading

    # Lancement du bot Telegram dans un thread séparé
    threading.Thread(target=start_bot).start()

    # Lancement de Flask
    logger.info("🚀 Démarrage du serveur Flask...")
    app.run(host="0.0.0.0", port=int(os.environ["PORT"]))

except Exception as e:
    logger.error(f"❌ Erreur au démarrage : {e}")
