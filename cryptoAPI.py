'''
Generic API interface for fetching crypto data

2020-10-09
'''

import abc

class cryptoAPI(abc.ABC):

	def __init__(self, url):
		self.url = url
		self.ready = False
		self.data = {}
	
	def get_output_str(self):
		output = ""
		if self.ready:
			for coin in sorted(self.data.keys()):
				rates = self.data[coin]
				line = "1 " + coin
				for curr, rate in rates.items():
					line += " = " + str(rate) + " " + curr
				output += line + "\n"
		return output
	
	def get_rate(self, coin, currency):
		if self.data:
			if coin in self.data.keys():
				if currency in self.data[coin].keys():
					return self.data[coin][currency]
	
	# Abstract
	def server_up(self):
		pass
	
	# Abstract
	def send_request(self, coins, output_currencies):
		pass
		