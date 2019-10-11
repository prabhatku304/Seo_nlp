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
vector={}
posting_list = {}
st_tokens = []
lengths=Counter()
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



for filename in tfs:
    vector[filename]=Counter()
    length=0
    for token in tfs[filename]:
        wt = weight(filename,token)
        vector[filename][token]=wt
        length+=wt**2
        lengths[filename]=math.sqrt(length)
        
for filename in vector:
    for token in vector[filename]:
        vector[filename][token] = vector[filename][token] / lenghts[filename]
        if token not in posting_list:
            posting_list[token]=Counter()
        posting_list[token][filename]=vector[filename][token]
        
def getWeight(filename,token):
    return vector[filename][token]


def query(inputstring):
    inputstring = inputstring.lower()
    qtf={}
    qlength=0
    ct=0
    loc_docs={}
    cos_sims=Counter()
    q_tokens = word_tokenize(inputstring)
    
    for token in q_tokens:
        token = stemmer.stem(token)
        if token not in posting_list:
            continue
        if getidf(token)==0:
            loc_docs[token],weight = zip(*posting_list[token].most_common())
        else:
            loc_docs[token],weight = zip(*posting_list[token].most_common(5))
        
        if ct==1:
            track = set(loc_docs[token]) & track
        else:
            track = set(loc_docs[token])
            ct=1
        qtf[token] = 1+log10(inputstring.count(token))
        qlength+=qtf[token]**2
    qlength=sqrt(qlength)
    for doc in vector:
        