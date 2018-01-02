# -*- coding: utf-8 -*-

from __future__ import division
import pandas as pd
import preprocess as PP
import count_prob as CP

from progressbar import ProgressBar
pbar = ProgressBar()

# read stop word from data and add to stop_words list
with open("./Data/Classifier/stop-word.txt") as f:
    stop_words = f.readlines()
stop_words = [x.strip() for x in stop_words]

# Read test data
# train_df = pd.read_csv(filepath_or_buffer="./Data/Training/full_training_dataset.csv",header=None)
train_df = pd.read_csv(filepath_or_buffer="./Data/Training/train.csv",header=None)

# create table (dataframe)
BOW_df = pd.DataFrame(columns=['total','positive','negative','prob_w_p','prob_w_n'])
STOP_df = pd.DataFrame(columns=['count'])

word_list = set()

total_test = len(train_df.index)

pos_test = 0
neg_test = 0
total_token = 0

print "Be Patient...!"

for i in pbar(range(total_test)):
    
    senti = train_df.loc[i][0]
    if senti=="neutral":
        continue
    elif senti=="positive":
        pos_test += 1
    else:
        neg_test += 1
    text = train_df.loc[i][1]

    text = PP.clean_tweet(text)
    temp_list = text.split(" ")

    total_token += len(temp_list)

    for word in temp_list:
        # Remove Symbols From Words
        word = PP.rem_symbol(word)

        # all word to lowercase
        word = word.lower()

        if len(word)<=1 or PP.is_number(word) :
            continue

        if word not in stop_words:
            if word not in word_list:
                # Add Unique word to the word_list Set and increament the count
                word_list.add(word)
                BOW_df.loc[word] = [0,0,0,0,0]
                BOW_df.loc[word]["total"] += 1

            else:

                BOW_df.loc[word]["total"] += 1

            if senti=="positive":
                BOW_df.loc[word]["positive"] += 1
            else:
                BOW_df.loc[word]["negative"] += 1

            # BOW_df.loc[word]['prob_pos'] = BOW_df.loc[word]['positive'] / BOW_df.loc[word]['total']
            # BOW_df.loc[word]['prob_neg'] = BOW_df.loc[word]['negative'] / BOW_df.loc[word]['total']
        else:
            if word not in STOP_df.index:
                STOP_df.loc[word]=[0]
                STOP_df.loc[word]['count'] += 1
            else:
                STOP_df.loc[word]['count'] += 1 


for word in BOW_df.index :
    BOW_df.loc[word]['prob_w_p'] = CP.count_prob_pos(word,BOW_df)
    BOW_df.loc[word]['prob_w_n'] = CP.count_prob_neg(word,BOW_df)
    


print "Total Training Data : %d" % total_test
print "Total Positive Data : %d" % pos_test
print "Total Negative Data : %d" % neg_test
print "Total Token : %d" % total_token                
print "Total Unique Words : %d" % len(word_list)
print "Total Unique Stop Words : %d" % len(STOP_df.index)
print "Total Stop Words : %d" % (STOP_df['count'].sum())


# print BOW_df

# Write table to Excel File
BOW_df.to_excel(excel_writer="train_result.xlsx")
# BOW_df.to_excel(excel_writer="part.xlsx")
# BOW_df.to_csv(path_or_buf="bb.csv")
STOP_df.to_excel(excel_writer="stop.xlsx")