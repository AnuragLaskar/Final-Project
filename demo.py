import preprocess as PP

text = "RT @jkaonline: Japan's leader just won a resounding election victory, but he's still unpopular @CNBC https://t.co/joSR2wpi5V"

clean_text = PP.clean_tweet(text)

print clean_text

clean_text2 = clean_text.split(" ")

clean_text3 = set()

for i in clean_text2:
    clean_text3.add(PP.rem_symbol(i))

print clean_text3

import pandas as pd

df = pd.read_excel("part.xlsx")

for i in df.index :
    print df.loc[i]['positive']

print df.index