import json
from watson_developer_cloud import AlchemyLanguageV1
import enchant
import unicodedata
from requests.utils import quote
import urlparse
from lxml import html
import requests
import time
import os

page_name = 'motherjones'




def get_text(link):
	#link = urlparse.unquote(link)
	alchemy_language = AlchemyLanguageV1(api_key='b299a98dda5788d296ef0daa33bf74c54afff1f7')
	txt = json.dumps(alchemy_language.text(url=link),indent=0)

	return txt
	# txt = json.loads(txt)
	# txt = txt['text']
	# string = []
	# d = enchant.Dict("en_US")
	# if(type(txt) == type(u'')):
	# 	txt = unicodedata.normalize('NFKD', txt).encode('ascii','ignore')
	# text_list = txt.split();

	# for elem in text_list:
	# 	if d.check(elem):
	# 		if(elem[-1] == '.'):
	# 			elem = elem[0:-1]
	# 		elem = elem.lower()
	# 		string.append(elem)
	# ans = ' '.join(string)
	# return ans

def get_text_d(url):
	page = requests.get(url)
	tree = html.fromstring(page.content)
	article_text = ''

	p = tree.xpath('//div[@id="node-body-top"]//p/text()')
	for text in p:
		if 'newsletter' not in text.encode('utf-8').lower():
			article_text += text.encode('utf-8')
			print(text.encode('utf-8'))

	return article_text

def write_article_content(url):
	print(url)
	# page = requests.get(url)
	# tree = html.fromstring(page.content)
	# article_text = ''

	# p = tree.xpath('//p/text()')
	# for text in p:
	# 	if 'newsletter' not in text.encode('utf-8').lower():
	# 		print(text.encode('utf-8

	### GET TEXT OF PAGE AT URL ###

	article_text = get_text_d(url)


	file_name = page_name + '_' + url.split('/')[-1]
	path = 'texts/articles/' + file_name + '_d.txt'
	print(path)

	output = open(path, 'w')
	output.write(article_text)
	output.write('\n')
	output.close()

def process_breitbart_articles():

	for page_number in range(1, 5):

		section = 'national-security' # or 'national-security'
		URL = 'http://www.breitbart.com/' + section + '/page/' + str(page_number) + '/'
		page = requests.get(URL)
		tree = html.fromstring(page.content)


		articleurls = tree.xpath('//a[@class="thumbnail-url"]/@href') #/@class

		for next_url in articleurls:
			if next_url.startswith('/'):
				#relative path
				next_url = 'http://www.breitbart.com' + next_url
			write_article_content(next_url)
			time.sleep(1)

def process_motherjones_articles():
	for page_number in range(1, 5):
		URL = 'http://www.motherjones.com/politics?page=' + str(page_number)
		page = requests.get(URL)
		tree = html.fromstring(page.content)


		articleurls = tree.xpath('//h3[@class="title"]//a/@href') 

		for next_url in articleurls:
			if next_url.startswith('/'):
				#relative path
				next_url = 'http://www.motherjones.com' + next_url
			write_article_content(next_url)
			time.sleep(5)

process_motherjones_articles()



