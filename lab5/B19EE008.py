# -*- coding: utf-8 -*-
"""B19EE008_Lab_Exercise_5 .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AzCWocxq_rT1lFNN5pB3fBo-xB2TWSYt

<font color='orange'>**Please create your own copy before starting modification**</font>

Dependencies: Add Your dependencies here
"""

import numpy as np
import pandas as pd
import re
import nltk
import spacy
import string
pd.options.mode.chained_assignment = None
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import RegexpTokenizer

from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
stop_words = set(stopwords.words('english'))

"""Load the data"""

df = pd.read_csv('/content/train.csv')

df.head()

"""Plot the count for each target"""

classes = df['target'].value_counts()
print(classes)
plt.pie([classes[0],classes[1]],labels=[0,1])
plt.legend(title = "classes")

"""Print the unique keywords"""

df['keyword'].value_counts()[:20]

"""Plot the count of each keyword"""

df_fake = df.loc[df['target']==0]
df_real = df.loc[df['target']==1]
plt.figure(figsize=(30,10))
plt.ylabel('Ketwords')
plt.title('keywords vs Count',fontweight='bold')
sns.barplot(y=df['keyword'].value_counts()[:20].index,x=df['keyword'].value_counts()[:20])
plt.show()

"""Is there any correlation of the length of a tweet with its target. Try to visualize"""

#Average tweet length
print(df['text'].str.len().mean())
#Average Word length of the tweet for seperate real and fake set
wlen_fake = df_fake['text'].str.split().apply(lambda x: len(x))
wlen_real = df_real['text'].str.split().apply(lambda x: len(x))
print("mean of fake class = ",{wlen_fake.mean()})
print("mean of real class = ",{wlen_real.mean()})

plt.figure(figsize=(15,5))
plt.subplot(121)
plt.title("Mean Word count of fake ",fontweight='bold')
sns.distplot(wlen_fake.map(lambda x: np.mean(x)))
plt.xlabel('count')
plt.subplot(122)
plt.title("Mean Word count of real",fontweight='bold')
sns.distplot(wlen_real.map(lambda x: np.mean(x)))
plt.xlabel('count')
plt.show()

"""Print the number of null values in each column"""

null_counts = df.isnull().sum()
null_counts[null_counts > 0].sort_values(ascending=False)

"""Remove the null values"""

# from the above result its clear that their is no nul value in text and target row so we don't need to remove this because if we remove this data we left with small traning 
# data set without any good so i think we not need to detele null data

"""Remove:


1.   Double Spaces
2.   Hypens and arrows
3.   Emojis
4.   URL
5.   Any other non english or special symbol

Replace wrong spellings with correct spellings


"""

df["txt_lower"] = df["text"].str.lower()

def remove_urls(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)

df["txt_urls"] = df["txt_lower"].apply(lambda text: remove_urls(text))

# remove punctuation
remove_punct = string.punctuation
def remove_punctuation(text):
    return text.translate(str.maketrans('', '', remove_punct))

df["txt_punct_urls"] = df["txt_urls"].apply(lambda text: remove_punctuation(text))

#remove double space
def remove_double_space(text):
    return re.sub("\s\s"," ",text)
df["txt_punct_urls_doubSpace"] = df["txt_punct_urls"].apply(lambda text: remove_double_space(text))
df["txt_punct_urls_doubSpace"]

# remove emojis
def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F" 
                           u"\U0001F300-\U0001F5FF" 
                           u"\U0001F680-\U0001F6FF"  
                           u"\U0001F1E0-\U0001F1FF"
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

df["txt_punct_urls_doubSpace_emojis"] = df["txt_punct_urls_doubSpace"].apply(lambda text: remove_emoji(text))

# remove nonenglish
def remove_non_english(text):
    return re.sub("[^a-zA-Z]"," ",text)
df["txt_punct_urls_doubSpace_emojis_nonEng"] = df["txt_punct_urls_doubSpace_emojis"].apply(lambda text: remove_non_english(text))

!pip install pyspellchecker

from spellchecker import SpellChecker
spell = SpellChecker()
def correct_spellings(text):
    corrected_text = []
    misspelled_words = spell.unknown(text.split())
    for word in text.split():
        if word in misspelled_words:
            corrected_text.append(spell.correction(word))
        else:
            corrected_text.append(word)
    return " ".join(corrected_text)
        
df["txt_punct_urls_doubSpace_emojis_nonEng_wronspell"] = df["txt_punct_urls_doubSpace_emojis_nonEng"].apply(lambda text: correct_spellings(text))

df=df.iloc[:,0:13]
df

"""Plot a word cloud of real target and fake target"""

from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
text = " ".join(review for review in df.txt_punct_urls_doubSpace_emojis_nonEng)
stopwords = set(STOPWORDS)
wordcloud = WordCloud(stopwords=stopwords, background_color="white",width=1000, height=600).generate(text)
plt.rcParams["figure.figsize"] = (10, 10)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

def txt_target_cloud(label):
  text = ''
  for word in df[df['target'] == label]['txt_punct_urls_doubSpace_emojis_nonEng']:
    word= word.lower()
    text += word + ' '
  wordcloud = WordCloud(stopwords=stopwords, background_color="white",width=1000, height=600).generate(text)
  plt.imshow(wordcloud)
  plt.axis('off')
  plt.show()

txt_target_cloud(0)

txt_target_cloud(1)

"""Keep only text and target column in the dataset"""

df['text']=df['txt_punct_urls_doubSpace_emojis_nonEng_wronspell']
df['text']

df = df[['text','target']]
df

"""Split data into train and validation"""

X = df['text']
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(X_train, y_train)

"""Print the count of unique words"""

target_0 = []
target_1 = []
for i in range(0,len(df)):
  if(df['target'].ravel()[i]==0):
    target_0.append(df['text'].ravel()[i])
  else:
    target_1.append(df['text'].ravel()[i])

class1_words = []
class0_words = []
for i in target_0:
  for j in i.split():
    class0_words.append(j)
for i in targ1:
  for j in i.split():
    class1_words.append(j)
print(class1_words, class0_words)

"""Compute the Term-Document Matrix (TDM) for all classes.

Use CountVectorizer of sklearn and print the dataframe with number of columns = number of unique words and the row showing the count of that word in a sentence.
"""

from sklearn.feature_extraction.text import CountVectorizer

vectorizer0 = CountVectorizer()
c0_vectorizer = vectorizer0.fit_transform(class0_words)
vectorizer1 = CountVectorizer()
c1_vectorizer = vectorizer1.fit_transform(class1_words)

print(vectorizer0.get_feature_names())
print(vectorizer1.get_feature_names())
print(c0_vectorizer.toarray())
print(c1_vectorizer.toarray())



"""Frequency of words in class 0 and 1"""

from collections import Counter
unique_class0 = Counter(class0_words)
print(unique_class0)

unique_class1 = Counter(class1_words)
print(unique_class1)

"""Does the sum of the unique words in target 0 and 1 sum upto the total number of unique words in the whole document? Why or why not? Explain in report.

Total frequency
"""







"""Calculate the probability for each word in a given class."""

targ0_train = []
targ1_train = []

for i in range(0,len(X_train)):
  if(y_train.ravel()[i]==0):
    targ0_train.append(X_train.ravel()[i])
  else:
    targ1_train.append(X_train.ravel()[i])


class0_words_train = []
for i in targ0_train:
  for j in i.split():
    class0_words_train.append(j)

class1_words_train = []
for i in targ1_train:
  for j in i.split():
    class1_words_train.append(j)

from collections import Counter

unique_class1_train = Counter(class1_words_train)
unique_class0_train = Counter(class0_words_train)

v1 = len(unique_class1_train)
v0 = len(unique_class0_train)

for i in unique_class0_train.keys():
    unique_class0_train[i] += 1
for i in unique_class1_train.keys():
    unique_class1_train[i] += 1


for i in unique_class1_train.keys():
  try:
    a = unique_class0_train[i]
  except KeyError as err:
    unique_class0_train[i] = 1

for i in unique_class0_train.keys():
  try:
    a = unique_class1_train[i]
  except KeyError as err:
    unique_class1_train[i] = 1

"""Class 0"""

likelihood_prob_0 =  {}
for i in unique_class0_train.keys():
  likelihood_prob_0[i] = (unique_class0_train[i])/( len(class0_words_train)+v0)

sum = 0
for i in likelihood_prob_0:
  sum+= likelihood_prob_0[i]
print(len(likelihood_prob_0))
print(sum)

"""Class 1"""

likelihood_prob_1 =  {}

for i in unique_class1_train.keys():
  likelihood_prob_1[i] = (unique_class1_train[i])/(len(class1_words_train) + v1) 

sum = 0
for i in likelihood_prob_1:
  sum+= likelihood_prob_1[i]
print(len(likelihood_prob_1))
print(sum)

"""We have calculated the probability of occurrence of word in a class, we can now substitute the values in the Baye's equation.

If a word from the new sentence does not occur in the class within the training set, the equation becomes zero. This problem can be solved using smoothing like Laplace smoothing.
"""







"""Probability for class 0"""

Prior_0 = len(targ0_train)/(len(targ1_train) + len(targ0_train)) 
Prior_0

"""Probability for class 1"""

Prior_1 = len(targ1_train)/(len(targ1_train) + len(targ0_train)) 
Prior_1



"""Print target class"""

y_test_pred = []
for i in X_test:
  prob1 = 1000*prior1
  prob0 = 1000*prior0
  for j in i:
    try:
      prob1 = prob1*likelihood_prob_1[j]
    except KeyError as err:
      prob1 = prob1*(1/( len(class1_words_train) + v1))
    try:
      prob0 = prob0*likelihood_prob_0[j]
    except KeyError as err:
      prob0 = prob0*(1/( len(class0_words_train) + v0))
    
  if(prob1>prob0):
    y_test_pred.append(1)
  else:
    y_test_pred.append(0)

print(len(y_test), len(y_test_pred))
print(y_test)
print(y_test_pred)

tp = 0
fp = 0
tn = 0
fn = 0

for i in range(0,len(y_test)):
  if(y_test.ravel()[i]==0 and y_test_pred[i]==0):
    tn = tn +1
  if(y_test.ravel()[i]==0 and y_test_pred[i]==1):
    fp = fp +1
  if(y_test.ravel()[i]==1 and y_test_pred[i]==0):
    fn = fn +1
  if(y_test.ravel()[i]==1 and y_test_pred[i]==1):
    tp = tp +1
  
print("tp=",tp," fp=",fp," tn=",tn," fn=",fn)
print("classwise accuracy=", (tp/(tp+fn) +tn/(tn+fp))/2 )
print("Total accuracy=",(tp+tn)/(tn+fp+tp+fn) )

precision =  tp/(tp+fp)
recall = tp/(tp+fn)
f1=2*precision*recall/(precision+recall)
print("Precision : ", precision)
print("Recall : ",recall)
print("f1-score :", f1)

"""References:

[Ref1](https://sebastianraschka.com/Articles/2014_naive_bayes_1.html)
"""