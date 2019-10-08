import pandas as pds
import os
import numpy as np
import pickle
from nltk.corpus import wordnet 

def get_synonyms(word):
    synonyms = []
    for syn in wordnet.synsets(word): 
        for l in syn.lemmas(): 
            synonyms.append(l.name()) 
    synonyms = sorted(list(set(synonyms)))
    outStr = ""
    for syn in synonyms:
        if syn != word:
            outStr += syn
            outStr += ", "
    return outStr

# cond = df["Source"] == "princeton"
pickleName = "/storage/emulated/0/qpython/projects/GRE/dataFrame.p"
df = pickle.load(open(pickleName, "rb"))
temp_df = df.sample(frac=1).reset_index(drop=True)
words = []
scores = {}

for (word, score, src, c, ic) in zip(temp_df["Word"], temp_df["Score"], 
                              temp_df["Source"], temp_df["Correct"], 
                              temp_df["Incorrect"]):
    if (score<0.61):
        words.append(word)
        scores[word] = score

def key_scores(word):
    global scores
    return scores[word]

sorted_words = sorted(words, key=key_scores)
length = len(sorted_words)
fin_score = 0

groupSize = input("Group size for revision: ")
if len(groupSize)<2:
    groupSize = 30
else:
    groupSize = int(groupSize)
    
groupCount = int(np.ceil(length/groupSize))


for groupIndex in range(groupCount):
    currSet = sorted_words[groupIndex*groupSize:(groupIndex+1)*groupSize]
    for sweepIndex in range(2):
        np.random.shuffle(currSet)
        x = 0
        for i, word in enumerate(currSet):
            cond = (df["Word"] == word)
            index = df[cond].index[0]
            row = df.iloc[index]
            mean = row["Meaning"]
            mean = mean.replace("2" , "\n2")
            usage = row["Usage"]
            usage = usage.replace("2", "\n2")
            s = row["Score"]
            if s == -2:
                string = "New"
            else:
                string = str(int(s*100.))

            temp = input("G%d/%d: R%d/2: W%d/%d) %s => Score: %s%%"%(groupIndex+1, groupCount, sweepIndex+1,
                                                         i+1, groupSize, word.upper(), string))
            print("\nSource : %s\n%s = %s\n\nEx: %s\nSynonyms: %s"%(row["Source"], 
                                                        row["Word"].upper(), 
                                                        mean, 
                                                        usage, get_synonyms(row["Word"])))
            correct = input("Remember? :: Y/N ").lower()
            if len(correct) == 0:
                break

            if (correct[0] == "y"):
                df.at[index, "Correct"] += 1
                x += 1
                fin_score += 1
            else:
                df.at[index, "Incorrect"] += (1+sweepIndex)
            os.system("clear")
            c = df.at[index, "Correct"]
            ic = df.at[index, "Incorrect"]

            df.at[index, "Score"] = float(c)/float(c+ic)
            pickle.dump(df, open(pickleName, "wb"))
        print("Score: G%d/%d :: %d/%d"%(groupIndex+1, groupCount, x, groupSize))

print("\nEnding revision %d/%d!"%(fin_score, i))