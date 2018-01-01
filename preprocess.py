import re

def rem_symbol(word):
    c_word = re.sub('[^a-zA-Z0-9]','',word)
    return c_word

text = "he'sllo.ss iugu@i$gu ^ *SKD(SDSD+-_)SSDSD guyg!u#gu"
