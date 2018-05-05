import collections
import nltk.classify.util
from nltk.classify import MaxentClassifier
import csv
import random
import itertools

import pandas as pd
import preprocess as PP
 
posdata = []
negdata = []

train_df = pd.read_csv(filepath_or_buffer="../Data/Training/train.csv",header=None)

total_test = len(train_df.index)
print "Be Patient...!"

for i in range(total_test):
    
    senti = train_df.loc[i][0]
    if senti=="positive":
        text = train_df.loc[i][1]
        text = PP.clean_tweet(text)
        posdata.append(text)
    else:
        text = train_df.loc[i][1]
        text = PP.clean_tweet(text)
        negdata.append(text)

def word_split(data):    
    data_new = []
    for word in data:
        word_filter = [i.lower() for i in word.split()]
        data_new.append(word_filter)
    return data_new
  
def word_feats(words):    
    return dict([(word, True) for word in words])
 
with open("../Data/Classifier/stop-word.txt") as f:
    stop_words = f.readlines()
stop_words = [x.strip() for x in stop_words]

# stop_words = set([x.strip() for x in stop_words]) - set(('over', 'under', 'below', 'more', 'most', 'no', 'not', 'only', 'such', 'few', 'so', 'too', 'very', 'just', 'any', 'once'))


     
def stopword_filtered_word_feats(words):
    return dict([(word, True) for word in words if word not in stop_words])
 

def evaluate_classifier(featx):
    
    negfeats = [(featx(f), 'neg') for f in word_split(negdata)]
    posfeats = [(featx(f), 'pos') for f in word_split(posdata)]

    trainfeats = negfeats + posfeats    
  
    random.shuffle(trainfeats)    
    n = 5 
    

    
    subset_size = len(trainfeats) / n
    accuracy = []
    classi = None
    cv_count = 1
    for i in range(n):        
        testing_this_round = trainfeats[i*subset_size:][:subset_size]
        training_this_round = trainfeats[:i*subset_size] + trainfeats[(i+1)*subset_size:]
        
    
        classifierName = 'Maximum Entropy'
        classifier = MaxentClassifier.train(training_this_round, 'IIS', trace=0, encoding=None, labels=None, gaussian_prior_sigma=0, max_iter = 1)
        classi = classifier
                
        refsets = collections.defaultdict(set)
        testsets = collections.defaultdict(set)
        for i, (feats, label) in enumerate(testing_this_round):
            refsets[label].add(i)
            observed = classifier.classify(feats)
            testsets[observed].add(i)
        cv_accuracy = nltk.classify.util.accuracy(classifier, testing_this_round)
                
        accuracy.append(cv_accuracy)
        
        cv_count += 1

    print '---------------------------------------'
    print '(' + classifierName + ')'
    print '---------------------------------------'
    print 'accuracy:', sum(accuracy) / n
    print ''

print ''
print 'With Stop Words'
evaluate_classifier(word_feats)
    
print 'Without Stop Words'
evaluate_classifier(stopword_filtered_word_feats)