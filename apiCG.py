'''
Coingecko API interface

2020-10-09
'''

import requests
from cryptoAPI import cryptoAPI

class apiCG(cryptoAPI):
	
	def __init__(self, url):
		cryptoAPI.__init__(self, url)
		self.coin_id_table = {"eth" : "ethereum", "btc" : "bitcoin", "ltc" : "litecoin"}
		self.curr_id_table = {"eur" : "eur", "usd" : "usd"}
		self.default_curr = "eur"
		
	def server_up(self):
		url = self.url + "/ping"
		headers = {"accept" : "application/json"}
		resp = requests.get(url=url, headers=headers)
		return resp.status_code == 200
	
	def send_request(self, coins, output_currency):
		url = self.url + "/simple/price"
		headers = {"accept" : "application/json"}
		params = {}
		
		# Resolve correct ID for output currency
		if output_currency in self.curr_id_table.keys():
			output_curr_str = self.curr_id_table[output_currency]
			self.output_curr = output_currency
		else:
			output_curr_str = self.curr_id_table[self.default_curr]
			self.output_curr = self.default_curr
			
		# Resolve correct IDs for coins
		idstr = ""
		for c in coins:
			if c in self.coin_id_table.keys():
				idstr += self.coin_id_table[c]
				idstr += ","
		idstr = idstr[:-1] # Remove last comma
		
		params = {"ids" : idstr, "vs_currencies" : output_curr_str}
		resp = requests.get(url=url, headers=headers, params=params)
		
		# Parse JSON content
		json_data = resp.json()
		reverse_coin_table = {v : k for k, v in self.coin_id_table.items()}
		self.data = {}
		for id, val in json_data.items():
			if id in reverse_coin_table.keys():
				coin_id = reverse_coin_table[id]
				price = val[output_curr_str]
				self.data[coin_id] = str(price)
		
		self.ready = True
