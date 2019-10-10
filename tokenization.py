import nltk
import os
import nltk.corpus
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

corp='./data'
filename = os.listdir(corp)

file = open(os.path.join(corp, filename[0]), "r", encoding='UTF-8')

info = file.read()
file.close()
info = info.lower()
sw=set(stopwords.words('english'))
data_token = word_tokenize(info)
data_tokens = [token for token in data_token if token not in sw]

fdist = FreqDist()
for i in data_tokens:
    fdist[i]+=1

fdist