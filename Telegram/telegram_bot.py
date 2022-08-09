# pip install pyrogram
# pip install TgCrypto (Deixa Pyrogram mais rapido)
from asyncio import run
from pyrogram import Client
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent,
                            InlineKeyboardMarkup, InlineKeyboardButton)

from decouple import config

api_id = 8530827
api_hash = '08290d72279246186b0c1sef13e933a04'
bot_token = '1665637466:AAGeUeSHH5f7hergPGdvIEzICCB4tp6LkMI'
id_bot = '@RobotZeus_bot'

app = Client("bot_sessions/Binance_bot",api_id=api_id, api_hash=api_hash, bot_token=bot_token)

async def main():
    await app.start()
    await app.send_message('@tk_milionario', 'Ola Lucas')
    await app.stop()

run(main())