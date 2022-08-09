# pip install pyrogram
# pip install TgCrypto (Deixa Pyrogram mais rapido)
#from asyncio import run
from pyrogram import Client, filters
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent,
                            InlineKeyboardMarkup, InlineKeyboardButton,
                            ReplyKeyboardMarkup)

from decouple import config

api_id = 8530827
api_hash = '08290d72279246186b0c1ef13e933a04'
bot_token = '1665637466:AAH0AJP_xmjwtlxu38g0MKeicTw3i7OSd3w'
id_bot = '@RobotZeus_bot'

app = Client("bot_sessions/Bot_telegram",api_id=api_id, api_hash=api_hash, bot_token=bot_token)




@app.on_message(filters.command('ajuda'))
async def ajuda(client, message):
    await message.reply(
        'Esse é menu para pedir ajuda!'
    )


# Paginação 
@app.on_callback_query()
async def callback(client, callback_query):
    pages = {
        'data': {
            'proximo': InlineKeyboardButton('Proximo >>', callback_data='page_2'),
            'anterior': InlineKeyboardButton('<< anterior', callback_data='data'),
            'menu': InlineKeyboardButton('Menu', callback_data='data'), #, callback_data='menu'
            'texto': 'Aqui fica informações da **Pagina 1**',
        },
        'page_2': {
            'proximo': InlineKeyboardButton('Proximo >>', callback_data='page_3'),
            'anterior': InlineKeyboardButton('<< anterior', callback_data='data'),
            'menu': InlineKeyboardButton('Menu', callback_data='data'), #, callback_data='menu'
            'texto': 'Aqui fica informações da **Pagina 2**',
        },
        'page_3': {
            'proximo': InlineKeyboardButton('Proximo >>', callback_data='data'),
            'anterior': InlineKeyboardButton(' <<anterior', callback_data='page_2'),
            'menu': InlineKeyboardButton('Menu', callback_data='data'), #, callback_data='menu'
            'texto': 'Aqui fica informações da **Pagina 3**',
        }
    }
    page = pages[callback_query.data]
    await callback_query.edit_message_text(
        page['texto'],
        reply_markup = InlineKeyboardMarkup([[page['menu'], page['anterior'], page['proximo']]])
    )

@app.on_message(filters.command('menu'))
async def botoes(client, message):
    usuario = message.chat.username
    botoes = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('Site Bot Binance', url='https://www.youtube.com/watch?v=bO-ksqJNPXg'),
                InlineKeyboardButton('Renovar licença', callback_data='0'),
                InlineKeyboardButton('Comprar bot', callback_data='0'),
               
            ],
            [
                InlineKeyboardButton('Canal VIP', callback_data='0'),
                InlineKeyboardButton('Grupo Free', callback_data='0'),
                InlineKeyboardButton('Informações', callback_data='data'),
            ],
            [   InlineKeyboardButton('Pagina do usuário', callback_data='0'),
                InlineKeyboardButton('Outros', callback_data='0'),
                InlineKeyboardButton('Videos', callback_data='0'),
                InlineKeyboardButton('Ajuda', callback_data='ajuda'),
            ]
        ]
    )
    await message.reply(f'''Olá **{usuario}**, Escolha uma das opções abaixo:''', reply_markup=botoes)

@app.on_message(filters.command('teclado'))
async def tecado(client, message):
    teclado = ReplyKeyboardMarkup(
        [
            ['/Iniciar', '/configuração', '/Gerenciamento'],
            ['/opcao1', '/opcao2', '/ajuda'],
        ],
        resize_keyboard=True
    )
    await message.reply(
        'Aperta ai no teclado',
        reply_markup = teclado
    )

#filters.private = Se a conversa for no privado, se for em grupo ficaria(filters.group("Nome_do_grupo"))
@app.on_message(filters.sticker)
async def send_sticker(client, message):
    await app.send_sticker(
        message.chat.id,
        message.sticker.file_id
    )

@app.on_message(filters.photo | filters.video)
async def photo_video(client, message):
    await message.reply(
        'Não respondemos por fotos ou videos, escolha uma opção válida'
    )

@app.on_message(filters.photo | filters.video)
async def photo_video(client, message):
    await message.reply(
        'Não respondemos por fotos ou videos, escolha uma opção válida'
    )

# pegar quem mandou mensgem para o bot
@app.on_message()
async def messages(client, message):
    print(message.chat.username, message.text)
    usuario = message.chat.username
    await message.reply(f'Seja bem vindo: {usuario}')


# async def main():
#     await app.start()
#     await app.send_message('@tk_milionario', 'Ola Lucas')
#     await app.stop()
#run(main())

app.run()