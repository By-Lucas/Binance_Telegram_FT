from typing import Dict, List, Tuple
import requests
import json
from pprint import pprint

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


if __name__ == '__main__':
    testnet = False
    conn = ConnBinance(testnet=testnet)
    print(conn.check_conn())
    bf = BinanceFunctions(testnet=testnet)
    print(bf.check_coin_price(symbol='XRPUSDT'))
