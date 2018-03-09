from textblob import TextBlob

text = "Tiger zinda hai Fails to cross overseas Record weekend of Raees"

blob = TextBlob(text)

print blob.sentences[0].sentiment.polarity

from sets import Set

s = Set(['bhargab','anurag','debasmit','bhargab'])

print s