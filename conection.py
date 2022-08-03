#from telethon import TelegramClient
from telethon.sync import TelegramClient

class CONNECTION():
    api_id = 2684651
    api_hash = '69ebc6695f7ab2ac9bae9c2940ab7b05'
    phone = '+5574981423804'
    id_groups = '-1001729353083' #ID do grupo: Crypto Czar®🔥
    client = TelegramClient(phone, api_id, api_hash)

class INFOBINANCE():
    pass
    

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
            Horarios.append(hora_texto)#tipos.
            mi += 1
        hor +=1