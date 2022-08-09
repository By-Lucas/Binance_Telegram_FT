from binance.client import Client
from decouple import config


api_key = config('API_KEY_REAL')
api_secret = config('API_SECRET_REAL')
base_url_test = 'https://fapi.binance.com'

client = Client(api_key, api_secret)

# pegar informações da nossa conta
info = client.get_account()
for item in info:
    print(item)

# ver os saldos dos ativos que temos na conta
lista_ativos = info["balances"]
# print(lista_ativos)
# ativos que temos algum saldo
for ativo in lista_ativos:
    if float(ativo["free"]) > 0:
        print(ativo)

# criar uma ordem dentro da binance
from binance.enums import *

order = client.create_order(
    symbol='BNBBRL',
    side=SIDE_SELL,
    type=ORDER_TYPE_MARKET,
    quantity=0.01,
)
print('ODERM', order)

# visualizar as ordens executadas
print(client.get_all_orders(symbol='BNBBRL'))
print(client.get_my_trades(symbol='BNBBRL'))

# Mostrar as referências de cada par de moedas
print(client.get_symbol_info('BNBBRL'))
