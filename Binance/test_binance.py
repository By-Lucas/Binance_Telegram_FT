import logging
from binance.um_futures import UMFutures as Client
from binance.error import ClientError
from binance.lib.utils import config_logging
from datetime import datetime

#config_logging(logging, logging.DEBUG)

api_key=''
api_secret=''


base_url_test = 'https://testnet.binancefuture.com'

client = Client(key=api_key, secret=api_secret, base_url=base_url_test)


def total_wallet_balance():
    try:
        res = client.account(timestamp=datetime.now().timestamp())
        for ativo in res['assets']:
            if float(ativo["walletBalance"]) > 0:
                print(f"Ativo: {ativo['asset']} | Balance: {float(ativo['walletBalance']):.2f}")

        balance = res['totalWalletBalance']
        print(f'Total balance: {float(balance):.2f}')
        
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )
    return balance

def add_new_order():
    params = {
        'symbol': 'BTCUSDT',
        'side': 'SELL',
        'type': 'LIMIT',
        'timeInForce': 'GTC',
        'quantity': 0.1,
        'price': 23257.3
    }   
    try:
        order = client.new_order(**params)
        print('Success order')
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )

def new_list_order(params= list):
    params = {
        "batchOrders": [
            {
                "symbol":"ETHUSDT",
                "side": "SELL",
                "type": "LIMIT",
                "quantity": "0.001",
                "timeInForce": "GTC",
                "reduceOnly": "false",
                "price": "23939"
            },
            {
                "symbol":"BTCUSDT",
                "side": "SELL",
                "type": "LIMIT",
                "quantity": "0.001",
                "timeInForce": "GTC",
                "reduceOnly": "false",
                "price": "23939"
            }
            ]
    }
    try:
        order_list = client.new_batch_order(**params)
        print('Success orders')
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )


def get_all_orders( ** kwargs ):
    params  = { ** kwargs }
    try:
        response = client.get_orders()
        
        if response:
            lista = []
            for orders in response:
                lista.append(orders)
                order_id = orders['orderId']
                symbol = orders['symbol']
                client_order_id = orders['clientOrderId']
                stop_price = orders['stopPrice']
                print(order_id, symbol, client_order_id, stop_price)
        else:
            print('Not ordes')
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )
    return lista

def cancel_ordes_open( **kwargs):
    all_orders = get_all_orders()
    for cancel_lista in all_orders:
        symbol = cancel_lista['symbol']
    try:
        reresponse = client.cancel_open_orders(symbol=symbol, recvWindow=2000,
                                                )
        print('Ordemm cancelada')
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )


cancel_ordes_open() # Cancelar ordem aberta
#get_all_orders() # Pegar ordens aberta
#new_list_order() # fazer ordens multiplas
#add_new_order() # Uma ordem por vez
#total_wallet_balance() # informacoes financeira da conta
