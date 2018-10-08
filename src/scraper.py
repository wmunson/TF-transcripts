import requests
import pandas as pd
from bs4 import BeautifulSoup

def main():
	parse_html()

def parse_html():
	# with open('links.csv', delimiter='\n') as fd:

	urls = pd.read_csv('links.csv', sep='\n')
	test = urls.loc[20,'urls']
	# print(test)
	req = requests.get(test)
	soup = BeautifulSoup(req.text, 'html.parser')
	main = (soup.find("div",{'class':'entry-content'}))
	ps = (main.findAll('p'))
	start = []
	for i,_ in enumerate(ps):
		print(str(_))
		print(type(str(_)))
		if '<p><strong>Tim Ferriss:</strong' in str(_):
			start.append(i)
	start = start[0]
	


def get_urls():
	url = 'https://tim.blog/2018/09/20/all-transcripts-from-the-tim-ferriss-show/?utm_source=convertkit&utm_medium=convertkit&utm_campaign=5bf'
	req = requests.get(url)
	soup = BeautifulSoup(req.text, 'html.parser')
	
	main = soup.find(id='post-36531')
	posts = main.findAll('p')
	hrefs=[]
	for p in posts:
		try:
			href = p.a['href']
			
			hrefs.append(href)
		except:
			pass

	df = pd.DataFrame(hrefs)
	df.to_csv('links.csv',index=False)
	# print(hrefs)


if __name__ == '__main__':
	main()