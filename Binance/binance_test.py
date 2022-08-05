#from binance.client import Client
from binance.client import Client
#from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
from credentials import api_secret, api_key

class OperarBinance():
    def __init__(self):
        global client

        base_url_test = 'https://testnet.binance.vision'
        #base_url = "https://api.binance.com"

        client = Client(api_key, api_secret,  testnet=True)#testnet=True
        print(client.get_account)
        #client.API_URL = 'https://testnet.binance.vision/api/'
        #client.API_URL = 'https://testnet.binancefuture.com

        crypto_price = client.get_symbol_ticker(symbol="BNBBTC")
        print('CRYPTO:',crypto_price["symbol"], '| PREÇO:', crypto_price["price"])
        
        try:
            print(client.get_all_orders())
        
            # get balances for all assets & some account information
            print(client.get_account())

            # get balance for a specific asset only (BTC)
            print(client.get_asset_balance(asset='BTC'))

            # get latest price from Binance API
            btc_price = client.get_symbol_ticker(symbol="BTCUSDT")

            # print full output (dictionary)
            print('CRYPTO: ', btc_price["symbol"], 'PREÇO: ', btc_price["price"])

        except BinanceAPIException as e:
            print (e.status_code)
            print (e.message)
       

    def new_test_order():
        try:
            order_test = client.create_oco_order(
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
    
    def new_real_order():
        try:
            order_test = client.create_oco_order(
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

    def cancel_order():
        # To cancel order
        result = client.cancel_order(
            symbol='BNBBTC',
            orderId='orderId')

    def status_order():
        # Get order status
        order = client.get_order(
            symbol='BNBBTC',
            orderId='orderId')
                

OperarBinance()