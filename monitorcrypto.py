'''
Script for alerting if cryptocurrency prices get above / below certain limit

2020-10-16, ss1r

LICENSE: If you find this code, do whatever the fuck you want with it
'''

from apiCG import apiCG

import datetime
import os
import argparse
import time

from plyer.utils import platform
from plyer import notification

API_ROOT_URL = "https://api.coingecko.com/api/v3/"
ALERT_PERIOD = 30 * 60 # Time between alerts (secs)

def main():

	# Parse arguments
	parser = argparse.ArgumentParser(description='Get crypto rates')
	parser.add_argument('--coin',     action='store', type=str,   nargs='?', default='btc',   help='Coin to monitor')
	parser.add_argument('--currency', action='store', type=str,   nargs='?', default='usd',   help='Currency to monitor')
	parser.add_argument('--limit',    action='store', type=float, nargs='?', default=15000.0, help='Exchange rate which triggers the alert')
	parser.add_argument('--trigtype', action='store', type=str,   nargs='?', default='above', help='Trigger type (above or below)')
	parser.add_argument('--pollrate', action='store', type=float, nargs='?', default=30.0,    help='Server poll rate (polls / minute)')
	args = parser.parse_args()

	api = apiCG(API_ROOT_URL)
	quit = False
	alert_time = 0;
	
	while not quit:

		# Send request
		coins = [args.coin]
		currencies = [args.currency]
		if not api.send_request(coins, currencies):
			print("Could not fetch data from server")
			quit = True
		
		# Check the exchange rate
		rate = api.get_rate(args.coin, args.currency)
		if rate:
			print("Rate is " + str(rate))
			
			# Determine if the trigger occured
			triggered = False
			if args.trigtype == 'above' and rate > args.limit:
				triggered = True
			elif args.trigtype == 'below' and rate < args.limit:
				triggered = True
			
			# Set alert
			if triggered:
				if time.time() - alert_time > ALERT_PERIOD:
					alert_time = time.time()
					unit = args.currency + "/" + args.coin
					msg = "Exchange rate: " + str(rate) + " " + unit + "\n"
					msg += "Limit set to " + str(args.limit) + " " + unit
					notification.notify(title='Crypto monitor alert', message=msg, app_name='monitorcrypto.py')
		else:
			print("Data not available")
			quit = True
			
		# Wait
		time.sleep(60.0 / args.pollrate)

if __name__ == "__main__":
    main()