from settings_loader import bittrex_access as key
import requests as r
import time
import urllib.parse
import hashlib
import hmac
import json

base_url = 'https://bittrex.com/api/v1.1'
secret = bytes(key['secret'], 'utf-8')

def get_tokens():
    request = r.get(base_url + '/public/getmarkets')
    data = request.json()['result']
    tokens = []

    for token in data:
        if token['BaseCurrency'] == 'BTC':
            tokens.append(token['MarketCurrency'])
            print(token['MarketCurrency'])

    return tokens

def get_token_price(token):
    request = r.get(base_url + "/public/getticker", params={'market': 'btc-' + token})
    data = request.json()['result']
    return float(data["Ask"])

def buy_token(token, quantity, rate):
    url = base_url + "/market/buylimit?"
    params = {'apikey': key['key'],'nonce': str(nonce()), 'market': 'btc-' + token, 'quantity': quantity, 'rate': rate}
    new_url = url+urllib.parse.urlencode(params)
    signature = encrypt(new_url)
    print(new_url+"\n"+signature)
    req = r.get(new_url, headers={'apisign':signature})
    resp = json.loads(req.text)
    print(resp)

def sell_token(token, quantity, rate):
    url = base_url + "/market/selllimit?"
    params = {'apikey': key['key'],'nonce': str(nonce()), 'market': 'btc-' + token, 'quantity': quantity, 'rate': rate}
    new_url = url+urllib.parse.urlencode(params)
    signature = encrypt(new_url)
    print(new_url+"\n"+signature)
    req = r.get(new_url, headers={'apisign':signature})
    resp = json.loads(req.text)
    print(resp)

def encrypt(url):
    new_url = bytes(url, 'utf-8')
    signature = hmac.new(secret, new_url, hashlib.sha512).hexdigest()
    return signature


def nonce():
    return int(round(time.time()))

buy_token('eth', 125.33, 0.0000001)

