import re
import PyPDF2
import json
import io
import requests

def pdf_parser(ep_num,link):
	# file = 'pdfs/01-kevin-rose.pdf'
	req = requests.get(link)
	pdf_bytes = io.BytesIO(req.content)
	result ={}
	pdf_raw = PyPDF2.PdfFileReader(pdf_bytes)
	print(pdf_raw)
	num = pdf_raw.numPages
	result['num_pages'] = num
	raw_string = ''
	for i in range(num):
		raw_string += (pdf_raw.getPage(i).extractText())

	# print(raw_string)
	## Text clean up
	pdf = raw_string.replace('!"#$%&\'()*+*,--.\n/,-01*2&3*45%%&667*899*:&\'()6*:565%;5<7','')
	pdf = pdf.replace('\n','|')
	pdf = pdf.replace('. |','')
	pdf = pdf.replace('|','')
	pdf = pdf.replace(' ! ','')
	pdf = pdf.replace('Ò','"')
	pdf = pdf.replace('Ó','"')
	pdf = pdf.replace('Õ',"'")
	pdf = pdf.replace('Õ',"'")
	pdf = pdf.replace('Ð',"-")
	pdf = pdf.lower()
	print(pdf)


	## Saving episode details
	show_details = re.search(r'!the tim ferriss show transcripts episode ([0-9]+):  ([a-z]+ [a-z]+)',pdf,re.MULTILINE).groups()
	guest = show_details[1]
	result['guest'] = guest
	first,last = guest.split()
	episode = show_details[0]
	result['episode_num'] = ep_num


	## Remove headers and speaker names
	raw_text = pdf.replace(f'!the tim ferriss show transcripts episode {episode}:  {guest} show notes and links at tim.blog/podcast','')

	raw_text_list = raw_text.split()
	text_len = len(raw_text_list)
	result['raw_text'] = raw_text.strip()
	result['text_len'] = text_len


	## Save individual speaker text and basic metrics
	sent_start_idx = []
	for i,r in enumerate(raw_text_list):
		if r == 'ferriss:' or r == f"{last}:":
			# print(i,raw_text_list[i:i+3])
			sent_start_idx.append(i)
	result['sent_start_idx'] = sent_start_idx
	
	tim_text_list = []
	guest_text_list = []
	for i, idx in enumerate(sent_start_idx):
		start = idx + 1
		try:
			end = sent_start_idx[i+1]
		except IndexError:
			end = len(raw_text_list)
			print(start, end)
		if raw_text_list[idx] == 'ferriss:':
			tim_text_list.append(' '.join(raw_text_list[start:end-1]))		
		if raw_text_list[idx] == f'{last}:':
			guest_text_list.append(' '.join(raw_text_list[start:end-1]))
	
	tim_text_len = 0
	for t in tim_text_list:
		tim_text_len += len(t.split())
	guest_text_len = 0
	for t in guest_text_list:
		guest_text_len += len(t.split())

	result['tim_text'] = tim_text_list
	result['tim_text_len'] = tim_text_len
	result['guest_text'] = guest_text_list
	result['guest_text_len'] = guest_text_len

	return result
	# print((guest_text_list))
	# print(result)
	# with open('files/json.json','w') as fp:
	# 	json.dump(result,fp,sort_keys=True)



if __name__ == '__main__':
	data = pdf_parser(0,'https://fhww.files.wordpress.com/2018/07/59-alex-blumberg-part-2.pdf')
	with open('files/Testpdf.json','w') as fp:
		json.dump(data,fp,sort_keys=True)
