import nltk,math
import os
import nltk.corpus
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from collections import Counter
from math import log10,sqrt
from nltk.stem.porter import PorterStemmer


stemmer = PorterStemmer()
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


def weight(filename,token):
    idf=getidf(token)
    return (1+log10(tfs[filename][token]))*idf

def getidf(token):
    if df[token]==0:
        return -1
    return log10(len(tfs) / df[token])

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
        vector[filename][token] = vector[filename][token] / lengths[filename]
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
    tenth={}
    cos_sims=Counter()
    track={}
    q_tokens = word_tokenize(inputstring)
    
    for token in q_tokens:
        token = stemmer.stem(token)
        if token not in posting_list:
            continue
        if getidf(token)==0:
            loc_docs[token],weights = zip(*posting_list[token].most_common())
        else:
            loc_docs[token],weights = zip(*posting_list[token].most_common(10))
        tenth[token]=weights[9]
        if ct==1:
            track = set(loc_docs[token]) & track
        else:
            track = set(loc_docs[token])
            ct=1
        qtf[token] = 1+log10(inputstring.count(token))
        qlength+=qtf[token]**2
    qlength=sqrt(qlength)
    for doc in vector:
        cos_sim=0
        for token in qtf:
            if doc in loc_docs[token]:
                cos_sim = cos_sim + (qtf[token]/ qlength) * posting_list[token][doc]
            else:
                cos_sim = cos_sim + (qtf[token] / qlength) * tenth[token]
        cos_sims[doc] = cos_sim
    max = cos_sims.most_common(5)
    ans,wght = zip(*max)
    try:
        if ans[0] in track:
            return ans
        else:
            return "fetch more"
    except UnboundLocalError:
        return "none"
    
    
    