import os
import requests
import json

# from telethon import TelegramClient
from telethon.sync import TelegramClient

import toml

from decouple import config

cwd = os.getcwd()  # Get the current working directory (cwd)
path = cwd.replace('FT/Binance', 'FT/settings/config.toml')
config_telegram = toml.load(path)


class ConnTelegram:
    def __init__(self):
        self.api_id = config("API_ID")
        self.api_hash = config("API_HASH")
        self.phone = config("PHONE")
        self.id_groups = '-1001729353083'  # ID do grupo: Crypto Czar®🔥
        self.client = TelegramClient(self.phone, self.api_id, self.api_hash)
        print(self.api_hash)


class ConnBinance:
    def __init__(self, testnet: bool = True):
        self.testnet = testnet
        if testnet:
            self.api_key = config('API_KEY_TESTNET')
            self.secret = config('API_SECRET_TESTNET')
            self.url = 'https://testnet.binancefuture.com'
        else:
            self.api_key = config('API_KEY_REAL')
            self.api_secret = config('API_SECRET_REAL')
            self.url = 'https://fapi.binance.com'

    def check_conn(self):
        try:
            request = requests.get(self.url + '/fapi/v1/ping')
            r = request.json()
            if self.testnet:
                return 'Binance TESTNET connection successfully!!!'
            return 'Binance REAL ACCOUNT connection successfully!!!!!!'

        except Exception as e:
            print(e)


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
