# -*- coding: utf-8 -*-
import preprocess as PP

with open("../Data/Classifier/stop-word.txt") as f:
    stop_words = f.readlines()
stop_words = [x.strip() for x in stop_words]

text = "RT @XHNews: Japan's ruling camp wins two-thirds majority in lower house election amid opposition splitting-up https://t.co/mE2hSxU3xV https…"

# clean_text = PP.clean_tweet(text)

# print clean_text

# clean_text2 = clean_text.split(" ")

# clean_text3 = set()

# for i in clean_text2:
#     clean_text3.add(PP.rem_symbol(i))

# print clean_text3

 
c_text = PP.clean_tweet(text)

temp_list = c_text.split(" ")

out = ""

for word in temp_list:
    # Remove Symbols From Words
    word = PP.rem_symbol(word)

    # all word to lowercase
    word = word.lower()
    if len(word)<=1 or PP.is_number(word) :
        continue
    
    if word not in stop_words :
        out = out + " " + word

print out