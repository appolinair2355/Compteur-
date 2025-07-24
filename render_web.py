from flask import Flask, request
from telegram import Update
from telegram.ext import Application
import logging
import asyncio

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# TOKEN direct ici
TOKEN = "7749786995:AAGr9rk_uuykLLp5g7Hi3XwIlsdMfW9pWFw"

telegram_app: Application = None  # sera défini dans render_bot

@app.route("/")
def home():
    return "🤖 Bot Joker 3K - En ligne !"

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    if telegram_app is None:
        return "Bot non initialisé", 500

    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    await telegram_app.update_queue.put(update)
    return "OK", 200
