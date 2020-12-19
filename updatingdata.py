import requests
from bs4 import BeautifulSoup
import ast
from datetime import datetime

import os

def main(argv):
	ticker = argv

	url = "https://finance.yahoo.com/quote/" + ticker
	quote_time = datetime.now()

	page = requests.get(url)

	soup = BeautifulSoup(page.content, 'html.parser')

	quote_id = 'C($primaryColor) Fz(24px) Fw(b)'

	q_uni = soup.find('span', class_=quote_id).get_text()
	q_string =str(q_uni.encode('ascii','ignore'))
	q_s = q_string.replace('b','').replace(',', '')
	quote = float(ast.literal_eval(q_s))

	time_string = quote_time.strftime('%Y-%m-%d %H:%M:%S')

	ticker_file = ticker + '.txt'
	temp_file = 'temp.txt'

	to_write = time_string + ',' + str(quote) + '\n'

	with open(ticker_file, 'r') as reading, open(temp_file, 'w') as file: # same here
		file.write(to_write)

		for line in reading:
			file.write(line)

	os.remove(ticker_file)
	os.rename(temp_file, ticker_file)



	return (quote_time, quote)


if __name__ == "__main__":
    main(sys.argv)

