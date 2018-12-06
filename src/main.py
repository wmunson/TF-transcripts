import pandas as pd
import json
from scraper import parse_html
from pdf_parser import pdf_parser

def main():
	# file = 'pdfs/01-kevin-rose.pdf'
	urls = pd.read_csv('links3.csv', sep='|')
	print(urls)




if __name__ == '__main__':
	main()