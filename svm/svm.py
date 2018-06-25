from __future__ import division
import numpy as np
import pandas as pd
import preprocess as PP
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

df = pd.read_csv(filepath_or_buffer="../Data/Training/training_dataset.csv",names=['senti','text'])

df.loc[df["senti"]=='positive',"senti",]=1
df.loc[df["senti"]=='negative',"senti",]=0

df_x = df['text']
df_y = df['senti']
x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size=0.25, random_state=4)

print "Total Datasets %d" % (len(df))
print "Total Training Datasets %d" % (len(x_train))
print "Total Testing Datasets %d" % (len(x_test))

# read stop word from data and add to stop_words list
with open("../Data/Classifier/stop-word.txt") as f:
    stop_word_list = f.readlines()
stop_word_list = [x.strip() for x in stop_word_list]

cv = TfidfVectorizer(min_df=1,stop_words=stop_word_list)

x_traincv = cv.fit_transform(x_train)
# a=x_traincv.toarray()
# cv.inverse_transform(a[0])

y_train=y_train.astype('int')

x_testcv=cv.transform(x_test)


print "Traning is In Progress Please Wait"

clf = svm.SVC(kernel='linear',C=0.5)
clf.fit(x_traincv,y_train)

predictions=clf.predict(x_testcv)

a=np.array(y_test)

count=0

for i in range (len(predictions)):
    if predictions[i]==a[i]:
        count=count+1

acc = count/len(predictions)
acc*=100
print "Accuracy : %f %% " % acc


result = pd.DataFrame(columns=['Text','Actual','Predicted'])

for i in range(len(y_test)) : 
    # result.loc[i] = [1,2,3]
    result.loc[i] = [df.loc[i][1],y_test[y_test.index[i]],predictions[i]]

result.to_excel(excel_writer="test_result.xlsx")