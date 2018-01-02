from __future__ import division
import pandas as pd

def count_prob_pos(word,df):
    
    prob_word = ( df.loc[word]['positive'] + 1 ) / (df['positive'].sum() + len(df.index))

    return prob_word


def count_prob_neg(word,df):
    
    prob_word = ( df.loc[word]['negative'] + 1 ) / (df['negative'].sum() + len(df.index))

    return prob_word