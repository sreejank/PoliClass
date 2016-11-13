import json
from watson_developer_cloud import AlchemyLanguageV1
import unicodedata
from requests.utils import quote
from urllib.parse import urlparse
from lxml import html
import requests
import time
import os

page_name = 'occupydemocrats'




def get_text(link):
	#link = urlparse.unquote(link)
	with open("english_words.txt") as word_file:
		english_words = set(word.strip().lower() for word in word_file)
	alchemy_language = AlchemyLanguageV1(api_key='b299a98dda5788d296ef0daa33bf74c54afff1f7')
	txt = json.dumps(alchemy_language.text(url=link),indent=0)
	txt = json.loads(txt)
	txt = txt['text']
	string = []
	if(type(txt) == type(u'')):
		txt = unicodedata.normalize('NFKD', txt).encode('ascii','ignore')
	text_list = txt.split();

	for elem in text_list:
		if type(elem)==type("a"):
			if(not elem[-1].isalpha()):
				elem = elem[0:-1]
			elem = elem.lower()
			if elem in english_words:
				string.append(elem)
	ans = ' '.join(string)
	return ans

def get_text_d(url):
	page = requests.get(url)
	tree = html.fromstring(page.content)
	article_text = ''

	p = tree.xpath('//div[@id="content-main"]/p/text()')
	for text in p:
		if 'newsletter' not in text.encode('utf-8').lower():
			article_text += text.encode('utf-8')

	return article_text

def write_article_content(url):
	# page = requests.get(url)
	# tree = html.fromstring(page.content)
	# article_text = ''

	# p = tree.xpath('//p/text()')
	# for text in p:
	# 	if 'newsletter' not in text.encode('utf-8').lower():
	# 		print(text.encode('utf-8

	### GET TEXT OF PAGE AT URL ###

	article_text = get_text(url)

	print("** Reading URL: " + url)
	print("****** Writing text: " + article_text)

	file_name = page_name + '_' + url.split('/')[-2]
	path = 'texts/articles/' + file_name + '_d.txt'

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


		articleurls = tree.xpath('//h3[@class="title"]/a[@rel="bookmark"/@href') 

		for next_url in articleurls:
			if next_url.startswith('/'):
				#relative path
				next_url = 'http://www.motherjones.com' + next_url
			if not next_url.startswith('http://'):
				continue
			write_article_content(next_url)
			time.sleep(5)

def process_occupy_articles():
	for page_number in range(1, 5):
		URL = 'http://occupydemocrats.com/category/economy/' #+ str(page_number)
		page = requests.get(URL)
		tree = html.fromstring(page.content)


		articleurls = tree.xpath('//li[@class="infinite-post"]//a/@href') 

		for next_url in articleurls:
			if next_url.startswith('/'):
				#relative path
				next_url = 'http://occupydemocrats.com' + next_url
			if not next_url.startswith('http://'):
				continue
			write_article_content(next_url)
			time.sleep(1)

process_occupy_articles()



