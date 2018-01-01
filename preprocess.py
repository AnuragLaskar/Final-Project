import re

def rem_symbol(word):
    c_word = re.sub('[^a-zA-Z0-9]','',word)
    return c_word

def clean_tweet(tweet):
	return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())