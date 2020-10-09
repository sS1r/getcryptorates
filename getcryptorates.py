'''
Simple script for reading cryptocurrency rates automatically

2020-10-09, ss1r

LICENSE: If you find this code, do whatever the fuck you want with it
'''

from apiCG import apiCG

import datetime

API_ROOT_URL = "https://api.coingecko.com/api/v3/"
COINS_REQUESTED = ["btc", "eth", "ltc"]
TARGET_CURRENCIES = ["eur", "usd"]

api = apiCG(API_ROOT_URL)

if api.server_up():
	api.send_request(COINS_REQUESTED, TARGET_CURRENCIES)
	output = api.get_output_str()
	currentime = datetime.datetime.now().replace(microsecond=0)
	print("Cryptocurrency rates (" +  currentime.isoformat(sep=" ") + "):")
	print(output)
else:
	print("Crypto server down :(")
	print("Server address: " + API_ROOT_URL)
	
