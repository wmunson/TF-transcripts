import requests
import re
import pandas as pd
import json
from bs4 import BeautifulSoup


def parse_html(ep_num, link):
	# with open('links.csv', delimiter='\n') as fd:

	# urls = [ x for x in pd.read_csv('links.csv', sep='\n').loc[:,'urls']]
	# # test = urls.loc[0,'urls']
	# for i,url in enumerate(urls[69]):
	result = {}
	result['episode_num'] = ep_num
	# print(ep_num, link)
	req = requests.get(link)
	soup = BeautifulSoup(req.text, 'html.parser')
	main = (soup.find("div",{'class':'entry-content'}))
	ps = (main.findAll('p'))
	# print(len(ps))
	raw_text = (type(ps[0].get_text()))
	speakers = re.search(r'<p><strong>([A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+)',str(ps))
	# print((speakers[0]))
	start = []
	speakers = []
	end = len(ps)
	for i, _ in enumerate(ps):
		txt = str(_).replace('</strong>','')
		if re.search(r'<p><strong>([A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+)',txt):
			# print(re.search(r'<p><strong>([A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+)',txt).group(0),i)
			speakers.append(re.search(r'<p><strong>([A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+)',txt).group(0))
			start.append(i)
		if re.match('<p id="fhcp">',txt):
			# print(i, txt)
			end = i
	# print('end',end)
	speakers_set = (set([str(x).replace('<p><strong>','').replace('</strong>','').lower() for x in speakers]))
	guests = [x for x in speakers_set if x != 'tim ferriss']
	try:
		start = start[0]
	except IndexError:
		start = 0
	raw_text = ' '.join([x.get_text() for x in ps[start:end]])
	text_sents = [x.lower() for x in re.split(r'[.?!] ',raw_text)][:-1]
	# print(raw_text)
	# print(len(text_sents))
	# print(ps[0].get_text())
	print(speakers_set)
	# print(guests)
	# print(text_sents)
	dialog_starts = {}
	for i,p in enumerate(speakers_set):
		dialog_starts[p] = []

	# Assigning speaker sentences index 
	speak = ''
	for i,sent in enumerate(text_sents):
		# print(sent)
		for p in speakers_set:
			if re.match(p,sent.lower()):
				speak = p
		try:
			dialog_starts[speak].append(i)
		except KeyError:
			pass
	cleaned_sents = text_sents
	for p in speakers_set:
		cleaned_sents = list(map(lambda x:x.replace(f"{p.lower()}: ",''),cleaned_sents))
	# print((cleaned_sents))
	# cleaned_sents = (cleaned_sents)
	words = list(map(lambda x: x.split(' '),cleaned_sents))
	words = [it for sub in words for it in sub]
	# print(words)
	if len(dialog_starts) > 0:
		show_type = 'html'
	else:
		show_type = 'audio'
	result['file_type'] = show_type
	result['guests'] = guests
	result['speakers'] = list(speakers_set)
	result['raw_text'] = raw_text.strip()
	result['num_words'] = len(words)
	result['num_sentences'] = len(text_sents)
	result['text_sentences'] = cleaned_sents
	result['dialog_idx'] = dialog_starts


	return result

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
	data = parse_html(0,'https://tim.blog/edward-norton-on-the-tim-ferriss-show-transcript/')
	# data = parse_html(0,'https://tim.blog/2018/06/21/the-tim-ferriss-show-transcripts-soman-chainani/')
	# data = parse_html(0,'https://tim.blog/2018/01/01/the-tim-ferriss-show-transcripts-on-zero-to-hero-transformations/')

	
	with open('files/Testhtml.json','w') as fp:
		json.dump(data,fp,sort_keys=True)

	# get_urls()