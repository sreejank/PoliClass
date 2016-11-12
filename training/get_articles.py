
from lxml import html
import requests

page_name = 'breitbart'
filename = 'texts/articles/' + page_name + '_r.txt'
output = open(filename, 'w')

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
	output.write(article_text)
	output.write('\n')

def process_articles():
	URL = 'http://www.breitbart.com/'
	page = requests.get(URL)
	tree = html.fromstring(page.content)


	articleurls = tree.xpath('//a[@class="thumbnail-url"]/@href') #/@class

	for next_url in articleurls:
		if next_url.startswith('/'):
			#relative path
			next_url = 'http://www.breitbart.com' + a
		write_article_content(a)

process_articles()
output.close()



