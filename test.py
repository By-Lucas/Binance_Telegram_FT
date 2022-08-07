#Bibliotecas
import asyncio
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import os
from telethon import events
import threading

# from binance.enums import *
# from binance.client import Client

import pandas as pd
import re

from settings.connections import Tipos, ConnTelegram, ConnBinance, ConfigTelegam

conf_t = ConfigTelegam()
conn_binance = ConnBinance()
conexao = ConnTelegram()
tipos = Tipos()

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

    GRUPOS = []

    target_group=groups[int(g_index)]
    grupo_msg =  conexao.client.get_messages(groups[int(g_index)], limit=200)
    g = {"target_group":target_group, 'grupo_msg': grupo_msg }
    GRUPOS.append(g)

    for gr in GRUPOS:
        id_grupos = gr['target_group'].id
        print(id_grupos)
        return id_grupos


def models_message():
    gru = list_msg_grups()
    @conexao.client.on(events.NewMessage(chats=gru))
    async def myfunc (event):
        msgRecebida = event.message.message #event.raw_text

        # LEITURA DOS SINAIS
        sinal = 'sinal.txt'
        lista = []
        with open(sinal, "w", encoding="utf-8") as f:
            f.write(msgRecebida)
            f.close()
        with open(sinal.lower(), "r", encoding="utf-8") as f:
            linhas = f.readlines()
            for linha in linhas:
                lista.append(linha.lower().split())
        df = pd.DataFrame({'coluna_1': linhas})


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
        ponto_entrada = df[df.coluna_1.str.match('Entry'.replace(')',''))]
        
        if ponto_entrada.size != 0:
            entrar_em_1 = lista[ponto_entrada.index[0]][2]
            entrar_em_2 = lista[ponto_entrada.index[0]][4]
            entrar_em = ""
            find_entrada = False
            if entrar_em_1 >= entrar_em_1 and entrar_em_2 <= entrar_em_2:
                entrar_em = entrar_em_1
                find_entrada = True
            else:
                entrar_em = ""
                find_entrada = False
        else:
            entrar_em = ""
            find_entrada = False
        
        #MODELOS DE TAKES PROFIT
        takes = df[df.coluna_1.str.match('1)'.replace(')',''))]
        if takes.size != 0:

            take_profit = ""
            findTake = False
            if '1)' in lista[takes.index[0]][0] and conf_t.take_profit == 1:
                take_profit = lista[takes.index[0]][1]
                findTake = True

            if '2)' in lista[takes.index[0]+1][0] and conf_t.take_profit == 2:
                take_profit = lista[takes.index[0]+1][1]
                findTake = True
            
            if '3)' in lista[takes.index[0]+2][0] and conf_t.take_profit == 3:
                take_profit = lista[takes.index[0]+2][1]
                findTake = True

            if '4)' in lista[takes.index[0]+3][0] and conf_t.take_profit == 4:
                take_profit = lista[takes.index[0]+3][1]
                findTake = True
        else:
            take_profit = ""
            findTake = False

        #MODELO STOP LOSS
        detect_stop_loss = df[df['coluna_1'].str.match('Stop')]
        if detect_stop_loss.size != 0:
            stop_em = lista[detect_stop_loss.index[0]][2]
            stop_loss_model = re.sub("]","",stop_em).replace("[","").lower()
            stop_loss = ""
            find_stop_loss = False
            if stop_loss_model:
                stop_loss = stop_loss_model
                find_stop_loss = True
            else:
                stop_loss = ''
                find_stop_loss = False

        else:
            stop_loss = ""
            find_stop_loss = False

        
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
            print(f"COMPRA / VENDA: {Short_buy}")
            print(f"TAKES PROFIT: {take_profit}")
            print(f"STOP LOSS: {stop_loss}")
            print(f"HORÁRIO: {horario}")
            return par, entrar_em, take_profit, Short_buy, stop_loss, horario

        else:
            print (" ========  NÃO ENCONTROU ===================== ")
            print (f"Paridade: {findPar}, Entrar em: {find_entrada}, Take profit : {findTake}, Compra / venda: {findBuy_or_sell},Stop Loss: {find_stop_loss}, Horário : {findHorario}")
            print (" ============================================= ")
            print (  event.message.message)
            print (" ============================================= ")

models_message()

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


def start(demo, amount=0.005):

    count_real = 'Order_real'
    list_sinals = list_msg_grups()
    if demo:
        print("AMBIENTE DE TESTES")
        count_demo = 'Order_demo'