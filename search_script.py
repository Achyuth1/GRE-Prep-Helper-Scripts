import pickle
import numpy as np

date = input("date: ")
words = pickle.load(open("./files/words_%s.p"%date, "rb"))

while(True):
	key = input("word: ")
	if key in words.keys():
		print("%s = %s\n"%(key, words[key]))
	else:
		print("%s not found or incorrect spelling\n"%key)