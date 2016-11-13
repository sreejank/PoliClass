import nltk
import os
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn import svm

from sklearn.tree import DecisionTreeClassifier, export_graphviz
from scipy.io import loadmat as load
from numpy import argsort, reshape, transpose, array, zeros
from matplotlib.pyplot import imshow, xlabel, ylabel, title, figure, savefig,show
from numpy.random import permutation, seed
from pydotplus import graph_from_dot_data
import pickle
from sklearn.externals import joblib

keyWords=[]

def buildKeyWords(keyWordsFileName):
	global keyWords
	f=open(keyWordsFileName,'r')
	for line in f:
		splits=line.split(',')
		keyWords.append((splits[0],splits[1],splits[2]))

	keyWords=keyWords[:500]


def buildTrainingVector(fileName):
	global keyWords
	f=open(fileName,'r')
	trainingVector=[0 for i in range(len(keyWords))]
	totalWords=0
	for line in f:
		tokens = nltk.ngrams(nltk.wordpunct_tokenize(line.lower()),3)
		for word in tokens:
			if word[0].isalpha() and word[1].isalpha() and word[2].isalpha():
				totalWords+=1
				if word in keyWords:
					trainingVector[keyWords.index(word)]+=1
		
		for i in range(len(trainingVector)):
			if totalWords!=0:
				trainingVector[i]=1+(trainingVector[i]/totalWords)
		
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

	#np.set_printoptions(threshold=np.nan)
	print("Training Features: ")
	print(trainingFeatures)
	print("Training labels: ")
	print(trainingLabels)

	model.fit(trainingFeatures,trainingLabels)

	scores=cross_val_score(model,trainingFeatures,trainingLabels,cv=10)
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

def leaveoneout(x,c,model):
	confusionMatrix=zeros([len(x),len(x)])
	classifiedCorrectly=0.0
	total=len(x)

	for i in range(len(x)):
		out=x[i]
		out_label=c[i]
		

		mask = [True for x in range(len(x))]
		mask=array(mask)


		mask[[i]]=False

		inside=x[mask]
		inside_labels=c[mask]


		model.fit(inside,inside_labels)

		prediction=model.predict(out)
		confusionMatrix[out_label-1,prediction-1]+=1
		if prediction==out_label:
			classifiedCorrectly+=1

	accuracy=classifiedCorrectly/total
	return (confusionMatrix,accuracy)

buildKeyWords('Word_Counts.csv')
print(keyWords)
clf=GaussianNB()
trainData("training/new_crawl/trainingset/",clf)
joblib.dump(clf,"TrainedClassifier",protocol=2)






def outputClass(text):
	clf=joblib.load("TrainedClassifer")
	tokens = nltk.ngrams(nltk.wordpunct_tokenize(text.lower()),3)
	for word in tokens:
		if word[0].isalpha() and word[1].isalpha() and word[2].isalpha():
			totalWords+=1
			if word in keyWords:
				trainingVector[keyWords.index(word)]+=1
		
	for i in range(len(trainingVector)):
		if totalWords!=0:
			trainingVector[i]=1+(trainingVector[i]/totalWords)

	return clf.predict(trainingVector)[0]
		
	




"""
print("----TESTING-----")
preds=[]
actual=[]
for file in os.listdir('training/new_crawl/testingset/'):
	if ".txt" in file:
		print("Prediction "+file)
		if file[-5]=='d':
			actual.append(False)
		else:
			actual.append(True)

		preds.append(clf.predict(buildTrainingVector('training/new_crawl/testingset/'+file))[0])
		print(clf.predict_proba(buildTrainingVector('training/new_crawl/testingset/'+file))[0])

sameDemo=0
sameRepub=0
totalDemos=0
totalRepubs=0
same=0
for i in range(len(preds)):
	if actual[i]==True:
		totalRepubs+=1
		if actual[i]==preds[i]:
			sameRepub+=1
			same+=1
	else:
		totalDemos+=1
		if actual[i]==preds[i]:
			sameDemo+=1
			same+=1

print("TOTAL ACCURACY: "+str(same/len(preds)))
print("CONSERVATIVE ACCURACY: "+str(sameRepub/totalRepubs))
print("LIBERAL ACCURACY: "+str(sameDemo/totalDemos))

print("Predicted demo: "+str(sameDemo))
print("Total demo: "+str(totalDemos))

print("Predicted repub: "+str(sameRepub))
print("Total repub: "+str(totalRepubs))
"""
