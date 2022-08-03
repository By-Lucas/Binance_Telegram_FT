#Bibliotecas
import asyncio
from asyncio.runners import run
import time
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import os
from telethon import TelegramClient, client, events
import threading

from binance.enums import *
from binance.client import Client

from crecentials import api_secret, api_key
from conection import TIPOS, CONNECTION, INFOBINANCE

conn_binance = INFOBINANCE()
conexao = CONNECTION()
tipos = TIPOS()

amount = 0.001


def clear():
    try:
        lines = os.get_terminal_size().lines
    except AttributeError:
        lines = 15
    print("\n" * lines)

def list_msg_grups():
    conexao.client.connect()

    #Se nao estiver conectado, vai enviar codigo para telegram
    if not conexao.client.is_user_authorized():
        conexao.client.send_code_request(conexao.phone)
        conexao.client.sign_in(conexao.phone, input('Digite o codigo enviado: '))

    #Limpar terminal
    clear()

    #Listar grupo e demais informacoes
    chats = []
    last_date = None
    chunk_size = 200
    groups=[]

    result = conexao.client(GetDialogsRequest(
                offset_date=last_date,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=chunk_size,
                hash = 0
            ))
    chats.extend(result.chats)

    #fazendo for para grupo (chats)
    for chat in chats:
        groups.append(chat)

    #opcao de selecionar grupo e grupos listados
    print('[+] Selecione um grupo para usar:\n')
    for i, g in enumerate(groups):
        print(str(i)+' - ' + g.title,'|ID =' , g.id)
    print('')
    g_index = input("[+] Grupo 1: ")
    # g_index_2 = input("[+] Grupo 2: ")

    GRUPOS = []

    target_group=groups[int(g_index)]
    grupo_msg =  conexao.client.get_messages(groups[int(g_index)], limit=200)
    g = {"target_group":target_group, 'grupo_msg': grupo_msg }
    GRUPOS.append(g)

    # target_group = groups[int(g_index_2)]
    # grupo_msg =  conexao.client.get_messages(groups[int(g_index_2)], limit=200)
    # g = {"target_group":target_group, 'grupo_msg': grupo_msg }
    # GRUPOS.append(g)

    for gr in GRUPOS:
        id_grupos = gr['target_group'].id
        print(id_grupos)
        return id_grupos

def models_message():
    gru = list_msg_grups()
    @conexao.client.on(events.NewMessage(chats=gru))
    async def myfunc (event):
        msgRecebida = event.message.message #event.raw_text

        #VARIAVEIS GLOBAIS
        global par, findPar, entrar_em, find_entrada, take_profit, findTake, \
        Short_buy, findBuy_or_sell, horario, findHorario

        #MODELOS PARES DE MOEDAS
        par = ""
        findPar = False
        for p in tipos.Paridades:
            if p.lower() in msgRecebida.lower():
                par = p.replace("#", "")
                findPar = True
                break

        #MODELOS DE PONTOS DE ENTRADA
        entrar_em = ""
        find_entrada = False
        if "Entry Above" in msgRecebida.lower() or "entry above" in msgRecebida.lower():
            entrar_em = 1
            find_entrada = True
        
        #MODELOS DE TAKES PROFIT
        take_profit = ""
        findTake = False
        if "Take-Profit" in msgRecebida.lower() or "take-profit" in msgRecebida.lower():
            take_profit = 1.564
            findTake = True
        
        #MODELOS DE COMRPA E VENDA
        Short_buy = ""
        findBuy_or_sell = False
        if "#Long".lower().replace("#", "") in msgRecebida.lower():
            Short_buy = 'Compra'
            findBuy_or_sell = True
        elif "#Short".lower().replace("#", "") in msgRecebida.lower():
            Short_buy = 'Venda'
            findBuy_or_sell = True
        
        #MODELOS DE HORARIOS
        horario = ""
        findHorario = False
        for h in tipos.Horarios:
            if h in msgRecebida:
                horario = h
                findHorario = True
                break

        if findPar and find_entrada and findTake and Short_buy and findHorario:
            #   SALVAR ENTRADA EM UMA LISTA DE ENTRADAS
            #   SALVAR ENTRADA EM UMA LISTA DE ENTRADAS

            print("================================================")
            print(f"PARIDADE: {par}")
            print(f"ENTRAR EM : {entrar_em}")
            print(f"TAKES PROFIT: {take_profit}")
            print(f"COMPRA / VENDA: {Short_buy}")
            print(f"HORÁRIO: {horario}")
            return par, entrar_em, take_profit, Short_buy, horario

        else:
            print (" ========  NÃO ENCONTROU ===================== ")
            print (f"Paridade: {findPar}, Entrar em: {find_entrada}, Take profit : {findTake}, Compra / venda: {findBuy_or_sell}, Horário : {findHorario}")
            print (" ============================================= ")
            print (event.message.message)
            print (" ============================================= ")
        



def start(self):
    self._thread = threading.Thread(target=self.run())
    self._thread.start()

def run(self):
    conexao.client.start()
    

async def main():
    while True:
        await asyncio.sleep(1)
        
print('Tudo certo!')
conexao.client.loop.run_until_complete(main())

def balance():
    pass

def Order_demo():
    ordem_teste = Client.create_test_order(
        symbol = "BTCBRL",
        side=SIDE_BUY,
        type=ORDER_TYPE_LIMIT,
        timeInforce=TIME_IN_FORCE_GTC,
        quantity=0.001,
        price=320000
    )
    return ordem_teste

def Order_real():
    ordem_real = Client.create_order(
        symbol = "BTCBRL",
        side=SIDE_BUY,
        type=ORDER_TYPE_LIMIT,
        timeInforce=TIME_IN_FORCE_GTC,
        quantity=0.001,
        price=320000
    )
    return ordem_real


def start(demo, amount=0.005):

    count_real = Order_real
    list_sinals = list_msg_grups()
    if demo:
        print("AMBIENTE DE TESTES")
        count_demo = Order_demo