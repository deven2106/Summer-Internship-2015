from gensim import corpora, models, similarities
from collections import defaultdict
from pprint import pprint
import logging
import sys

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

corpus=[]
f=open("1.txt","r")
data=f.read()
corpus.append(str(data))
f.close()
f=open("2.txt","r")
data=f.read()
corpus.append(str(data))
f.close()
stoplist=set('from by had have as it his has been on with he she * this that for a of the and to in is was at are be \\theta \\alpha \\beta / >'.split())

'''
texts=[[word for word in doc.lower().split() if word not in stoplist]
       for doc in corpus]
print texts

print "<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>"
'''

texts=[]
temp=[]
for doc in corpus:
    for word in doc.lower().split():
        if word not in stoplist and word.isalnum():
            temp.append(word)
    texts.append(temp)
    temp=[]
#print texts

frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token]+=1

#print frequency

#print "<<<<<<<<<<>>>>>>>>>>>"

dictionary=corpora.Dictionary(texts)
dictionary.save('dict.dict')

corpus = [dictionary.doc2bow(text) for text in texts]    # now corpus is list of lists contains tuples (word_id,count in the document)
#There exist several file formats for serializing a Vector Space corpus (~sequence of vectors) to disk
corpora.MmCorpus.serialize('dict.mm',corpus)             # store to disk in the Matrix Market format:, for later use

dictionary=corpora.Dictionary.load('dict.dict')
corpus=corpora.MmCorpus('dict.mm')
print(list(corpus))

tfidf=models.TfidfModel(corpus,normalize=True)
corpus_tfidf=tfidf[corpus]

'''for i in corpus_tfidf:
    print i
print(corpus_tfidf)
'''

lda = models.ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=3)
corpus_lda = lda[corpus]

print "dsfds"
f=open("a.txt",'w')
sys.stdout=f
print lda.print_topics(3)
f.close()
#lda.output=open('lda_out','w')
#lda.output.write(str(lda.print_topics(3)))
#lda.print_topics(3)
#lsi.print_topics(5)

