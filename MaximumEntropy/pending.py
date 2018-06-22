import collections
import nltk.classify.util
from nltk.classify import MaxentClassifier
import csv
from sklearn import cross_validation
import random
from nltk.corpus import stopwords
import itertools
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk import precision , recall , f_measure
import pandas as pd
import preprocess as PP
 
posdata = []
negdata = []

train_df = pd.read_csv(filepath_or_buffer="../Data/Training/full_training_dataset.csv",header=None)

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
 
def word_split_sentiment(data):
    data_new = []
    for (word, sentiment) in data:
        word_filter = [i.lower() for i in word.split()]
        data_new.append((word_filter, sentiment))
    return data_new
    
def word_feats(words):    
    return dict([(word, True) for word in words])
 
with open("../Data/Classifier/stop-word.txt") as f:
    stop_words = f.readlines()
stop_words = [x.strip() for x in stop_words]

def stopword_filtered_word_feats(words):
    return dict([(word, True) for word in words if word not in stop_words])
 

def evaluate_classifier(featx):
    
    negfeats = [(featx(f), 'neg') for f in word_split(negdata)]
    posfeats = [(featx(f), 'pos') for f in word_split(posdata)]
        
    negcutoff = len(negfeats)*3/4
    poscutoff = len(posfeats)*3/4
 
    trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
    testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
    

    classifierName = 'Maximum Entropy'
    classifier = MaxentClassifier.train(trainfeats, 'GIS', trace=0, encoding=None, labels=None, gaussian_prior_sigma=0, max_iter = 1)
    
        
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)

    for i, (feats, label) in enumerate(testfeats):
            refsets[label].add(i)
            observed = classifier.classify(feats)
            testsets[observed].add(i)

    accuracy = nltk.classify.util.accuracy(classifier, testfeats)
    
    print ''
    print '---------------------------------------'
    print 'SINGLE FOLD RESULT ' + '(' + classifierName + ')'
    print '---------------------------------------'
    print 'accuracy:', accuracy
            

    print ''
    
    ## CROSS VALIDATION
    
    trainfeats = negfeats + posfeats    
    
    # SHUFFLE TRAIN SET
    # As in cross validation, the test chunk might have only negative or only positive data    
    random.shuffle(trainfeats)    
    n = 5 # 5-fold cross-validation    
    

    
    subset_size = len(trainfeats) / n
    accuracy = []
   
    cv_count = 1
    for i in range(n):        
        testing_this_round = trainfeats[i*subset_size:][:subset_size]
        training_this_round = trainfeats[:i*subset_size] + trainfeats[(i+1)*subset_size:]
        
    
        classifierName = 'Maximum Entropy'
        classifier = MaxentClassifier.train(training_this_round, 'GIS', trace=0, encoding=None, labels=None, gaussian_prior_sigma=0, max_iter = 1)
        
                
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
    print 'N-FOLD CROSS VALIDATION RESULT ' + '(' + classifierName + ')'
    print '---------------------------------------'
    print 'accuracy:', sum(accuracy) / n
    print ''

    
# evaluate_classifier(word_feats)
evaluate_classifier(stopword_filtered_word_feats)
#evaluate_classifier(bigram_word_feats)    
#evaluate_classifier(bigram_word_feats_stopwords)