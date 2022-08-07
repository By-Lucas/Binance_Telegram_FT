from typing import Dict, List, Tuple
import requests
import json
from pprint import pprint

from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException

from decouple import config

from settings.connections import ConnBinance


class BinanceFunctions:
    def __init__(self, testnet: bool = True):
        if testnet:
            self.api_key = config('API_KEY_TESTNET')
            self.secret = config('API_SECRET_TESTNET')
            self.url = 'https://testnet.binancefuture.com'
        else:
            self.api_key = config('API_KEY_REAL')
            self.api_secret = config('API_SECRET_REAL')
            self.url = 'https://fapi.binance.com'

    def check_coin_price(self, symbol) -> Dict:
        try:
            url = self.url
            request = requests.get(url + f"/fapi/v1/premiumIndex?symbol={symbol}")
            r = request.json()
            return {r['symbol']: r['indexPrice']}
        except Exception as e:
            print(f'The coin not found: {e}')

    # def new_order(self, symbol, side):
    #     try:
    #         url = self.url
    #         symbol = symbol
    #         side = side
    #         type=
    #         timestamp=
    #         '/fapi/v1/order'
    #         order_test = create_oco_order(
    #             symbol='ETHUSDT',
    #             side=SIDE_SELL,
    #             quantity=100,
    #             price='1667',
    #             stopPrice='1800',
    #             stopLimitPrice='1500',
    #             stopLimitTimeInForce='GTC')

        except BinanceAPIException as e:
            # error handling goes here
            print(e)
        except BinanceOrderException as e:
            # error handling goes here
            print(e)

    def new_real_order(self):
        try:
            order_test = self.client.create_oco_order(
                symbol='ETHUSDT',
                side='SELL',
                quantity=100,
                price=250,
                stopPrice=150,
                stopLimitPrice=150,
                stopLimitTimeInForce='GTC')

        except BinanceAPIException as e:
            # error handling goes here
            print(e)
        except BinanceOrderException as e:
            # error handling goes here
            print(e)

    def cancel_order(self):
        # To cancel order
        result = self.client.cancel_order(
            symbol='BNBBTC',
            orderId='orderId')

    def status_order(self):
        # Get order status
        order = self.client.get_order(
            symbol='BNBBTC',
            orderId='orderId')


if __name__ == '__main__':
    testnet = False
    conn = ConnBinance(testnet=testnet)
    print(conn.check_conn())
    bf = BinanceFunctions(testnet=testnet)
    print(bf.check_coin_price(symbol='XRPUSDT'))
