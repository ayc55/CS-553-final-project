import requests
import json
from os import path
import time
from datetime import datetime
import matplotlib
matplotlib.use("TkAgg")

from matplotlib import pyplot as plt # ? 

import sys

def main(argv):

	params = {
		'access_key': '3061319f37cdab47b5576ed021aeb3af',
		'interval': '15min'
	}

#	ticker = input("Enter a ticker: \n")
	ticker = argv # not error-checking for now

	filename = ticker + '.json'
	if path.exists(filename):
		print("Loading " + filename)
		with open(filename, 'r') as file:
			file_string = file.read()
			api_response = json.loads(file_string)
	else:
		print("Downloading data for " + ticker)
		api_url = 'http://api.marketstack.com/v1/tickers/' + ticker.lower() + '/intraday'
		api_result = requests.get(api_url, params)
		api_response = api_result.json()
		with open(filename, 'w') as file:
			file.write(json.dumps(api_response))

	timeseries = api_response['data']['intraday']

	time_dict = {}

	for item in timeseries:
		time_raw, quote = item['date'], item['last']
		time_struct = time.strptime(time_raw, '%Y-%m-%dT%H:%M:%S%z') # 2020-12-17T20:45:00+0000
		time_dt = datetime.fromtimestamp(time.mktime(time_struct))
		time_dict.update({time_dt: quote})

	# print(time_dict)
	time_list = [(k, v) for k, v in time_dict.items()]
	times = [x[0] for x in time_list]
	values = [x[1] for x in time_list]

	times_today = times[:27]
	values_today = values[:27]

	# Edit this to convert datetime back to string and then save
	# also, don't think I'm going to bother with the 27 bit

	file_save = ticker + '.txt'
	with open(file_save, 'w') as f:
		for i in range(len(time_list)):
			st = str(times[i]) + ',' + str(values[i]) + '\n'
			f.write(st)

# to convert back in other file:
# a = time.strptime(time_str, '%Y-%m-%d %H:%M:%S')
# b = datetime.fromtimestamp(time.mktime(a))

#	plt.plot(times_today, values_today)
#	plt.gcf().autofmt_xdate()
	# plt.plot_date(times, values)
#	plt.show()


if __name__ == "__main__":
    main(sys.argv)

