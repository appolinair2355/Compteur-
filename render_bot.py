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
Qest la méthode utilisée dans ce code?

Stp corrigé ce code pour moi

import logging
from telegram.ext import (
Application, CommandHandler, ContextTypes
)
from telegram import Update
from render_web import app
import os
import logging
import sys
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
from compteur import get_compteurs, update_compteurs, reset_compteurs_canal
from style import afficher_compteurs_canal
import re
import json

TOKEN direct ici

TOKEN = "7749786995:AAGr9rk_uuykLLp5g7Hi3XwIlsdMfW9pWFw"
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

TOKEN = "7749786995:AAGr9rk_uuykLLp5g7Hi3XwIlsdMfW9pWFw"
PORT = int(os.environ.get("PORT", 10000))

app = Flask(name)
application = Application.builder().token(TOKEN).build()

Commande /start

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text("Bonjour ! Je suis actif.")

Enregistre la commande

application.add_handler(CommandHandler("start", start))

Route webhook que Telegram appelle

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
update = Update.de_json(request.get_json(force=True), application.bot)
application.update_queue.put(update)
return "OK", 200

Route de test

@app.route("/", methods=["GET"])
def index():
return "Bot en ligne !"

if name == "main":
application.bot.set_webhook(url=f"https://<TON-SOUS-DOMAINE>.onrender.com/{TOKEN}")
app.run(host="0.0.0.0", port=PORT)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(name)

Exemple de commande

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text("🤖 Bot Joker 3K est prêt !")

def start_bot():
application = Application.builder().token(TOKEN).build()

Ajouter des handlers

application.add_handler(CommandHandler("start", start))

Injecter dans render_web

import render_web
render_web.telegram_app = application

Webhook URL Render

webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"

application.run_webhook(
listen="0.0.0.0",
port=int(os.environ.get("PORT", 10000)),
webhook_url=webhook_url,
)

#!/usr/bin/env python3
"""
Bot with separated counters per channel
"""

Track processed messages per channel

processed_messages = set()

Configure logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(name)

Global variables

style_affichage = 1
TOKEN="7749786995:AAGr9rk_uuykLLp5g7Hi3XwIlsdMfW9pWFw"
def save_bot_status(running, message=None, error=None):
"""Save status to file"""
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

def is_message_processed(message_key):
"""Check if message was already processed"""
return message_key in processed_messages

def mark_message_processed(message_key):
"""Mark message as processed"""
processed_messages.add(message_key)

def load_processed_messages():
"""Load processed messages from file"""
global processed_messages
try:
with open("processed_messages.json", "r") as f:
processed_messages = set(json.load(f))
except:
processed_messages = set()

def save_processed_messages():
"""Save processed messages to file"""
try:
with open("processed_messages.json", "w") as f:
json.dump(list(processed_messages), f)
except:
pass

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
"""Handle incoming messages and edited messages"""
global style_affichage

Get message from any source (including edited messages)

msg = update.message or update.channel_post or update.edited_channel_post or update.edited_message
if not msg or not msg.text:
return

text = msg.text
chat_id = msg.chat_id

Detect if this is an edited message

is_edited = update.edited_channel_post or update.edited_message

logger.info(f"Channel {chat_id}: {'[EDITED] ' if is_edited else ''}{text[:80]}")

Check for message number

match_numero = re.search(r"#n(\d+)", text)
if not match_numero:
return

numero = int(match_numero.group(1))
message_key = f"{chat_id}_{numero}"

Check for progress indicators

progress_indicators = ['⏰', '▶', '🕐', '➡️']
confirmation_symbols = ['✅', '🔰']

has_progress = any(indicator in text for indicator in progress_indicators)
has_confirmation = any(symbol in text for symbol in confirmation_symbols)

If message has progress indicators without confirmation, wait for final version

if has_progress and not has_confirmation:
logger.info(f"Message #{numero} has progress indicators, waiting for final version")
return

For final messages (no progress indicators OR with confirmation):

- If already processed and not edited, skip

- If edited or not processed, proceed

if is_message_processed(message_key):
if not is_edited:
logger.info(f"Message #{numero} already processed and not edited, skipping")
return
else:
logger.info(f"Message #{numero} was edited, reprocessing...")
# For edited messages, we need to subtract previous counts first
# This will be handled by resetting and recounting

Mark as processed (or update if edited)

mark_message_processed(message_key)
save_processed_messages()

Find FIRST parentheses only

match = re.search(r'', text)
if not match:
logger.info("No parentheses found")
return

content = match.group(1)
logger.info(f"Channel {chat_id} - Content: '{content}'")

Count ALL card symbols in the content (including both heart symbols)

cards_found = {}
total_cards = 0

Check for hearts (both symbols)

heart_count = content.count("❤️") + content.count("♥️")
if heart_count > 0:
update_compteurs(chat_id, "❤️", heart_count)
cards_found["❤️"] = heart_count
total_cards += heart_count

Check other symbols

for symbol in ["♦️", "♣️", "♠️"]:
count = content.count(symbol)
if count > 0:
update_compteurs(chat_id, symbol, count)
cards_found[symbol] = count
total_cards += count

if not cards_found:
logger.info(f"No card symbols found in: '{content}'")
return

logger.info(f"Channel {chat_id} - Cards counted: {cards_found}")

save_bot_status(True, f"Channel {chat_id}: {cards_found}")

try:
# Get updated counters and send response
compteurs_updated = get_compteurs(chat_id)
response = afficher_compteurs_canal(compteurs_updated, style_affichage)
await msg.reply_text(response)
logger.info(f"Response sent to channel {chat_id}")
except Exception as e:
logger.error(f"Send error: {e}")

async def reset_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
"""Reset command"""
if not update.message:
return

chat_id = update.message.chat_id
reset_compteurs_canal(chat_id)

Clear processed messages for this channel

global processed_messages
processed_messages = {key for key in processed_messages if not key.startswith(f"{chat_id}_")}
save_processed_messages()

await update.message.reply_text("✅ Reset done for this channel")
save_bot_status(True, f"Reset completed for channel {chat_id}")

async def deposer_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
"""Create deployment package and send it"""
if not update.message:
return

try:
await update.message.reply_text("📦 Création du package de déploiement en cours...")

# Import and run the deployment package creation    
from create_deploy_package import create_deployment_package    
zip_filename = create_deployment_package()    
    
# Check if file exists    
if os.path.exists(zip_filename):    
    # Send the ZIP file    
    await update.message.reply_document(    
        document=open(zip_filename, 'rb'),    
        filename=zip_filename,    
        caption="✅ Package de déploiement créé avec succès !\n🚀 Prêt pour upload sur render.com"    
    )    
    logger.info(f"ZIP file sent: {zip_filename}")    
else:    
    await update.message.reply_text("❌ Erreur : fichier ZIP non trouvé")    
    
save_bot_status(True, "Deployment package sent")

except Exception as e:
await update.message.reply_text(f"❌ Erreur : {str(e)}")
logger.error(f"Error in deposer command: {e}")

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
"""Start command"""
welcome_msg = (
"🤖 Bot de Comptage de Cartes 🃏\n\n"
"Bonjour ! Je compte les cartes séparément pour chaque canal.\n\n"
"📝 Comment ça marche :\n"
"• Envoyez un message avec des cartes entre parenthèses\n"
"• Exemple : Résultat du tirage (❤️♦️♣️♠️)\n"
"• Je compterai automatiquement chaque symbole\n\n"
"🎯 Symboles reconnus :\n"
"❤️ Cœurs • ♦️ Carreaux • ♣️ Trèfles • ♠️ Piques\n\n"
"💡 Commandes disponibles :\n"
"• /reset - Réinitialiser les compteurs\n"
"• /deposer - Créer package de déploiement\n\n"
"⚡ Je suis maintenant actif et prêt à compter !"
)
if update.message:
await update.message.reply_text(welcome_msg)
chat_id = update.message.chat_id
save_bot_status(True, f"Bot started in channel {chat_id}")

async def new_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
"""Handle when bot is added to a group or channel"""
if not update.message or not update.message.new_chat_members:
return

Check if the bot itself was added

for member in update.message.new_chat_members:
if member.id == context.bot.id:
welcome_msg = (
"👋 Salut tout le monde ! 🃏\n\n"
"Je suis le Bot de Comptage de Cartes !\n\n"
"🎯 Ma mission :\n"
"Je vais compter automatiquement tous les symboles de cartes "
"que vous mettez entre parenthèses dans vos messages.\n\n"
"📋 Les compteurs sont séparés par canal !\n"
"Chaque canal aura ses propres totaux.\n\n"
"🃏 Cartes reconnues :\n"
"❤️ Cœurs • ♦️ Carreaux • ♣️ Trèfles • ♠️ Piques\n\n"
"⚡ Je suis maintenant actif !\n\n"
"💡 Commandes utiles :\n"
"• /reset - Réinitialiser les compteurs de ce canal\n"
"• /start - Revoir ce message"
)

await context.bot.send_message(    
        chat_id=update.message.chat_id,    
        text=welcome_msg    
    )    
    chat_id = update.message.chat_id    
    save_bot_status(True, f"Bot added to channel {chat_id}")    
    logger.info(f"Bot added to chat: {chat_id}")    
    break

def main():
"""Main function"""

Get token

token = os.getenv("TELEGRAM_BOT_TOKEN")
if not token:
save_bot_status(False, error="No token")
sys.exit(1)

Load processed messages

load_processed_messages()

logger.info("Starting bot...")
save_bot_status(True, "Starting...")

Create app

app = Application.builder().token(token).build()

Add handlers for messages AND edited messages

app.add_handler(CommandHandler("start", start_cmd))
app.add_handler(CommandHandler("reset", reset_cmd))
app.add_handler(CommandHandler("deposer", deposer_cmd))
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_chat_member))

Handle all messages (new, edited, channel posts, etc.)

app.add_handler(MessageHandler(filters.ALL, handle_message))

logger.info("Bot ready")
save_bot_status(True, "Bot online")

#import logging

from telegram.ext import (
Application, CommandHandler, ContextTypes
)
from telegram import Update
from render_web import app
import os
import logging
import sys
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
from compteur import get_compteurs, update_compteurs, reset_compteurs_canal
from style import afficher_compteurs_canal
import re
import json

TOKEN direct ici

TOKEN = "7749786995:AAGr9rk_uuykLLp5g7Hi3XwIlsdMfW9pWFw"
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

TOKEN = "7749786995:AAGr9rk_uuykLLp5g7Hi3XwIlsdMfW9pWFw"
PORT = int(os.environ.get("PORT", 10000))

app = Flask(name)
application = Application.builder().token(TOKEN).build()

Commande /start

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text("Bonjour ! Je suis actif.")

Enregistre la commande

application.add_handler(CommandHandler("start", start))

Route webhook que Telegram appelle

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
update = Update.de_json(request.get_json(force=True), application.bot)
application.update_queue.put(update)
return "OK", 200

Route de test

@app.route("/", methods=["GET"])
def index():
return "Bot en ligne !"

if name == "main":
application.bot.set_webhook(url=f"https://<TON-SOUS-DOMAINE>.onrender.com/{TOKEN}")
app.run(host="0.0.0.0", port=PORT)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(name)

Exemple de commande

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text("🤖 Bot Joker 3K est prêt !")

def start_bot():
application = Application.builder().token(TOKEN).build()

Ajouter des handlers

application.add_handler(CommandHandler("start", start))

Injecter dans render_web

import render_web
render_web.telegram_app = application

Webhook URL Render

webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"

application.run_webhook(
listen="0.0.0.0",
port=int(os.environ.get("PORT", 10000)),
webhook_url=webhook_url,
)

#!/usr/bin/env python3
"""
Bot with separated counters per channel
"""

Track processed messages per channel

processed_messages = set()

Configure logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(name)

Global variables

style_affichage = 1
TOKEN="7749786995:AAGr9rk_uuykLLp5g7Hi3XwIlsdMfW9pWFw"
def save_bot_status(running, message=None, error=None):
"""Save status to file"""
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

def is_message_processed(message_key):
"""Check if message was already processed"""
return message_key in processed_messages

def mark_message_processed(message_key):
"""Mark message as processed"""
processed_messages.add(message_key)

def load_processed_messages():
"""Load processed messages from file"""
global processed_messages
try:
with open("processed_messages.json", "r") as f:
processed_messages = set(json.load(f))
except:
processed_messages = set()

def save_processed_messages():
"""Save processed messages to file"""
try:
with open("processed_messages.json", "w") as f:
json.dump(list(processed_messages), f)
except:
pass

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
"""Handle incoming messages and edited messages"""
global style_affichage

Get message from any source (including edited messages)

msg = update.message or update.channel_post or update.edited_channel_post or update.edited_message
if not msg or not msg.text:
return

text = msg.text
chat_id = msg.chat_id

Detect if this is an edited message

is_edited = update.edited_channel_post or update.edited_message

logger.info(f"Channel {chat_id}: {'[EDITED] ' if is_edited else ''}{text[:80]}")

Check for message number

match_numero = re.search(r"#n(\d+)", text)
if not match_numero:
return

numero = int(match_numero.group(1))
message_key = f"{chat_id}_{numero}"

Check for progress indicators

progress_indicators = ['⏰', '▶', '🕐', '➡️']
confirmation_symbols = ['✅', '🔰']

has_progress = any(indicator in text for indicator in progress_indicators)
has_confirmation = any(symbol in text for symbol in confirmation_symbols)

If message has progress indicators without confirmation, wait for final version

if has_progress and not has_confirmation:
logger.info(f"Message #{numero} has progress indicators, waiting for final version")
return

For final messages (no progress indicators OR with confirmation):

- If already processed and not edited, skip

- If edited or not processed, proceed

if is_message_processed(message_key):
if not is_edited:
logger.info(f"Message #{numero} already processed and not edited, skipping")
return
else:
logger.info(f"Message #{numero} was edited, reprocessing...")
# For edited messages, we need to subtract previous counts first
# This will be handled by resetting and recounting

Mark as processed (or update if edited)

mark_message_processed(message_key)
save_processed_messages()

Find FIRST parentheses only

match = re.search(r'', text)
if not match:
logger.info("No parentheses found")
return

content = match.group(1)
logger.info(f"Channel {chat_id} - Content: '{content}'")

Count ALL card symbols in the content (including both heart symbols)

cards_found = {}
total_cards = 0

Check for hearts (both symbols)

heart_count = content.count("❤️") + content.count("♥️")
if heart_count > 0:
update_compteurs(chat_id, "❤️", heart_count)
cards_found["❤️"] = heart_count
total_cards += heart_count

Check other symbols

for symbol in ["♦️", "♣️", "♠️"]:
count = content.count(symbol)
if count > 0:
update_compteurs(chat_id, symbol, count)
cards_found[symbol] = count
total_cards += count

if not cards_found:
logger.info(f"No card symbols found in: '{content}'")
return

logger.info(f"Channel {chat_id} - Cards counted: {cards_found}")

save_bot_status(True, f"Channel {chat_id}: {cards_found}")

try:
# Get updated counters and send response
compteurs_updated = get_compteurs(chat_id)
response = afficher_compteurs_canal(compteurs_updated, style_affichage)
await msg.reply_text(response)
logger.info(f"Response sent to channel {chat_id}")
except Exception as e:
logger.error(f"Send error: {e}")

async def reset_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
"""Reset command"""
if not update.message:
return

chat_id = update.message.chat_id
reset_compteurs_canal(chat_id)

Clear processed messages for th


