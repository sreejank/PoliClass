"""import urllib
from bs4 import BeautifulSoup

def extract_from_link(link):
	dat = urllib.urlopen(link)
	content = dat.read()
	return content

def extract_text(content):
	soup = BeautifulSoup(content, "html.parser")
	# kill all script and style elements
	for script in soup(["script", "style"]):
	    script.extract()    # rip it out

	# get text
	text = soup.get_text()

	# break into lines and remove leading and trailing space on each
	lines = (line.strip() for line in text.splitlines())
	# break multi-headlines into a line each
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	# drop blank lines
	text = '\n'.join(chunk for chunk in chunks if chunk)
	return text

def clean_text_from_link(link):
	content = extract_from_link(link)
	text = extract_text(content)
	return text
"""

from lxml import html
import requests
import enchant
import unicodedata

page = requests.get('http://www.nytimes.com/2016/11/13/us/politics/donald-trump-administration-appointments.html')
tree = html.fromstring(page.content)
text_list = tree.xpath('//p/text()')
string = []
d = enchant.Dict("en_US")

for elem in text_list:
	temp = elem.split()
	for a in temp:
		if d.check(a):
			if(type(a) == type(u'')):
				a = unicodedata.normalize('NFKD', a).encode('ascii','ignore')
			if(a[-1] == '.'):
				a = a[0:-1]
			a = a.lower()
			string.append(a)





