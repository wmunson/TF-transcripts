import requests
import re
import pandas as pd
from bs4 import BeautifulSoup


def parse_html(ep_num, link):
	# with open('links.csv', delimiter='\n') as fd:

	urls = [ x for x in pd.read_csv('links.csv', sep='\n').loc[:,'urls']]
	# test = urls.loc[0,'urls']
	for i,url in enumerate(urls):
		print(url)
		episode = 151+i
		req = requests.get(url)
		soup = BeautifulSoup(req.text, 'html.parser')
		main = (soup.find("div",{'class':'entry-content'}))
		ps = (main.findAll('p'))
		# print(ps)
		raw_text = (type(ps[0].get_text()))
		speakers = re.search(r'<p><strong>([A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+):</strong>',str(ps))
		# print((speakers[0]))
		start = []
		speakers = []
		for i, _ in enumerate(ps):
			if re.search(r'<p><strong>([A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+):</strong>',str(_)):
				# print(re.search(r'<p><strong>([A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+):</strong>',str(_)).group(0))
				speakers.append(re.search(r'<p><strong>([A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+):</strong>',str(_)).group(0))
				start.append(i)
		# print(start)
		speakers_set = (set([str(x).replace(':','').replace('<p><strong>','').replace('</strong>','').lower() for x in speakers]))
		guests = [x for x in speakers_set if x != 'tim ferriss']
		try:
			start = start[0]
		except IndexError:
			start = 0
		text_sents = [x.get_text() for x in ps[start:]]
		raw_text = ' '.join([x.get_text() for x in ps])
		# print(raw_text)
		print(len(text_sents))
		# print(ps[0].get_text())
		print(speakers_set)
		print(guests)
		dialog = {}
		for i,p in enumerate(speakers_set):
			dialog[p] = []
		for i,sent in enumerate(text_sents):
			# print(sent)
			for p in speakers_set:
				if re.match(p,sent.lower()):
					dialog[p].append(i)
		# print(dialog)

	

# # Used for making links.csv. Need to move to own file!
def get_urls():
	url = 'https://tim.blog/2018/09/20/all-transcripts-from-the-tim-ferriss-show/?utm_source=convertkit&utm_medium=convertkit&utm_campaign=5bf'
	req = requests.get(url)
	soup = BeautifulSoup(req.text, 'html.parser')
	
	main = soup.find(id='post-36531')
	posts = main.findAll('p')
	hrefs=[]
	episodes = []
	for p in posts:
		# print((p.text.strip()))
		txt = p.text.strip()
		if re.match(r'^(Episode|Ep.|#)', txt):
			print('txt: ',txt)
			try:
				ep = re.match(r'^(Episode |Ep. |Ep |#)(\d+)',txt).groups()
				# print((ep))
				episodes.append(ep[1])
			except:
				print(txt)
			try:
				href = p.a['href']
				# print((href))
				hrefs.append(href)
			except:
				pass

	df = pd.DataFrame({'urls':hrefs,'ep':episodes})
	df.to_csv('links3.csv',index=False,sep='|')
	# print(hrefs)
	# print(episodes)
	print(df)


if __name__ == '__main__':
	# Testing
	# parse_html()
	get_urls()