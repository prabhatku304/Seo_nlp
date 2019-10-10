import nltk
import os
import nltk.corpus
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from collections import Counter

corp='./data'
root = os.listdir(corp)
df=Counter()
tfs={}

for filename in root:
    
    file = open(os.path.join(corp, filename), "r", encoding='UTF-8')
    
    info = file.read()
    file.close()
    info = info.lower()
    sw=set(stopwords.words('english'))
    data_token = word_tokenize(info)
    data_tokens = [token for token in data_token if token not in sw]
    
    tf=Counter(data_tokens)
    df+=Counter(list(set(data_tokens)))
    tfs[filename]=tf.copy()
    tf.clear()

df
tfs