import pandas as pd
import numpy  as np
import matplotlib
from matplotlib import pylab as plt
import re
import nltk
import sklearn
import sklearn.feature_extraction.text as sk



def wm2df(wm, feat_names):
    
    # create an index for each row
    doc_names = ['Doc{:d}'.format(idx) for idx, _ in enumerate(wm)]
    df = pd.DataFrame(data=wm.toarray(), index=doc_names,
                      columns=feat_names)
    return(df)




list01 = [ ['earthquake', 'panic', 'disco'], ['panic', 'shopping', 'nuts'], ['politics', 'nuts', 'zebras'] ]




uplist=list(map(' '.join, list01))




# instantiate the vectorizer object
cvec = sk.CountVectorizer(lowercase=False)

# convert the documents into a document-term matrix
wm = cvec.fit_transform(uplist)

# retrieve the terms found in the corpora
tokens = cvec.get_feature_names()

# create a dataframe from the matrix
table=wm2df(wm, tokens)
table




word_freq=table.sum(axis = 0, skipna = True)
type(word_freq)

f_word = pd.DataFrame([word_freq])
f_word=f_word.transpose()
f_word = f_word.sort_values(0,ascending=False)



#word_freq.value_counts()[:20].plot(kind='bar')
f_word[0][:20].plot.bar()
plt.xlabel('Keywords')
plt.ylabel('Count')
plt.title('Most Frequently occuring Keywords')
plt.tight_layout()


