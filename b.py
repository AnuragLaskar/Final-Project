# -*- coding: utf-8 -*-
from __future__ import division
import pandas as pd
import preprocess as PP

# read stop word from data and add to stop_words list
with open("./Data/Classifier/stop-word.txt") as f:
    stop_words = f.readlines()
stop_words = [x.strip() for x in stop_words]

df = pd.read_excel("bow.xlsx")

text = "bhargab hazarika is a bad boy"
clean = PP.clean_tweet(text)


polarity_pos = 1.0
polarity_neg = 1.0
for word in clean.split(" ") :
    
    no_sym_word =  PP.rem_symbol(word)

    if word not in stop_words:
        if word in df.index :
            polarity_pos = (9667/19333) * polarity_pos * (df.loc[word]["prob_w_p"])
            polarity_neg = (9666/19333) * polarity_neg * df.loc[word]["prob_w_n"]

# print polarity_pos
# print polarity_neg

print text 
        
if polarity_pos > polarity_neg:
    print "=> Positive"
else:
    print "=> Negative"
    