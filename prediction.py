import nltk
import os
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
keyWords=[]

def buildKeyWords(keyWordsFileName):
	global keyWords
	f=open(keyWordsFileName,'r')
	for line in f:
		splits=line.split(',')
		if splits[0].isalpha():
			keyWords.append(splits[0])

	keyWords=keyWords[:500]


def buildTrainingVector(fileName):
	global keyWords
	f=open(fileName,'r')
	trainingVector=[0 for i in range(len(keyWords))]
	for line in f:
		tokens = nltk.wordpunct_tokenize(line.lower())
		for word in tokens:
			if word.isalpha():
				if word in keyWords:
					trainingVector[keyWords.index(word)]+=1

	return trainingVector

def buildTrainingVectorFromText(text):
	global keyWords
	trainingVector=[0 for i in range(len(keyWords))]
	for word in text.split(' '):
		if word.isalpha():
			if word in keyWords:
				trainingVector[keyWords.index(word)]+=1

	return trainingVector


def getTrainingMatrix(PATH):
	print("Training from directory "+PATH)

	dataMatrix=[]
	labels=[]

	for filename in os.listdir(PATH):
		#print("Processing file "+filename)
		with open(PATH+filename,'r') as file:
			if ".txt" in filename:
				dataMatrix.append(buildTrainingVector(PATH+filename))
				#True=Conservative, False=Liberal
				labels.append(filename[-5]=='r')

	dataMatrix=np.asarray(dataMatrix)
	labels=np.asarray(labels)
	return (dataMatrix,labels)

#Train model on all files in PATH. Output 2-fold crossvalidation accuracies.
def trainData(PATH,model):
	mats=getTrainingMatrix(PATH)
	trainingFeatures=mats[0]
	trainingLabels=mats[1]

	print("Training Features: ")
	print(trainingFeatures)
	print("Training labels: ")
	print(trainingLabels)

	model.fit(trainingFeatures,trainingLabels)

	scores=cross_val_score(model,trainingFeatures,trainingLabels)
	print(scores)

	print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

#Gets part of article with most heavy weight in terms of keywords.
def preprocessArticle(text):
	wordLocations={}
	index=0
	counts=[0 for i in range(len(keyWords))]
	for word in text.split(' '):
		if word in keyWords:
			counts[keyWords.index(word)]+=1
			if word not in wordLocations:
				wordLocations[word]=[index]
			else:
				wordLocations[word].append(index)
		index+=1

	sortedWords=sorted(wordLocations,key=lambda x: count[keyWords.index(x)])

	totalMass=sum([i * counts[i] for i in range(len(sortedWords))])

	massdistance=sum([i * sum(wordLocations[sortedWords[i]]) for i in range(len(sortedWords))])

	center_of_mass=massdistance/totalMass


buildKeyWords('Word_Counts.csv')
print(keyWords)
clf=GaussianNB()
trainData("training/texts/articles/",clf)

print("----TESTING-----")
print(clf.predict(buildTrainingVector("article.txt")))
print(clf.predict(buildTrainingVector("article2.txt")))
print(clf.predict(buildTrainingVector("article3.txt")))
print(clf.predict(buildTrainingVector("article4.txt")))
print(clf.predict(buildTrainingVector("article5.txt")))



