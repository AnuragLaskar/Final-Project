import pandas as pd
import preprocess as PP

BOW_df = pd.DataFrame(columns=['total','positive','negative'],dtype=int)

word_list = set()

text = "hello world text yo world is bla hello."

temp_list = text.split(" ")

print(temp_list)

for word in temp_list:
    # Remove Symbols From Words
    word = PP.rem_symbol(word)

    if word not in word_list:
        # Add Unique word to the word_list Set and increament the count
        word_list.add(word)
        BOW_df.loc[word] = [0,0,0]
        BOW_df.loc[word]["total"] += 1

    else:

        BOW_df.loc[word]["total"] += 1


print(word_list)


print(BOW_df)

# Write table to Excel File
BOW_df.to_excel(excel_writer="bow.xlsx")