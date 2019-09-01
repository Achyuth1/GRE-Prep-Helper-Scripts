import pickle
import os
import numpy as np


if os.path.exists("./revise/fileNames.p"):
	fileNames = pickle.load(open("./revise/fileNames.p", "rb"))
	finalGroup = pickle.load(open("./revise/words_all.p", "rb"))
else:
	fileNames = []
	finalGroup = {}

for fileName in os.listdir("./files/"):
	if not fileName in fileNames:
		temp = pickle.load(open("./files/"+fileName, "rb"))
		fileNames += [fileName]
		for (word,mean) in temp.items():
			if not word in finalGroup.keys():
				finalGroup[word] = {"meaning": mean, "wrongCount":0, "correctCount":0}

pickle.dump(fileNames, open("./revise/fileNames.p", "wb"))
pickle.dump(finalGroup, open("./revise/words_all.p", "wb"))

wordsAll = list(finalGroup.keys())
np.random.shuffle(wordsAll)

print("Shuffling %d words from %s"%(len(wordsAll), str(fileNames)))

for word in wordsAll:
	temp = input("Meaning of the word %s = "%word)
	if len(temp)<2:
		break
	print(finalGroup[word]["meaning"])
	status = input("Y/N: ")
	if status== "y" or status == "Y":
		finalGroup[word]["correctCount"] += 1
	else:
		finalGroup[word]["wrongCount"] += 1
	pickle.dump(finalGroup, open("./revise/words_all.p", "wb"))


outStr = "word,meaning,score\n"
for word in sorted(wordsAll):
	if finalGroup[word]["correctCount"]+finalGroup[word]["wrongCount"] == 0:
		acc = -1
	else:
		acc = float(finalGroup[word]["correctCount"])*100.0/ (finalGroup[word]["correctCount"] + finalGroup[word]["wrongCount"])

	outStr += "%s,%s,%f\n"%(word, finalGroup[word]["meaning"].replace(",", " "), acc)

with open("./revise/report.csv", "w") as f:
	f.write(outStr)