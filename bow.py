from sets import Set
import pandas as pd

BOW_df = pd.DataFrame(columns=['scores'])

word_list = Set()

text = "hello world text yo world is bla hello."

temp_list = text.split(" ")

print temp_list

for word in temp_list:
    if word not in word_list:
        word_list.add(word)
        BOW_df.loc[word] = [0]
        BOW_df.loc[word]["scores"] += 1
    else:
        BOW_df.loc[word]["scores"] += 1


print word_list


print BOW_df

def remove_symbols(raw_word):
    