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
#import cPickle as pickle
import nltk
from sklearn.externals import joblib
#from '../../prediction.py' import outputClass


keyWords=[]

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
	# print(link)
	# page_text = get_text(link)
	r = random.randint(0,1)
	if r:
		return "RIGHT"
	return "LEFT"

@app.route('/classify/<path:link>')
def classify(link):
	#link is escaped
	#print(link)
	#print(outputClass("for the second day in a row the liberal michael moore has published a plan for activists to put into motion whats getting all of the attention is item on the list pursuing the impeachment of donald trump its highly unlikely that the requisite minority of obedient house republican members would defend the constitution from a rampaging member of their own party but theoretically it could happen at any time with the number of lawsuits and charges leveled against trump across the country he also wants to ditch the electoral college which at this point makes sense considering that until it had only a failure rate to deliver the most voted candidate and since has failed to deliver the elected candidate to office of the time second list of recipes for the american left to move forward strictly an declaration either beyond proposing that a swift opposition movement emerge he also demanded a program of obstruction to deny supreme court judges reform within the democratic national committee and even an apology to sanders from the party the most immediately doable item on the list would be a special prosecutor to investigate fbi director james partisan interference in this years election theres already a movement to terminate the fbi directors employment for violating the hatch act if there could be a yearlong server investigation surely the government does have the resources to investigate its top lawman after the justice departments office of special counsel rules on the hatch act complaints wish list ended with the national and the personal he called for major changes to our voting systems for federal elections to ensure an accountable paper trail a holiday on election day and to end the disenfranchisement of felons who have completed their sentences heres all of them must quickly and decisively form an opposition movement the likes of which been seen since the will do my part to help lead this as sure many others elizabeth warren the community will too the core of this opposition force will be fueled by young people who as with occupy wall street and black lives matter tolerate and are relentless in their resistance to authority they have no interest in compromising with racists and misogynists prepare to impeach trump just as the republicans were already planning to do with president from day one we must organize the apparatus that will bring charges against him when he violates his oath and breaks the law and then we must remove him from office must commit right now to a vigorous fight civil disobedience if necessary which will block any and all donald trump supreme court nominees who do not meet our approval we demand the democrats in the senate aggressively filibuster any nominees who support citizens united or who oppose the rights of women immigrants and the poor this is demand the apologize to sanders for trying to fix the primaries against him for spinning the press to ignore his historic campaign for giving the questions in advance at the flint debate for its latent ageism and in trying to turn voters against him because of his age or religious beliefs and for its system of who are elected by no one we all know now had been given a fair shot he probably would have been the nominee and he as the true outsider and change candidate would have inspired and fired up the base and soundly defeated donald trump if no apology is soon forthcoming from the thats ok when we take over the democratic party yesterdays list we will issue the apology in person demand that president establish a special prosecutor to investigate who and what was behind fbi director james illegal interference into the presidential election days before the vote was held begin a national push while its fresh in mind for a constitutional amendment to fix our broken electoral system eliminate the electoral college popular vote only paper ballots only no electronic voting election day must be made a holiday for all or held on a weekend so more people vote all citizens regardless of any with the criminal justice system must have the right to vote swing states like florida and virginia of all black men are prohibited by law from convince president to immediately do what he should have done a year ago send in the army corps of engineers to flint to dig up and replace all the poisoned pipes nothing has changed the water in flint is still unusable"))
	#return "LEFT"
	page_text = get_text(link)
	if text_is_conservative(page_text):
		return "RIGHT"
	return "LEFT"

def text_is_conservative(text):
	print text
	res = outputClass(text)
	return res

def outputClass(text):
	global keyWords
	buildKeyWords('Word_Counts.csv')
	trainingVector=[0 for i in range(len(keyWords))]
	clf=joblib.load('TrainedClassifier')
	tokens = nltk.ngrams(nltk.wordpunct_tokenize(text.lower()),3)
	totalWords = 0
	for word in tokens:
		if word[0].isalpha() and word[1].isalpha() and word[2].isalpha():
			totalWords+=1
			if word in keyWords:
				trainingVector[keyWords.index(word)]+=1
		
	for i in range(len(trainingVector)):
		if totalWords!=0:
			trainingVector[i]=1+(trainingVector[i]/totalWords)

	return clf.predict(trainingVector)[0]

def get_text(link):
	with open("english_words.txt") as word_file:
		english_words = set(word.strip().lower() for word in word_file)

    # word_file = open("english_words.txt")
    # for word in word_file:
    # 	english_words = (set(word.strip.lower()))

	#link = urlparse.unquote(link)
	alchemy_language = AlchemyLanguageV1(api_key='396444a062b0b8f61080b23a4b2b461e638bb3a3')
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

def buildKeyWords(keyWordsFileName):
	global keyWords
	f=open(keyWordsFileName,'r')
	for line in f:
		splits=line.split(',')
		keyWords.append((splits[0],splits[1],splits[2]))

	keyWords=keyWords[:500]

