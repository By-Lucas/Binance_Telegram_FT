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

def get_all_orders():
    try:
        response = client.get_all_orders(symbol="BTCUSDT", recvWindow=2000)
        #logging.info(response)
        print(response)
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )

#add_new_order()
#get_all_orders()
print(total_wallet_balance())
