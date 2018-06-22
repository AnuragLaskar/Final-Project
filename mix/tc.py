import re
text = "hello i am dummy text"

# read stop word from data and add to stop_words list
with open("./stop-word.txt") as f:
    stop_words = f.readlines()
stop_words = [x.strip() for x in stop_words]

temp_text_tok = text.split()
text_tok = []

def rem_symbol(word):
    c_word = re.sub('[^a-zA-Z0-9]','',word)
    return c_word

for word in temp_text_tok :
    word = rem_symbol(word)
    if word not in stop_words:
        text_tok.append(word)

print text_tok
