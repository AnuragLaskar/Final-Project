from __future__ import division
import pandas as pd
import preprocess as PP

from progressbar import ProgressBar
pbar = ProgressBar()

# read stop word from data and add to stop_words list
with open("./Data/Classifier/stop-word.txt") as f:
    stop_words = f.readlines()
stop_words = [x.strip() for x in stop_words]

test_df = pd.read_csv(filepath_or_buffer="./Data/Training/test.csv",header=None)
df = pd.read_excel("train_result.xlsx")

result = pd.DataFrame(columns=['Text','Sentiment_pre','Sentiment_cal'])


total_test = len(test_df.index)

for i in pbar(range(total_test)) :
    
    polarity_pos = 1.0
    polarity_neg = 1.0

    text = test_df.loc[i][1]
    c_text = PP.clean_tweet(text)
    temp_list = c_text.split(" ")
    for word in temp_list:
        # Remove Symbols From Words
        word = PP.rem_symbol(word)

        # all word to lowercase
        word = word.lower()
        if len(word)<=1 or PP.is_number(word) :
            continue
        
        if word not in stop_words :
            if word in df.index :
                polarity_pos = (0.5) * polarity_pos * (df.loc[word]["prob_w_p"])
                polarity_neg = (0.5) * polarity_neg * df.loc[word]["prob_w_n"]

    senti = ""
    if polarity_pos > polarity_neg:
        senti = "Positive"
    else:
        senti = "Negative"
    
    result.loc[i] = [text,test_df.loc[i][0],senti]

result.to_excel(excel_writer="test_result.xlsx")
print result