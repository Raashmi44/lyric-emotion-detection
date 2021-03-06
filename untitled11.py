# -*- coding: utf-8 -*-
"""Untitled11.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1O2LSlEUBEBrkWRK6QkkiVO0EE9p3evQj
"""

pip install lyrics-extractor

import pandas as pd
single_label = pd.read_csv('SingleLabel.csv', encoding='utf-8')

labels = single_label['label']
unique_labels = labels.unique()
print("Unique labels are:")
unique_labels

#print(single_label.loc[1]['lyrics'])
single_label.head()

single_label['label'].value_counts()

from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt 
word_dict = dict()
for val in unique_labels:
    sentences = ""
    for l in single_label.loc[single_label['label'] == val]['lyrics']:
        sentences += " " + l
    word_dict[val] =sentences
for key in word_dict:
    word_cloud = WordCloud(width = 300, height = 300, 
                    background_color ='white', 
                    stopwords = STOPWORDS,
                    max_words = 50, 
                    min_font_size = 8).generate(word_dict[key])
    plt.figure(figsize = (6, 6)) 
    
    plt.title(str(key))
    plt.imshow(word_cloud)
    plt.savefig(str(key) + ".png")

multi_label = pd.read_csv('MultiLabel.csv')
multi_label.head()

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier


from sklearn.model_selection import cross_val_score
from sklearn import metrics
import numpy as np
import itertools
import nltk

X = single_label['lyrics']
y = single_label['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state = 42)

emotions =['sadness','tension','tenderness','power','nostalgia','solemnity','joyful activation','calmness','amazement']
emotion_dtm = pd.read_csv('MultiLabel.csv')
emotion_dtm.head()

freqs = emotion_dtm.labels
freqs=[i.split(',') for i in freqs]
f={}
for i in emotions:
  f[i]=0
for each_line in freqs:
  for each_word in each_line:
    each_word=each_word.lower()
    each_word=each_word.strip()
    f[each_word]+=1

result = f
freq_count = pd.DataFrame(result.items(), columns=['Emotions', 'Counts'])
freq_sorted = freq_count.sort_values(['Counts'], ascending=False)
freq_sorted

emotion_per_example = [len(i) for i in freqs ]

print('Maximum emotions per example: %d'%max(emotion_per_example))
print('Minimum emotions per example: %d'%min(emotion_per_example))
print('Average emotions per example: %f'% ((sum(emotion_per_example))/len(emotion_per_example)))

from sklearn.preprocessing import MultiLabelBinarizer

mlb = MultiLabelBinarizer()
y = mlb.fit_transform(multi_label['labels'])
y

tfv = TfidfVectorizer(min_df=3, max_features=3000, strip_accents='unicode',lowercase =True,
                            analyzer='word', token_pattern=r'\w{3,}', ngram_range=(1,1),
                            use_idf=True,smooth_idf=True, sublinear_tf=True, stop_words = "english")
lr = LogisticRegression()
clf = OneVsRestClassifier(lr)
pipeline = make_pipeline(tfv, clf)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state = 42)

from sklearn.metrics import f1_score
pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
print('F1-SCORE :',f1_score(y_test, y_pred, average="micro"))

y_pred

from lyrics_extractor import SongLyrics 
extract_lyrics = SongLyrics('AIzaSyC19pmh__2zu8uMfc7m6O2jYgtwGGP0wJQ', '3bf2eaea105f081a0')
song=input("Enter Song Name ")
so=extract_lyrics.get_lyrics(song)
p=so['lyrics'].index(']')
ff=so['lyrics'][(p+1):]
mul = pd.DataFrame([ff], columns=['lyrics'])
mul.to_csv('cities.csv')
mul = pd.read_csv('cities.csv', encoding='utf-8')
x1= mul['lyrics']

y1 = mlb.fit_transform(multi_label['labels'])
y_pre = pipeline.predict(x1)
x1

print('F1-SCORE :',f1_score(y1[0], y_pre[0], average="micro"))
j=0
c=0
for i in y1:
  if(f1_score(i, y_pre[0], average="micro")>0.95):
    c+=1
    print(emotion_dtm['title'][j])
  j+=1
print("total no of songs recommended =",c)



