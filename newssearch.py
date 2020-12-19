import requests
from bs4 import BeautifulSoup
import re
import pickle

def main():
	url = 'https://www.businesswire.com/portal/site/home/template.PAGE/news/'
	page = requests.get(url)

	soup = BeautifulSoup(page.content, 'html.parser')

	divs = soup.find_all('div', {'itemtype':'http://schema.org/NewsArticle'})
	# finds all headline divs

	headlines_tags_dict = {}
	for item in divs:
		k = item.find('span', {'itemprop': 'headline'}) # just span is sufficient
		v_raw = item.find('a')
		v_str = str(v_raw)			# needed to extract url
		url_str = re.findall(r'"(.*?)"', v_str)[0]
		head_url = 'https://www.businesswire.com' + url_str
		headlines_tags_dict.update({k: head_url})
		# item.find('a') # turns up links - find_all would do more but one shold do

	headlines_text_dict = {}
	for headline, u in headlines_tags_dict.items():
		if headline is None:
			continue
		head_text = headline.contents[0]
		headlines_text_dict.update({head_text: u})


	keywords = ['Market', 'Offering', 'Growth', 'Project']

	results_dict = {}

	for h, u in headlines_text_dict.items():
		for keyword in keywords:
			if keyword in h:
				results_dict.update({h: u})
				break

	headlines = []
	articles = []
	pair_list = []
	for k, v in results_dict.items():
		articles.append(v)
		headlines.append(k)
		pair_list.append((k, v))

	# Temporary: just cache the URLs (and headlines?) in a file 
	# Can do that directly as the dictionary
	# or that's causing issues, so.

#	print(results_dict)
#	with open('articles-list.pkl', 'w') as f:
#		pickle.dump(results_dict, f)

	pair_string = str(pair_list)
	print(pair_string)
	with open('articles-list.txt', 'w') as f:
		f.write(pair_string)



# After URLs found, do more gets on those pages?
# Search text of the article itself, then. 
# div class ='bw-release-story' makes that part easier at least.

# Tags to look for there: 'ticker', 'symbol' - look for associated sentences?


if __name__ == "__main__":
    main()

