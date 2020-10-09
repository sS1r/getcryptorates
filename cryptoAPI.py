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
		self.output_curr = ""
	
	def get_output_str(self):
		output = ""
		if self.ready:
			for curr, rate in self.data.items():
				line = "1 " + curr + " = " + str(rate) + self.output_curr
				output += line + "\n"
		return output
		
	# Abstract
	def server_up(self):
		pass
	
	# Abstract
	def send_request(self, coins, output_currency):
		pass
		