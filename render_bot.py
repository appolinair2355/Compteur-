#!/usr/bin/env python3
"""
render_bot.py — Bot Telegram avec Flask pour Render
"""

import os
import json
import logging
import re
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ContextTypes, filters
)

from compteur import get_compteurs, update_compteurs, reset_compteurs_canal
from style import afficher_compteurs_canal
from create_deploy_package import create_deployment_package

# --- Configuration ---
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "TON_TOKEN_ICI")
PORT = int(os.environ.get("PORT", 10000))
RENDER_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "")
WEBHOOK_URL = f"https://{RENDER_HOSTNAME}/{TOKEN}"

# --- Flask app ---
app = Flask(__name__)

# --- Telegram App ---
application = Application.builder().token(TOKEN).build()

# --- Logger ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Données globales ---
processed_messages = set()
style_affichage = 1

# --- Fonctions de sauvegarde ---
def save_bot_status(running, message=None, error=None):
    status = {
        "running": running,
        "last_message": message,
        "error": error
    }
    try:
        with open("bot_status.json", "w") as f:
            json.dump(status, f)
    except:
        pass

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

def is_message_processed(key):
    return key in processed_messages

def mark_message_processed(key):
    processed_messages.add(key)

# --- Handlers Telegram ---

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            "🤖 Bot de Comptage de Cartes 🃏\n\n"
            "Envoyez des cartes entre parenthèses, je les compte pour chaque canal.\n"
            "Exemple : (❤️♦️♣️♠️)\n\n"
            "Commandes disponibles :\n"
            "/reset — Réinitialise les compteurs\n"
            "/deposer — Crée le package Render"
        )
        save_bot_status(True, f"Bot démarré dans {update.message.chat_id}")

async def reset_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    chat_id = update.message.chat_id
    reset_compteurs_canal(chat_id)

    global processed_messages
    processed_messages = {k for k in processed_messages if not k.startswith(f"{chat_id}_")}
    save_processed_messages()

    await update.message.reply_text("✅ Compteurs réinitialisés pour ce canal")
    save_bot_status(True, f"Reset effectué pour {chat_id}")

async def deposer_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    try:
        await update.message.reply_text("📦 Création du package en cours...")
        zip_filename = create_deployment_package()
        if os.path.exists(zip_filename):
            await update.message.reply_document(
                document=open(zip_filename, "rb"),
                filename=zip_filename,
                caption="✅ Package prêt pour Render !"
            )
        else:
            await update.message.reply_text("❌ Erreur : fichier ZIP introuvable")
        save_bot_status(True, "Package envoyé")
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur : {e}")
        logger.error(f"Erreur deposer: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global style_affichage

    msg = update.message or update.channel_post or update.edited_channel_post or update.edited_message
    if not msg or not msg.text:
        return

    text = msg.text
    chat_id = msg.chat_id
    is_edited = update.edited_channel_post or update.edited_message

    match_num = re.search(r"#n(\d+)", text)
    if not match_num:
        return

    numero = int(match_num.group(1))
    key = f"{chat_id}_{numero}"

    progress = ['⏰', '▶', '🕐', '➡️']
    confirmations = ['✅', '🔰']
    if any(p in text for p in progress) and not any(c in text for c in confirmations):
        return

    if is_message_processed(key) and not is_edited:
        return

    mark_message_processed(key)
    save_processed_messages()

    match = re.search(r"\((.*?)\)", text)
    if not match:
        return

    content = match.group(1)
    cards_found = {}
    total = 0

    heart = content.count("❤️") + content.count("♥️")
    if heart:
        update_compteurs(chat_id, "❤️", heart)
        cards_found["❤️"] = heart
        total += heart

    for symbol in ["♦️", "♣️", "♠️"]:
        count = content.count(symbol)
        if count:
            update_compteurs(chat_id, symbol, count)
            cards_found[symbol] = count
            total += count

    if not cards_found:
        return

    try:
        c = get_compteurs(chat_id)
        response = afficher_compteurs_canal(c, style_affichage)
        await msg.reply_text(response)
    except Exception as e:
        logger.error(f"Erreur d'envoi : {e}")

# --- Webhook pour Telegram (Render) ---

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put(update)
    return "OK", 200

@app.route("/", methods=["GET"])
def index():
    return "✅ Bot en ligne"

# --- Lancement principal ---
if __name__ == "__main__":
    load_processed_messages()

    application.add_handler(CommandHandler("start", start_cmd))
    application.add_handler(CommandHandler("reset", reset_cmd))
    application.add_handler(CommandHandler("deposer", deposer_cmd))
    application.add_handler(MessageHandler(filters.ALL, handle_message))

    application.bot.set_webhook(url=WEBHOOK_URL)
    app.run(host="0.0.0.0", port=PORT)
