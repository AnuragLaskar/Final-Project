import numpy as np
import pandas as pd
import preprocess as PP
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

df = pd.read_csv(filepath_or_buffer="../Data/Training/training_dataset.csv",names=['senti','text'])

df_x = df['text']
df_y = df['senti']
x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size=0.2, random_state=4)

# read stop word from data and add to stop_words list
with open("../Data/Classifier/stop-word.txt") as f:
    stop_word_list = f.readlines()
stop_word_list = [x.strip() for x in stop_word_list]

cv = TfidfVectorizer(min_df=1,stop_words=stop_word_list)

x_traincv = cv.fit_transform(x_train)
a=x_traincv.toarray()
# cv.inverse_transform(a[0])


x_testcv=cv.transform(x_test)

clf = svm.SVC(kernel='linear',C=1.0)
clf.fit(x_traincv,y_train)






