import pandas as pd
import preprocess as PP

# read stop word from data and add to stop_words list
with open("./Data/Classifier/stop-word.txt") as f:
    stop_words = f.readlines()
stop_words = [x.strip() for x in stop_words]

# Read test data
test_df = pd.read_csv(filepath_or_buffer="./Data/Training/full_training_dataset.csv",header=None)

# create table (dataframe)
BOW_df = pd.DataFrame(columns=['total','positive','negative'])
STOP_df = pd.DataFrame(columns=['count'])

word_list = set()

total_test = len(test_df.index)
print "Total test : %d" % total_test


total_token = 0

print "Be Patient...!"

for i in range(total_test):
    
    senti = test_df.loc[i][0]
    if senti=="neutral":
        continue
    text = test_df.loc[i][1]

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
                BOW_df.loc[word] = [0,0,0]
                BOW_df.loc[word]["total"] += 1

            else:

                BOW_df.loc[word]["total"] += 1

            if senti=="positive":
                BOW_df.loc[word]["positive"] += 1
            else:
                BOW_df.loc[word]["negative"] += 1
        else:
            if word not in STOP_df.index:
                STOP_df.loc[word]=[0]
                STOP_df.loc[word]['count'] += 1
            else:
                STOP_df.loc[word]['count'] += 1             
                
print "Total Token : %d" % total_token                
print "Total Unique Words : %d" % len(word_list)
print "Total Unique Stop Words : %d" % len(STOP_df.index)
print "Total Stop Words : %d" % (STOP_df['count'].sum())

# print BOW_df

# Write table to Excel File
BOW_df.to_excel(excel_writer="bow.xlsx")
STOP_df.to_excel(excel_writer="stop.xlsx")