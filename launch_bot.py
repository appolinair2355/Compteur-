import os
import asyncio
import logging
import nest_asyncio
from load_env import load_env
from render_web import app
from render_bot import start_bot

from threading import Thread
from werkzeug.serving import run_simple

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Patch la boucle déjà active (Render)
nest_asyncio.apply()

def start_server_in_background():
    def run():
        run_simple('0.0.0.0', int(os.getenv("PORT", 10000)), app, use_reloader=False)
    Thread(target=run).start()

async def main():
    load_env()
    logger.info("🚀 Lancement du serveur Flask")
    start_server_in_background()
    logger.info("🤖 Démarrage du bot Telegram")
    await start_bot()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot arrêté manuellement")
    except Exception as e:
        logger.error(f"❌ Erreur : {e}")
