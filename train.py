import nltk
import os
from math import log

#Maps word to [democratCount,republicanCount] list.
word_counts={}

#Function for sorting key words. 
def seperationFunction(d,r):
	alpha=0.1
	ratio=abs(float(d-r)/float(d+r))
	logarithm=log(d+r)
	logarithm=logarithm**alpha
	return ratio*logarithm
	


def process_word(word,isDemocrat):
	global word_counts
	if word not in word_counts:
		if isDemocrat:
			word_counts[word]=[1,0]
		else:
			word_counts[word]=[0,1]
	else:
		if isDemocrat:
			word_counts[word][0]+=1
		else:
			word_counts[word][1]+=1

#PATH = 'convote_v1.1/data_stage_two/training_set/'
def process_all_files(PATH):
	print("Processing directory "+PATH)
	for filename in os.listdir(PATH):
		print("Processing "+filename)
		with open(PATH+filename,'r') as file:
			if ".txt" in filename:
				for line in file:
					tokens = nltk.wordpunct_tokenize(line.lower())
					for word in tokens:
						if word.isalpha():
							isDemocrat=(filename[-7]=="D")
							process_word(word,isDemocrat)

def process_file(PATH, isDemocrat):
	print("Processing " + PATH)
	with open(PATH,'r') as file:
		if ".txt" in PATH:
			for line in file:
				tokens = nltk.wordpunct_tokenize(line.lower())
				for word in tokens:
					if word.isalpha():
						process_word(word, isDemocrat)



# process_all_files('convote_v1.1/data_stage_two/training_set/')
# process_all_files('convote_v1.1/data_stage_one/training_set/')
# process_all_files('convote_v1.1/data_stage_one/development_set/')
# process_all_files('convote_v1.1/data_stage_two/development_set/')
# process_all_files('convote_v1.1/data_stage_three/training_set/')
# process_all_files('convote_v1.1/data_stage_three/development_set/')

process_file("training/texts/prolife/focusonlife.txt", False)
process_file("training/texts/prolife/prolifealliance.txt", False)
process_file("training/texts/prochoice/naral.txt", True)

def plotWords():
	differences=[]
	totalOccurances=[]
	for word in word_counts.keys():
		differences.append(abs(word_counts[word][0]-word_counts[word][1]))
		totalOccurances.append(word_counts[word][0]+word_counts[word][1])

	plt.scatter(differences,totalOccurances)
	plt.show()





words=sorted(word_counts.keys(), key=lambda x: seperationFunction(word_counts[x][0],word_counts[x][1]),reverse=True)

outputfilename="Word_Counts.csv"
target=open(outputfilename,'w')
target.write("Word, Democrat, Republican\n")
for word in words:
	target.write(word+","+str(word_counts[word][0])+","+str(word_counts[word][1]))
	target.write("\n")