#Bibliotecas
import asyncio
from asyncio.runners import run
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import os, sys
import configparser
import csv
import time
from telethon import TelegramClient, client, events

import threading


class TIPOS:
    Paridades = ["#SOL/USDT", "#OP/USDT", "#MATIC/USDT", "#RSR/USDT", "#ANT/USDT", "#EGLD1", "#EGLD/USDT","#SOL1"] and \
                ["#MASK/USDT", "#MTL/USDT", "#ALICE/USDT", "#GMT/USD", "#ETH/USDT"]
    Horarios = []

hor = 0
parteHora = ""
parteMinuto = ""
while hor < 24:
    mi = 0
    while mi < 60:
        
        if hor < 10:
            parteHora = f"0{hor}"
        else:
            parteHora = hor

        if mi < 10:
            parteMinuto = f"0{mi}"
        else:
            parteMinuto = mi

        hora_texto = f"{parteHora}:{parteMinuto}"
        TIPOS.Horarios.append(hora_texto)
        mi += 1
    hor +=1


#Conexao com a api e numero
api_id = 2684651
api_hash = '69ebc6695f7ab2ac9bae9c2940ab7b05'
phone = '+5574981423804' #Digite seu numero de telefne formato +558398127723
client = TelegramClient(phone, api_id, api_hash)
client.connect()

#Se nao estiver conectado, vai enciar codigo para telegram
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Digite o codigo enviado: '))
    
os.system('clear')

#Listar grupo e demais informacoes
chats = []
last_date = None
chunk_size = 200
groups=[]

result = client(GetDialogsRequest(
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
g_index_2 = input("[+] Grupo 2: ")

GRUPOS = []

target_group=groups[int(g_index)]
grupo_msg =  client.get_messages(groups[int(g_index)], limit=200)
g = {"target_group":target_group, 'grupo_msg': grupo_msg }
GRUPOS.append(g)

target_group = groups[int(g_index_2)]
grupo_msg =  client.get_messages(groups[int(g_index_2)], limit=200)
g = {"target_group":target_group, 'grupo_msg': grupo_msg }
GRUPOS.append(g)

for gr in GRUPOS:
    
    @client.on(events.NewMessage(chats=gr['target_group'].id))
    async def myfunc (event):

        msgRecebida = event.message.message #event.raw_text
        
        #MODELOS PARES DE MOEDAS
        par = ""
        findPar = False
        for p in TIPOS.Paridades:
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
        if "#Long".replace("#", "") in msgRecebida.lower():
            Short_buy = 'Compra'
            findBuy_or_sell = True
        elif "#Short".replace("#", "") in msgRecebida.lower():
            Short_buy = 'Venda'
            findBuy_or_sell = True
        
        #MODELOS DE HORARIOS
        horario = ""
        findHorario = False
        for h in TIPOS.Horarios:
            if h in msgRecebida:
                horario = h
                findHorario = True
                break

        if findPar and find_entrada and findTake and Short_buy and findHorario:

            #   SALVAR ENTRADA EM UMA LISTA DE ENTRADAS
            #   SALVAR ENTRADA EM UMA LISTA DE ENTRADAS
            #   SALVAR ENTRADA EM UMA LISTA DE ENTRADAS

            print("================================================")
            print(f"PARIDADE: {par}")
            print(f"ENTRAR EM : {entrar_em}")
            print(f"TAKES PROFIT: {take_profit}")
            print(f"COMPRA / VENDA: {take_profit}")
            print(f"HORÁRIO: {horario}")
        
        else:
            print (" ========  NÃO ENCONTROU ===================== ")
            print (f"Paridade: {findPar}, Entrar em: {find_entrada}, Take profit : {findTake}, Compra ou venda: {findBuy_or_sell}, Horário : {findHorario}")
            print (" ============================================= ")
            print (event.message.message)
            print (" ============================================= ")

class loopRecebedor():

    def start(self):
        self._thread = threading.Thread(target=self.run())
        self._thread.start()
    
    def run(self):
        client.start()

    async def main():
        while True:
            await asyncio.sleep(1)
            
    print('Tudo certo!')
    client.loop.run_until_complete(main())
    

    
    #   VERIFICAR LISTA DE ENTRADAS E FAZER AS ENTRADAS
    #   VERIFICAR LISTA DE ENTRADAS E FAZER AS ENTRADAS
    #   VERIFICAR LISTA DE ENTRADAS E FAZER AS ENTRADAS
    #   VERIFICAR LISTA DE ENTRADAS E FAZER AS ENTRADAS

