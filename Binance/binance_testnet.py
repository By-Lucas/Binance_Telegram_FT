import logging

from typing import List
from time import sleep
from datetime import datetime

from binance.um_futures import UMFutures as Client
from binance.error import ClientError
from binance.lib.utils import config_logging

from decouple import config


class BinanceManager:
    def __init__(self, testnet: bool = True):
        if testnet:
            self.api_key = config('API_KEY_TESTNET')
            self.api_secret = config('API_SECRET_TESTNET')
            self.base_url_test = 'https://testnet.binancefuture.com'
        else:
            self.api_key = config('API_KEY_REAL')
            self.api_secret = config('API_SECRET_REAL')
            self.base_url_test = 'https://fapi.binance.com'

        self.client = Client(key=self.api_key, secret=self.api_secret, base_url=self.base_url_test)

    def total_wallet_balance(self):
        try:
            print("Total wallet balance")
            res = self.client.account(timestamp=datetime.now().timestamp())
            for ativo in res['assets']:
                if float(ativo["walletBalance"]) > 0:
                    print(f"Ativo: {ativo['asset']} | Balance: {float(ativo['walletBalance']):.2f}")

            balance = res['totalWalletBalance']
            print(f'Total balance: {float(balance):.2f}')
            return balance

        except ClientError as error:
            logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )

    def add_new_order(self):
        params = {
            'symbol': 'BTCUSDT',
            'side': 'SELL',
            'type': 'LIMIT',
            'timeInForce': 'GTC',
            'quantity': 0.1,
            'price': 23257.3
        }
        try:
            order = self.client.new_order(**params)
            print('Success order')
        except ClientError as error:
            logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )

    def new_list_order(self, params=List):
        params = {
            "batchOrders": [
                {
                    "symbol": "ETHUSDT",
                    "side": "SELL",
                    "type": "LIMIT",
                    "quantity": "0.001",
                    "timeInForce": "GTC",
                    "reduceOnly": "false",
                    "price": "23939"
                },
                {
                    "symbol": "BTCUSDT",
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
            order_list = self.client.new_batch_order(**params)
            print('Success orders')
        except ClientError as error:
            logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )

    def get_all_orders(self, **kwargs):
        params = {**kwargs}
        print("Get all orders")
        time_server = self.client.time()['serverTime']
        check_time = datetime.now().timestamp()
        print(time_server)
        print(check_time)
        print(check_time - time_server)
        try:
            lista = []
            response = self.client.get_orders()
            if response:
                for orders in response:
                    lista.append(orders)
                    order_id = orders['orderId']
                    symbol = orders['symbol']
                    client_order_id = orders['clientOrderId']
                    stop_price = orders['stopPrice']
                    print(order_id, symbol, client_order_id, stop_price)
            else:
                print('Not ordes')
            return lista

        except ClientError as error:
            logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )

    def cancel_ordes_open(self, **kwargs):
        all_orders = self.get_all_orders()
        for cancel_lista in all_orders:
            symbol = cancel_lista['symbol']
        try:
            response = self.client.cancel_open_orders(symbol=symbol, recvWindow=2000)
            print('Ordemm cancelada')
        except ClientError as error:
            logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )

    def main(self):
        try:
            self.total_wallet_balance()  # informacoes financeira da conta
            # self.wallet_balance()
            self.get_all_orders()  # Pegar ordens aberta
            self.new_list_order()  # fazer ordens multiplas
            self.add_new_order()  # Uma ordem por vez
            sleep(4)
            self.get_all_orders()  # Pegar ordens aberta
            sleep(3)
            self.cancel_ordes_open()  # Cancelar ordem aberta
        except Exception as e:
            print(e)


if __name__ == '__main__':
    bm = BinanceManager()
    bm.main()
