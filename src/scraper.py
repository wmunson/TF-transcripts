import requests
import pandas as pd
from bs4 import BeautifulSoup

def main():
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