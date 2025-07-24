#!/usr/bin/env python3
"""
Production bot for Render.com deployment - Updated 2025
"""
import os
import logging
import sys
import signal
import threading
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
from compteur import get_compteurs, update_compteurs, reset_compteurs_canal
from style import afficher_compteurs_canal
from simple_web import app
import re
import json

# ✅ Token intégré directement ici
TOKEN = "7749786995:AAGr9rk_uuykLLp5g7Hi3XwIlsdMfW9pWFw"

# Track processed messages per channel
processed_messages = set()

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

style_affichage = 1
app_instance = None

def save_bot_status(running, message=None, error=None):
    try:
        with open("bot_status.json", "w") as f:
            json.dump({
                "running": running,
                "last_message": message,
                "error": error
            }, f)
    except Exception as e:
        logger.error(f"Could not save status: {e}")

def is_message_processed(message_key):
    return message_key in processed_messages

def mark_message_processed(message_key):
    processed_messages.add(message_key)

def load_processed_messages():
    global processed_messages
    try:
        with open("processed_messages.json", "r") as f:
            processed_messages = set(json.load(f))
    except:
        processed_messages = set()

def save_processed_messages():
    try:
        with open("processed_messages.json", "w") as f:
            json.dump(list(processed_messages), f)
    except:
        pass

def signal_handler(sig, frame):
    logger.info("Shutting down...")
    save_bot_status(False, "Bot stopped")
    if app_instance:
        app_instance.stop()
    sys.exit(0)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global style_affichage

    msg = update.message or update.channel_post or update.edited_channel_post or update.edited_message
    if not msg or not msg.text:
        return

    text = msg.text
    chat_id = msg.chat_id
    is_edited = update.edited_channel_post or update.edited_message

    match_numero = re.search(r"#n(\d+)", text)
    if not match_numero:
        match = re.search(r'\(([^()]*)\)', text)
        if not match:
            return
        content = match.group(1)
    else:
        numero = int(match_numero.group(1))
        message_key = f"{chat_id}_{numero}"
        progress_indicators = ['⏰', '▶', '🕐', '➡️']
        confirmation_symbols = ['✅', '🔰']

        has_progress = any(i in text for i in progress_indicators)
        has_confirmation = any(c in text for c in confirmation_symbols)

        if has_progress and not has_confirmation:
            return

        if is_message_processed(message_key) and not is_edited:
            return

        mark_message_processed(message_key)
        save_processed_messages()

        match = re.search(r'\(([^()]*)\)', text)
        if not match:
            return
        content = match.group(1)

    cards_found = {}
    total_cards = 0
    heart_count = content.count("❤️") + content.count("♥️")
    if heart_count:
        update_compteurs(chat_id, "❤️", heart_count)
        cards_found["❤️"] = heart_count
        total_cards += heart_count

    for symbol in ["♦️", "♣️", "♠️"]:
        count = content.count(symbol)
        if count:
            update_compteurs(chat_id, symbol, count)
            cards_found[symbol] = count
            total_cards += count

    if not cards_found:
        return

    compteurs_updated = get_compteurs(chat_id)
    response = afficher_compteurs_canal(compteurs_updated, style_affichage)
    await msg.reply_text(response)
    save_bot_status(True, f"Updated {cards_found}")

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot actif et prêt à compter vos cartes !")

async def reset_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    reset_compteurs_canal(chat_id)
    global processed_messages
    processed_messages = {k for k in processed_messages if not k.startswith(f"{chat_id}_")}
    save_processed_messages()
    await update.message.reply_text("✅ Compteurs réinitialisés")

async def health_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🟢 Bot opérationnel")

async def new_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            await update.message.reply_text("👋 Merci de m’avoir ajouté !")

def run_bot():
    global app_instance
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    logger.info("⏳ Initialisation du bot Telegram...")
    save_bot_status(True, "Starting...")

    app_instance = Application.builder().token(TOKEN).build()
    app_instance.add_handler(CommandHandler("start", start_cmd))
    app_instance.add_handler(CommandHandler("reset", reset_cmd))
    app_instance.add_handler(CommandHandler("health", health_check))
    app_instance.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_chat_member))
    app_instance.add_handler(MessageHandler(filters.ALL, handle_message))

    load_processed_messages()

    app_instance.run_polling(
        drop_pending_updates=True,
        allowed_updates=["message", "edited_message", "channel_post", "edited_channel_post"]
    )

def run_web():
    port = int(os.environ.get("PORT", 10000))
    print(f"🌐 Flask running on port {port}")
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Lance les deux services en parallèle
    threading.Thread(target=run_bot).start()
    run_web()
