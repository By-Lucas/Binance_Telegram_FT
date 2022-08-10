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

    def total_wallet_balance(self) -> str:
        try:
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
            'quantity': 0.001,
            'price': 27000.3
        }
        # check open orders.
        check_orders = self.client.get_orders()
        if len(check_orders) == 0 :
            print('Sem ordens para comparar')
            try:
                order = self.client.new_order(**params)
                print('Success order')
                print("order")
                print(order)
                return order
            except ClientError as error:
                logging.error(
                    "Found error. status: {}, error code: {}, error message: {}".format(
                        error.status_code, error.error_code, error.error_message
                    )
                )


        elif check_orders:
            for order in check_orders:
                symbol_check = 'BTCUSDT'
                if order['symbol'] == symbol_check:
                    print('Você já possui um trading aberto para esse par de moedas')
                else:
                    try:
                        order = self.client.new_order(**params)
                        print('Success order')
                        return order

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
                    "price": "2039"
                },
                {
                    "symbol": "BTCUSDT",
                    "side": "SELL",
                    "type": "LIMIT",
                    "quantity": "0.001",
                    "timeInForce": "GTC",
                    "reduceOnly": "false",
                    "price": "27939"
                }
            ]
        }
        check_orders = self.get_all_orders()
        for order in check_orders:
            if order['symbol'] == params['batchOrders'][0]['symbol']:
                print('Você já tem uma ordem aberta para esse par de moedas')
            else:
                try:
                    order_list = self.client.new_batch_order(**params)
                    print('Success orders')
                    print(order_list)
                    return order_list
                except ClientError as error:
                    logging.error(
                        "Found error. status: {}, error code: {}, error message: {}".format(
                            error.status_code, error.error_code, error.error_message
                        )
                    )

    def get_all_orders(self, **kwargs):
        params = {**kwargs}
        print("Get all orders")
        # time_server = self.client.time()['serverTime']
        # check_time = datetime.now().timestamp()
        try:
            lista = []
            response = self.client.get_orders()
            if response:
                for orders in response:
                    lista.append(orders)

                print(f"I found {len(lista)} open order(s).")
                for i, v in enumerate(lista):
                    print(f"Order {i+1}. Order ID- {v['orderId']}. Symbol = {v['symbol']}")
                    print(f"Type: {v['type']}. Side = {v['side']}, Size: {v['origQty']}\n")
                    print(f"\nComplete Info: {v}\n")

            else:
                print('Not orders')

            return lista

        except ClientError as error:
            logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )

    def cancel_orders_open(self, **kwargs):
        all_orders = self.get_all_orders()
        all_positions = self.client.get_position_risk(symbol='BTCUSDT', recWindow=2000)
        print("all_positions")
        print(all_positions)
        for cancel_lista in all_orders:
            symbol = cancel_lista['symbol']
            try:
                response = self.client.cancel_open_orders(symbol=symbol, recvWindow=2000)
                print('Ordemm cancelada')
                print(response)
            except ClientError as error:
                logging.error(
                    "Found error. status: {}, error code: {}, error message: {}".format(
                        error.status_code, error.error_code, error.error_message
                    )
                )


if __name__ == '__main__':
    bm = BinanceManager()
    try:
        bm.total_wallet_balance()  # informacoes financeira da conta
        sleep(2)
        bm.add_new_order()  # Uma ordem por vez
        sleep(2)
        bm.get_all_orders()  # Pegar ordens aberta
        sleep(2)
        bm.new_list_order()  # fazer ordens multiplas
        sleep(2)
        bm.get_all_orders()  # Pegar ordens aberta
        sleep(2)
        bm.cancel_orders_open()  # Cancelar ordem aberta
        sleep(2)
        bm.get_all_orders()  # Pegar ordens aberta
        sleep(2)
        bm.total_wallet_balance()  # informacoes financeira da conta
    except Exception as e:
        print(e)
