# coding: utf-8
import sys
import os
import gensim

from gensim.models import KeyedVectors
from gensim.models import Word2Vec
from scipy import stats
import numpy as np
import pandas as pd

corpusdir = "./corpus/"
file_jwsan = corpusdir + "JWSAN/jwsan-1400.csv"
file_w2v_hottolink = corpusdir + "w2v_all_vector200_win5_sgns0.vec"
file_w2v_wiki_hotto = corpusdir + "w2v_wiki_vector100_win5_sgns1.vec"
file_w2v_wiki_inui = corpusdir + "jawiki.word_vectors.200d.txt"


model_hottolink = KeyedVectors.load_word2vec_format(file_w2v_hottolink, binary=False) 
model_wiki_inui = KeyedVectors.load_word2vec_format(file_w2v_wiki_inui, binary=False) 
model_wiki_hotto = KeyedVectors.load_word2vec_format(file_w2v_wiki_hotto, binary=False) 


def get_ranklist(df,index_name):
    return df.assign(order=np.argsort(df.sort_values(index_name).index))

def evaluate_model(model,df_answer):

    df_test = pd.DataFrame(index=[], columns=['word1', 'word2','similarity'])
    for index,row in df_answer.iterrows():
        if(row["word1"] in model.wv and row["word2"]in model.wv):
            sim = model.wv.similarity(row["word1"],row["word2"])
        else:
            sim = 0.0
        df_test = df_test.append(pd.Series([row["word1"],row["word2"],sim],index=df_test.columns), ignore_index=True)
    df_answer = get_ranklist(df_answer,"similarity")
    df_test = get_ranklist(df_test,"similarity")

    corr, p_value = stats.spearmanr(df_answer.order, df_test.order)

    print("%1.3f" % (corr))

if __name__ == '__main__':
    df_answer_jwsan = pd.read_csv(file_jwsan)
    evaluate_model(model_hottolink,df_answer_jwsan)
    evaluate_model(model_wiki_inui,df_answer_jwsan)
    evaluate_model(model_wiki_hotto,df_answer_jwsan)
