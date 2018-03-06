from settings_loader import twitter_access as keys
from settings_loader import main_settings as shopping
import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import API
from tweepy import parsers
import liqui
import bittrex

import data_processor as proc

bittrex_tokens = bittrex.get_tokens()
liqui_tokens = liqui.get_tokens()

auth = OAuthHandler(keys.twitter_access['consumer_key'], keys.twitter_access['consumer_secret'])
auth.set_access_token(keys.twitter_access['access_token'], keys.twitter_access['access_token_secret'])

api = API(auth, parser=parsers.JSONParser())


class listener(StreamListener):
    def on_data(self, data):
        print(data)
        json_data = json.loads(data)
        symbol = get_symbols(json_data).upper()
        print('got symbol! --' + symbol)
        if symbol is not None:
            if symbol in liqui_tokens:
                liqui_shopping(symbol)
            elif symbol in bittrex:
                bittrex_shopping(symbol)
        return (True)

    def on_error(self, status):
        print(status)


def get_symbols(json_data):
    if 'text' in json_data:
        media_url = proc.get_media_url(json_data)
        text_from_tweet = proc.check_if_tweet_is_ok(json_data['text'])
        if text_from_tweet is not None:
            symbol_from_text = proc.get_symbol(text_from_tweet)
            if symbol_from_text is not None:
                return symbol_from_text
            if media_url is not None:
                img_to_ocr = proc.download_media(media_url)
                text_from_img = proc.make_ocr(img_to_ocr)
                symbol_from_img = proc.get_symbol(text_from_img)
                if symbol_from_img is not None:
                    return symbol_from_img
    return None


def bittrex_shopping(token):
    price = bittrex.get_token_price(token)
    price_i_pay = price * shopping['bittrexStartPriceFactor']
    amount_to_buy = shopping['btcToSpendBittrex'] / price_i_pay
    bought = False
    while bought is False:
        bought = bittrex.buy_token(amount_to_buy=amount_to_buy, rate=price_i_pay, token=token)['success']

    sold = False
    while sold is False:
        sold = bittrex.sell_token(token=token, quantity=amount_to_buy*0.9975, rate=price*shopping['bittrexEndPriceFactor'])['success']

def liqui_shopping(token):
    price = liqui.get_price(token)
    price_i_pay = price * shopping['liquiStartPriceFactor']
    amount_to_buy = shopping['btcToSpendLiqui'] / price_i_pay
    bought = 0
    while bought == 0:
        bought = liqui.buy_order(amount=amount_to_buy, rate=price_i_pay, token=token)['success']

    sold = 0
    while sold == 0:
        sold = liqui.sell_order(token=token, amount=amount_to_buy*0.9975[:.8], rate=price*shopping['liquiEndPriceFactor'])['success']


stream = Stream(auth, listener())
stream.userstream()
