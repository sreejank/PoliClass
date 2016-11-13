import json
from watson_developer_cloud import AlchemyLanguageV1
import enchant
import unicodedata
from requests.utils import quote
import urlparse

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