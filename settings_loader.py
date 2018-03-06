import json

data = json.load(open('settings.json'))

twitter_access = data['twitter_access']
bittrex_access = data['bittrex_access']
liqui_access = data['liqui_access']
main_settings = data['main_settings']

print("KEYS:")
print(twitter_access)
print(bittrex_access)
print(liqui_access)
print("**************")
