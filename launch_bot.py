import os
import asyncio
import logging
from load_env import load_env
from render_web import start_server_in_background
from render_bot import start_bot

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """Point d'entrée principal pour Render.com"""
    load_env()
    
    # Configuration du port pour Render (déjà défini à 10000)
    render_port = int(os.environ.get("PORT", 10000))
    os.environ["PORT"] = str(render_port)
    
    logger.info(f"🚀 🤖 Joker 3K démarré sur Render.com avec le port {render_port}")
    
    # Démarrer le serveur Flask (render_web.py)
    start_server_in_background()

    # Démarrer le bot principal (render_bot.py)
    await start_bot()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot arrêté par l'utilisateur")
    except Exception as e:
        logger.error(f"❌ Erreur: {e}")
        import time
        time.sleep(30)
