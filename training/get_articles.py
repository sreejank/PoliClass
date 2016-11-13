
from lxml import html
import requests
import time
import os

page_name = 'breitbart'


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
	article_text = 'PLACEHOLDER'

	file_name = page_name + '_' + url.split('/')[-2]
	path = 'texts/articles/' + file_name + '_r.txt'
	print(path)
	return 
	output = open(filename, 'w')
	output.write(article_text)
	output.write('\n')
	output.close()

def process_breitbart_articles():

	for page_number in range(1, 5):

		section = 'big-government' # or 'national-security'
		URL = 'http://www.breitbart.com/' + section + '/page/' + str(page_number) + '/'
		page = requests.get(URL)
		tree = html.fromstring(page.content)


		articleurls = tree.xpath('//a[@class="thumbnail-url"]/@href') #/@class

		for next_url in articleurls:
			if next_url.startswith('/'):
				#relative path
				next_url = 'http://www.breitbart.com' + next_url
			write_article_content(next_url)
			# time.sleep(1)

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
			# time.sleep(1)

process_breitbart_articles()



