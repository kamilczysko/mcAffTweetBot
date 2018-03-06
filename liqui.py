from settings_loader import liqui_access as key
import requests as r
import time
import urllib.parse
import hashlib
import hmac
import json

base_url = 'https://api.liqui.io/tapi'
secret = bytes(key['secret'], 'utf-8')


def encrypt(url):
    new_url = bytes(url, 'utf-8')
    signature = hmac.new(secret, new_url, hashlib.sha512).hexdigest()
    return signature

def get_price(token):
    pair = token + '_btc'
    new_url = 'https://api.liqui.io/api/3/ticker/' + pair
    print(new_url)
    req = r.post(new_url)
    data = json.loads(req.text)[pair]
    price = data['sell']
    print(price)


def get_tokens():
    token_list = []
    url = 'https://api.liqui.io/api/3/info'
    req = r.post(url)
    data = json.loads(req.text)['pairs']
    for key in data:
        if '_btc' in key:
            token_list.append(key[:-4].upper())
    print(token_list)
    return token_list


def get_info():
    ts = str(nonce())
    print('nonce: '+ts)

    params = {'nonce': ts, 'method': 'getinfo'}

    params_for_url = urllib.parse.urlencode(params)

    signature = encrypt(params_for_url)

    header = {'Key': key['key'], 'Sign': signature}
    req = r.post(base_url, headers=header, data=params_for_url)
    res = json.loads(req.text)
    return res

def buy_order(token, amount, rate):
    ts = str(nonce())
    print('nonce: '+ts)
    pair = token+"_btc"

    params = {'nonce': ts, 'method': 'trade', 'pair': pair, 'type': 'buy', 'rate': rate, 'amount': amount}

    params_for_url = urllib.parse.urlencode(params)

    signature = encrypt(params_for_url)

    header = {'Key': key['key'], 'Sign': signature}
    req = r.post(base_url, headers=header, data=params_for_url)
    res = json.loads(req.text)
    return res

def sell_order(token, amount, rate):
    ts = str(nonce())
    print('nonce: '+ts)
    pair = token+"_btc"

    params = {'nonce': ts, 'method': 'trade', 'pair': pair, 'type': 'sell', 'rate': rate, 'amount': amount}

    params_for_url = urllib.parse.urlencode(params)

    signature = encrypt(params_for_url)

    header = {'Key': key['key'], 'Sign': signature}
    req = r.post(base_url, headers=header, data=params_for_url)
    res = json.loads(req.text)
    return res


def nonce():
    return int(round(time.time()))

print(sell_order('eth', 100000, 0.0000020))