import os
import pickle
import numpy as np
import time

temp = time.ctime().split()
fileKey = temp[1]+"_"+temp[2]

def writeWordMeaning(word, words):
	global fileKey
	tMean = input("Enter the meaning for %s: "%tWord)
	if len(tMean)>2:
		words[word] = tMean
		pickle.dump(words, open("./files/words_%s.p"%fileKey, "wb"))
		print("%s = %s\n"%(word, tMean))
	else:
		print("Empty meaning given. Skipping the word\n")
	return


if os.path.exists("./files/words_%s.p"%fileKey):
	words = pickle.load(open("./files/words_%s.p"%fileKey, "rb"))
else:
	words = {}

while(True):
	tWord = input("Enter the word: ")
	tWord = tWord.lower()
	if len(tWord)>2:
		if tWord in words.keys():
			print("word exists in dictionary:\n%s = %s"%(tWord, words[tWord]))
			replace = input("Do you want to replace the word's meaning?Y/N ")
			if replace == "Y" or replace == "y":
				#write word to dict
				writeWordMeaning(tWord, words)
		else:
			#write word to dict
			writeWordMeaning(tWord, words)
	else:
		break

print("======\nWORDS and MEANINGS - %d\n======"%len(words.keys()))
word_list = []
for word in sorted(words.keys()):
	print(word + " = " + words[word])
	word_list += [[word, words[word]]]

np.savetxt("./words_%s.csv"%fileKey, X=np.array(word_list), fmt="%s", delimiter=",")
