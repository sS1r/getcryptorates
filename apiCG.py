'''
Coingecko API interface

2020-10-09
'''

import requests
from cryptoAPI import cryptoAPI

class apiCG(cryptoAPI):
	
	def __init__(self, url):
		cryptoAPI.__init__(self, url)
		self.coin_id_table = {"eth" : "ethereum", "btc" : "bitcoin", "ltc" : "litecoin", "bnb" : "binancecoin"}
		self.default_curr = "eur"
		
	def server_up(self):
		url = self.url + "/ping"
		headers = {"accept" : "application/json"}
		resp = requests.get(url=url, headers=headers)
		return resp.status_code == 200
	
	def send_request(self, coins, output_currencies):
		url = self.url + "/simple/price"
		headers = {"accept" : "application/json"}
		params = {}
		
		# Construct output currencies string
		output_curr_str = ""
		if type(output_currencies) is list:
			for c in output_currencies:
				output_curr_str += c
				output_curr_str += ","
			output_curr_str = output_curr_str[:-1]
		else:
			output_curr_str = self.default_curr
			
		# Construct ID string for coins
		idstr = ""
		for c in coins:
			if c in self.coin_id_table.keys():
				idstr += self.coin_id_table[c]
				idstr += ","
		idstr = idstr[:-1] # Remove last comma
		
		# Send the query
		params = {"ids" : idstr, "vs_currencies" : output_curr_str}
		resp = requests.get(url=url, headers=headers, params=params)
		
		# Parse JSON content
		json_data = resp.json()
		reverse_coin_table = {v : k for k, v in self.coin_id_table.items()}
		self.data = {}
		for id, prices in json_data.items():
			if id in reverse_coin_table.keys():
				coin_id = reverse_coin_table[id]
				self.data[coin_id] = prices
		
		self.ready = True
