import re
import PyPDF2
import json
import io
import requests

def pdf_parser(ep_num,link, guest):
	# file = 'pdfs/01-kevin-rose.pdf'
	req = requests.get(link)
	pdf_bytes = io.BytesIO(req.content)
	result ={}
	pdf_raw = PyPDF2.PdfFileReader(pdf_bytes)
	# print(pdf_raw)
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
	# pdf = pdf.lower()
	pdf = re.sub( r'^!','',pdf)
	pdf = re.sub( r'( !)(\w)',r'\2',pdf)
	pdf = re.sub( r'([\w,\.\?])(!)(\w)',r'\1 \3',pdf)
	pdf = re.sub( r'([,\.\?])(!)',r'\1 ',pdf)
	pdf = re.sub( r' ! ','i',pdf)
	# print(pdf)

	## Saving title and ep num
	show_details = re.search(r'The Tim Ferriss Show Transcripts (Episode|Episodes) ([0-9,\s]*):[\s]{1,2}(.+[,&]*) Show notes and links at tim.blog/podcast',pdf,re.MULTILINE).groups()
	title_text = show_details[2].lower()
	episode = show_details[1]
	# print(show_details)
	# poss_speakers = re.findall(r'[A-Z][a-z]+ [A-Z][a-z]+: |[A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+: ',pdf)
	# poss_speak_set = set(poss_speakers)
	# # print(poss_speakers)
	# speakers_list = []
	# for poss_speak in poss_speak_set:
	# 	ct = 0
	# 	for s in poss_speakers:
	# 		# print(s, poss_speak)
	# 		if poss_speak == s:
	# 			# print('y')
	# 			ct =+ 1
	# 	if ct >= 1:
	# 		speakers_list.append(poss_speak.strip().replace(':','').lower())
	guest_list = [x.lower() for x in guest if x != 'None']
	speakers_list = guest_list.copy()
	speakers_list.append('tim ferriss')
	# guest_list = [ x for x in speakers_list if x != 'Tim Ferriss']
	
	## Remove headers and speaker names
	pdf = pdf.lower()
	raw_text = pdf.replace(f'the tim ferriss show transcripts episode {episode}:  {title_text} show notes and links at tim.blog/podcast','')
	raw_text = raw_text.strip()
	
	raw_text_list = raw_text.split()
	text_sents = [x.lower().strip() for x in re.split(r'[.?!] ',raw_text)]

#######
# 	still owkring on catpuring guests name. Now works for two-named people, not three-names, and need to chekc for shows where names occure infrquently or only tim talks
#######

	# Checking for episodes with no guests
	# if len(re.findall(guests_text,pdf)) > 1:
	# 	guest_set = set(guests_text.split(','))
	# 	guest_list = [x.strip() for x in guest_set]
	# 	speakers_list = ['tim ferriss']
	# 	speakers_list.extend(guest_list)
	# else:
	# 	guest_list = []
	# 	speakers_list = ['tim ferriss']
		
	# print(re.findall(r'[a-zA-Z]+ [a-zA-Z]+: ',pdf))
	#####
#   working on eleiminating the title from speakers list when Tim solo episode. trying to use re search/find to establish min number of occurance of 'geusts_text' to elimiate title but keep guest names
	#####
	# print(speakers_list)
	# first,last = guest.split()
	

	# with open('files/pdfcheck.txt','w') as fp:
	# 	fp.write(raw_text)

	dialog_starts = {}
	for i,p in enumerate(speakers_list):
		dialog_starts[p] = []

	# Assigning speaker sentences index 
	speak = ''
	for i,sent in enumerate(text_sents):
		# print(sent)
		for p in speakers_list:
			if re.match(p,sent.lower()):
				speak = p
		try:
			dialog_starts[speak].append(i)
		except KeyError:
			pass
	cleaned_sents = text_sents
	for p in speakers_list:
		cleaned_sents = list(map(lambda x:x.replace(f"{p.lower()}: ",''),cleaned_sents))

	words = list(map(lambda x: x.split(' '),cleaned_sents))
	words = [it for sub in words for it in sub]
	
	if len(dialog_starts) > 0:
		show_type = 'pdf'
	else:
		show_type = 'audio'
	result['file_type'] = show_type
	result['episode_num'] = ep_num
	result['guests'] = guest_list
	result['speakers'] = speakers_list
	result['raw_text'] = raw_text.strip()
	result['num_words'] = len(words)
	result['num_sentences'] = len(text_sents)
	result['text_sentences'] = cleaned_sents
	result['dialog_idx'] = dialog_starts


	return result

	# print((guest_text_list))
	# print(result)
	# with open('files/pdfcheck.txt','w') as fp:
	# 	fp.write(pdf)



if __name__ == '__main__':
	data = pdf_parser(63,'https://fhww.files.wordpress.com/2018/07/15-neil-strauss.pdf', ['Neil Strauss'])
	with open('files/Testpdf.json','w') as fp:
		json.dump(data,fp,sort_keys=True)
