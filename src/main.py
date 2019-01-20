import pandas as pd
import json
from scraper import parse_html
from pdf_parser import pdf_parser

def main():
	# file = 'pdfs/01-kevin-rose.pdf'
	df = pd.read_csv('links5.csv', sep='|')
	episodes = list(df.loc[:,'ep'])
	urls = list(df.loc[:,'urls'])
	guests = list(df.loc[:,'guests'])
	for i,url in enumerate(urls):
		print(episodes[i], guests[i].split(','))
		if url[-1] == 'f':
			data = pdf_parser(episodes[i],url,guests[i].split(','))
		elif url[-1] == '/':
			data = parse_html(episodes[i],url)
		else:
			print('ERROR ',episodes[i])
			data = {'file_type':'audio'}
		
		with open(f'files/eps/{episodes[i]}.json','w') as fp:
			json.dump(data,fp,sort_keys=True)



if __name__ == '__main__':
	main()