import logging
from telegram.ext import (
    Application, CommandHandler, ContextTypes
)
from telegram import Update
from render_web import app

# TOKEN direct ici
TOKEN = "7749786995:AAGr9rk_uuykLLp5g7Hi3XwIlsdMfW9pWFw"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Exemple de commande
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot Joker 3K est prêt !")

def start_bot():
    application = Application.builder().token(TOKEN).build()

    # Ajouter des handlers
    application.add_handler(CommandHandler("start", start))

    # Injecter dans render_web
    import render_web
    render_web.telegram_app = application

    # Webhook URL Render
    webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"

    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=webhook_url,
    )
