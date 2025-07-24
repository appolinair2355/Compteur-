#!/usr/bin/env python3
"""
Fichier principal de lancement du bot Telegram avec Flask pour Render.com
"""

import os
import sys
import logging
import threading
from render_bot import run_bot, run_web  # ✅ Remplace simple_bot et simple_web

# ✅ Configuration du token directement dans le code (évite .env)
os.environ["TELEGRAM_BOT_TOKEN"] = "7749786995:AAGr9rk_uuykLLp5g7Hi3XwIlsdMfW9pWFw"

# ✅ Configuration du port (utile pour Render)
PORT = int(os.getenv("PORT", 10000))  # Utilise 10000 si non défini

try:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info("🚀 Démarrage du bot et du serveur web Flask...")

    # ✅ Lancer le bot dans un thread
    threading.Thread(target=run_bot).start()

    # ✅ Lancer le serveur Flask sur le port défini
    run_web(PORT)

except Exception as e:
    logger.error(f"❌ Erreur au lancement du bot : {e}")
    sys.exit(1)
