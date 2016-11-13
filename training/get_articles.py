import json
from watson_developer_cloud import AlchemyLanguageV1
import enchant
import unicodedata
from requests.utils import quote
import urlparse
from lxml import html
import requests

page_name = 'breitbart'
filename = 'texts/articles/' + page_name + '_r.txt'
output = open(filename, 'w')

def get_text(link):
	#link = urlparse.unquote(link)
	alchemy_language = AlchemyLanguageV1(api_key='b299a98dda5788d296ef0daa33bf74c54afff1f7')
	txt = json.dumps(alchemy_language.text(url=link),indent=0)
	txt = json.loads(txt)
	txt = txt['text']
	string = []
	d = enchant.Dict("en_US")
	if(type(txt) == type(u'')):
		txt = unicodedata.normalize('NFKD', txt).encode('ascii','ignore')
	text_list = txt.split();

	for elem in text_list:
		if d.check(elem):
			if(elem[-1] == '.'):
				elem = elem[0:-1]
			elem = elem.lower()
			string.append(elem)
	ans = ' '.join(string)
	return ans

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
	article_text = get_text(url)
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



