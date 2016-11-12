import nltk
import os

def process_word(word):
	# Handle each word
	#print(word)
	pass

def process_all_files():
	PATH = 'convote_v1.1/data_stage_two/training_set/'
	for filename in os.listdir(PATH):
		with open(PATH+filename,'r') as file:
			for line in file:
				tokens = nltk.wordpunct_tokenize(line)
				for word in tokens:
					if word.isalpha():
						process_word(word)

def main():
	process_all_files()


main()