import logging
from binance.spot import Spot as Client
from binance.error import ClientError
from binance.lib.utils import config_logging

config_logging(logging, logging.DEBUG)


# CADASTRAR API_KEY E API_SECRETS NO LINK https://testnet.binance.vision E COLCAR NOS CAMPOS ABAIXO
api_key=''
api_secret=''

params = {
    "symbol": "ETHUSDT",
    "side": "SELL",
    "type": "LIMIT",
    "timeInForce": "GTC",
    "quantity": 0.1,
    "price": 49500,
}


base_url_test = 'https://testnet.binance.vision'

client = Client(key=api_key, secret=api_secret, base_url=base_url_test)
response = client.account(recvWindow=6000)


try:
    response = client.get_orders("BTCUSDT")
    print(response)
except ClientError as error:
    logging.error(
        "Found error. status: {}, error code: {}, error message: {}".format(
            error.status_code, error.error_code, error.error_message
        )
    )

