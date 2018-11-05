import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

def main():
	parse_html()

def parse_html():
	# with open('links.csv', delimiter='\n') as fd:

	urls = pd.read_csv('links.csv', sep='\n')
	test = urls.loc[20,'urls']
	print(test)
	req = requests.get(test)
	soup = BeautifulSoup(req.text, 'html.parser')
	main = (soup.find("div",{'class':'entry-content'}))
	ps = (main.findAll('p'))
	# print((ps))
	speakers = re.search(r'<p><strong>([A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+):</strong>',str(ps))
	print(type(speakers[0]))
	start = []
	speakers = []
	for i, _ in enumerate(ps):
		if re.search(r'<p><strong>([A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+):</strong>',str(_)):
			print(re.search(r'<p><strong>([A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+):</strong>',str(_)).group(0))
			speakers.append(re.search(r'<p><strong>([A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+):</strong>',str(_)).group(0))
			start.append(i)
	# print(start)
	print(set([str(x).replace(':','') for x in speakers]))
	try:
		start = start[0]
	except IndexError:
		start = 0
	text = [x.get_text() for x in ps[start:]]
	print(text[0:2])
	print(len(text))
	print(ps[0].get_text())
	


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