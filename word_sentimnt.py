#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 17:44:07 2018

@author: Mengxi Shen
"""
# This program needs approximately 5min to run
import csv, operator, json, nltk
import nltk.corpus
from nltk.corpus import stopwords
words4 = []
wsdict = {} 
review_corpus = []
lem = nltk.WordNetLemmatizer()
all_words = set(nltk.corpus.words.words("en")) 
swords = set(stopwords.words('english'))

with open("yelp_academic_dataset_review_small.json") as infile:
    data = json.load(infile)
for i in range(len(data)):
    # break each review into individual words
    words1 = set(nltk.word_tokenize(data[i]['text'].lower()))
    # eliminate stop words and words that are not in corpus
    words2 = set([word for word in words1 if word not in swords and word.isalpha()])
    # lemmatize words
    review_corpus.append([lem.lemmatize(w) for w in words2])
    # eliminate words that are not in english corpus
    words3 = [set(review_corpus[i]) & all_words]
    words4.extend(words3)
    # assign each word to its star rating
    for key in list(words4[i]):
        if key not in wsdict:
            wsdict[key] = [data[i]['stars']]
        else:
            wsdict[key].append(data[i]['stars'])
# discard lemma used in fewer than 10 times
lemma_dict = {k:v for k, v in wsdict.items() if len(v) > 10}
# build lemma:associative-average-star-rating dictionary
for k, v in lemma_dict.items():
    lemma_dict[k] = sum(v)/len(v)
# sort by the values of lemma:associative-average-star-rating dictionary
slemma = sorted(lemma_dict.items(), key=operator.itemgetter(1), reverse=False)
with open("sentiment.csv", "w") as outfile:
    writer = csv.writer(outfile, delimiter=",")
    writer.writerow(["Lemma", "Sentiment Level"])
# write the 500 most negative lemma into the CSV file
    for row in slemma[:500]:
        writer.writerow(row)
# write the 500 most positive lemma into the CSV file
    for row in slemma[-500:]:
        writer.writerow(row)