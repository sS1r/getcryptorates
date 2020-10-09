'''
Simple script for reading cryptocurrency rates automatically

2020-10-09, ss1r

LICENSE: If you find this code, do whatever the fuck you want with it
'''

from apiCG import apiCG

import datetime
import configparser

API_ROOT_URL = "https://api.coingecko.com/api/v3/"
CONFIG_FILE = "getcryptorates.ini"

api = apiCG(API_ROOT_URL)

if api.server_up():
	
	# Parse config
	config = configparser.ConfigParser()
	config.read(CONFIG_FILE)
	coins = config["settings"]["coins"].split(",")
	coins = [c.strip() for c in coins]
	currencies = config["settings"]["currencies"].split(",")
	currencies = [c.strip() for c in currencies]
	
	# Send request and print output
	api.send_request(coins, currencies)
	output = api.get_output_str()
	currentime = datetime.datetime.now().replace(microsecond=0)
	print("Cryptocurrency rates (" +  currentime.isoformat(sep=" ") + "):")
	print(output)
else:
	print("Crypto server down :(")
	print("Server address: " + API_ROOT_URL)
	
