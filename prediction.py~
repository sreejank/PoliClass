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
		if line[-1]=='\n':
			line=line[:-1]
		if line.isalpha():
			keyWords.append(line)

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
				labels.append(filename[-7]!='D')

	dataMatrix=np.asarray(dataMatrix)
	labels=np.asarray(labels)
	return (dataMatrix,labels)

def trainData(PATH,model):
	mats=getTrainingMatrix(PATH)
	trainingFeatures=mats[0]
	trainingLabels=mats[1]

	print("Training Features: ")
	print(trainingFeatures)
	print("Training labels: ")
	print(trainingLabels)

	model.fit(trainingFeatures,trainingLabels)

	scores=cross_val_score(model,trainingFeatures,trainingLabels,cv=5)

	print(scores)


buildKeyWords('keywords.csv')
print(keyWords)
clf=GaussianNB()
trainData("convote_v1.1/data_stage_two/training_set/",clf)






