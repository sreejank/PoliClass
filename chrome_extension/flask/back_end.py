from flask import Flask
from flask import render_template
from flask import request
import json
from watson_developer_cloud import AlchemyLanguageV1
#import enchant
import unicodedata
from requests.utils import quote
import urlparse
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('manual.html');

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    #processed_text = text.upper()
    #throw text into classifier
    return "process"

@app.route('/random/<path:link>')
def give_num(link):
	scale = random.randint(0,5)
	return str(scale)

@app.route('/classify/<path:link>', methods=['GET'])
def classify(link):
	#link is escaped
	print(link)
	page_text = get_text(link)
	if text_is_conservative(text):
		return "RIGHT"
	return "LEFT"

def text_is_conservative(text):
	return True

def get_text(link):

	with open("english_words.txt") as word_file:
		english_words = set(word.strip().lower() for word in word_file)

    # word_file = open("english_words.txt")
    # for word in word_file:
    # 	english_words = (set(word.strip.lower()))

	#link = urlparse.unquote(link)
	alchemy_language = AlchemyLanguageV1(api_key='b299a98dda5788d296ef0daa33bf74c54afff1f7')
	txt = json.dumps(alchemy_language.text(url=link),indent=0)
	txt = json.loads(txt)
	txt = txt['text']
	string = []
	#d = enchant.Dict("en_US")
	if(type(txt) == type(u'')):
		txt = unicodedata.normalize('NFKD', txt).encode('ascii','ignore')
	text_list = txt.split();

	for elem in text_list:
		if(not elem[-1].isalpha()):
			elem = elem[0:-1]
		elem = elem.lower()
		if elem in english_words:
			string.append(elem)
	ans = ' '.join(string)
	return ans


