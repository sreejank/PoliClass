import json
from watson_developer_cloud import AlchemyLanguageV1
import unicodedata
from requests.utils import quote
#from urllib.parse import urlparse
from lxml import html
import requests
import time
import os

page_name = 'heat'




def get_text(link):
	#link = urlparse.unquote(link)
	with open("english_words.txt") as word_file:
		english_words = set(word.strip().lower() for word in word_file)
	alchemy_language = AlchemyLanguageV1(api_key='396444a062b0b8f61080b23a4b2b461e638bb3a3')
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

	p = tree.xpath('//p/text()')#//p/text()')
	for text in p:
		if(not text[-1].isalpha()):
			text = text[0:-1]
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
	print("****** Writing text *******")

	file_name = page_name + '_' + url.split('/')[-2]
	path = 'new_crawl/heat/' + file_name + '_r.txt'

	output = open(path, 'w')
	output.write(article_text)
	output.write('\n')
	output.close()

def process_breitbart_articles():

	for page_number in range(2, 6):

		section = '2016-presidential-race' # or 'national-security'
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
	for page_number in range(1, 15):
		URL = 'http://www.motherjones.com/politics?page=' + str(page_number)
		page = requests.get(URL)
		tree = html.fromstring(page.content)


		articleurls = tree.xpath('//h3[@class="title"]//a/@href') 

		for next_url in articleurls:
			if next_url.startswith('/'):
				#relative path
				next_url = 'http://www.motherjones.com' + next_url
			if not next_url.startswith('http://'):
				continue
			write_article_content(next_url)
			time.sleep(1)

def process_occupy_articles():
	for page_number in range(21, 30):
		URL = 'http://occupydemocrats.com/category/politics/page/' + str(page_number) + '/'
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
			#time.sleep(1)

def process_huffpo_articles():
	for page_number in range(1, 5):
		URL = 'http://www.huffingtonpost.com/section/queer-voices' #+ str(page_number)
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

def process_heat_articles():
	URL = 'http://heatst.com/politics/'
	page = requests.get(URL)
	tree = html.fromstring(page.content)


	articleurls = tree.xpath('//h2[@class="story-title story-card"]//a/@href') 

	for next_url in articleurls:
		if next_url.startswith('/'):
			#relative path
			next_url = 'http://heatst.com' + next_url
		if not next_url.startswith('http://'):
			continue
		write_article_content(next_url)
		time.sleep(1)

process_heat_articles()



