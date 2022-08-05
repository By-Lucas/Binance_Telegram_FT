# from telethon import TelegramClient
from telethon.sync import TelegramClient
import toml
from decouple import config

config_telegram = toml.load('settings/config.toml')


class Connection:
    def __init__(self):
        self.api_id = config("API_ID")
        self.api_hash = config("API_HASH")
        self.phone = config("PHONE")
        self.id_groups = '-1001729353083'  # ID do grupo: Crypto Czar®🔥
        self.client = TelegramClient(self.phone, self.api_id, self.api_hash)
        print(self.api_hash)


class InfoBinance:
    pass


class ConfigTelegam:
    def __init__(self):
        self.authentication = config_telegram.get("authentication")
        self.email = self.authentication["email"]
        self.password = self.authentication["password"]
        self.account_type = config_telegram.get("management")["account_type"]
        self.amount = config_telegram.get("management")["amount"]
        self.take_profit = config_telegram.get("management")["take_profit"]


class Tipos:
    Paridades = ["#SOL/USDT", "#OP/USDT", "#MATIC/USDT", "#RSR/USDT", "#ANT/USDT", "#EGLD1", "#EGLD/USDT", "#SOL1"] and \
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
            Horarios.append(hora_texto)  # tipos.
            mi += 1
        hor += 1
