#!/usr/bin/env python3
"""
render_bot.py — Contient le bot Telegram + l'app Flask (webhook) pour Render
"""

import os
import logging
import re
import json
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ContextTypes, filters
)

# ⚠️ TOKEN EN DUR (moins sécurisé, mais demandé par toi)
TOKEN = "7749786995:AAGr9rk_uuykLLp5g7Hi3XwIlsdMfW9pWFw"
PORT = int(os.environ.get("PORT", 10000))

# Initialisation
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variable globale pour l'application Telegram
telegram_app = None

# ========== Fonctions du bot ==========

compteurs = {
    "❤️": 0,
    "♦️": 0,
    "♣️": 0,
    "♠️": 0
}
messages_traites = set()


def extraire_cartes_parenthese(message):
    match = re.search(r"\((.*?)\)", message)
    if match:
        contenu = match.group(1)
        cartes = re.findall(r"[A-Z0-9]+[❤️♦️♣️♠️]", contenu)
        return cartes
    return []


def mettre_a_jour_compteurs(cartes):
    for carte in cartes:
        if carte[-1] in compteurs:
            compteurs[carte[-1]] += 1


def formater_compteurs():
    return "\n".join([f"{symbole} : {count}" for symbole, count in compteurs.items()])


def reset_compteurs():
    for symbole in compteurs:
        compteurs[symbole] = 0
    messages_traites.clear()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot actif. Envoyez des messages contenant des cartes !")


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reset_compteurs()
    await update.message.reply_text("✅ Compteurs remis à zéro.")


async def afficher(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texte = formater_compteurs()
    await update.message.reply_text(f"📊 Compteurs actuels :\n{texte}")


async def traiter_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_id = update.message.message_id
    chat_id = update.message.chat_id

    if (chat_id, message_id) in messages_traites:
        return

    cartes = extraire_cartes_parenthese(update.message.text or "")
    if cartes:
        mettre_a_jour_compteurs(cartes)
        messages_traites.add((chat_id, message_id))
        texte = formater_compteurs()
        await update.message.reply_text(f"✅ Compteurs mis à jour :\n{texte}")


# ========== Initialisation du bot ==========

def start_bot():
    global telegram_app
    telegram_app = Application.builder().token(TOKEN).build()

    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("reset", reset))
    telegram_app.add_handler(CommandHandler("afficher", afficher))
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, traiter_message))

    logger.info("🤖 Bot Telegram lancé.")
    telegram_app.run_polling()


# ========== Webhook Flask ==========

@app.route("/")
def index():
    return "✅ Bot et serveur en ligne."


@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot=Bot(TOKEN))
        if telegram_app:
            telegram_app.update_queue.put_nowait(update)
        return "OK"
