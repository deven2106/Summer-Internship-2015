import logging
import gensim
from gensim import corpora, models, similarities
from collections import defaultdict
import time,os
import shutil
from os import listdir
from os.path import isfile,join
import cPickle
import sys

########################### GLOBAL VARIABLE ########################
text=[]
files=[]
texts=[]
printList = []
LOG_FILENAME=""
no_top=1    #just an int var
pas=1       #1 doesn't mean anything
########################### GLOBAL VARIABLE ########################

def doc_read():
        #Reading document using cPickle library
        for file in listdir('.'):
            if isfile(file) and file.endswith('.pkl'):
                fp=open(file,'r')
                try:
                    b=cPickle.load(fp)
                except Exception:
                    #print "problem in file : "+ file
                    continue
                #print b
                temp=b['content']+b['subtitle']+b['title']
                text.append(temp)
                files.append(file)

def stopword_removal():
    #Stopword reading from universal file
    f=open('stopWords','r')
    stoplist=f.read()
    stoplist=set(stoplist.split())
    texts = [[word for word in t.lower().split() if word not in stoplist]
             for t in text]

def remove():
    if os.path.exists('my_dict.dict'):
        os.remove('my_dict.dict')
    if os.path.exists('my_corpus.mm'):
        os.remove('my_corpus.mm')
    if os.path.exists('my_corpus.mm.index'):
        os.remove('my_corpus.mm.index')

def get_topic_fromlog():
    theFile = open(LOG_FILENAME,'r')
    FILE = theFile.readlines()
    theFile.close()
    for line in FILE:
        if('topic #' in line):
            printList.append(line)
        if('optimized alpha' in line):
            printList.append(line)

def write_result():
    f1=open('Topics_'+str(no_top)+'_'+str(pas)+'/Topics_'+str(no_top)+'_pass_'+str(pas)+'.res','w')
    for item in printList:
        f1.write(str(item)+'\n')
    f1.close()


def main():

    time1=time.time()
    #input parameter read.. value of number of topics and number of passes
    no_top=int(sys.argv[1])
    pas=int(sys.argv[2])

    os.chdir('Log_text files')
    if not os.path.exists('Topics_'+str(no_top)+'_'+str(pas)):
        os.mkdir('Topics_'+str(no_top)+'_'+str(pas)) #directory creation for every Topic
    else:
        shutil.rmtree('/Topics_'+str(no_top)+'_'+str(pas))
        os.mkdir('Topics_'+str(no_top)+'_'+str(pas)) #directory creation for every Topic

    #Logging generation
    tm=time.strftime('%Y%m%d-%H%M%S')
    LOG_FILENAME="Topics_"+str(no_top)+"_"+str(pas)+"/log_file"+tm+"_topics_"+str(no_top)+"_pass_"+str(pas)+".log"
    logging.basicConfig(filename=LOG_FILENAME,format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    os.chdir('./..')

    #Reading document using cPickle library
    doc_read()

    ##Stop Word Removal
    stopword_removal()


    ##Dictionary Creation based on word IDs
    dictionary = corpora.Dictionary(texts)
    dictionary.save('my_dict.dict')
    dictionary.compactify()


    ##Corpus creation with word IDs and their count
    corpus = [dictionary.doc2bow(text1) for text1 in texts]
    corpora.MmCorpus.serialize('my_corpus.mm', corpus)


    ##Loading corpus in MM format
    corpus = corpora.MmCorpus('my_corpus.mm')


    ##Explicit generation of ID to word dictionary
    id2word = {}
    for word in dictionary.token2id:
        id2word[dictionary.token2id[word]] = word


    ##LDA module call
    lda = gensim.models.ldamodel.LdaModel(corpus=corpus, alpha='auto', id2word=id2word, num_topics=no_top, update_every=1, chunksize=10000, passes=pas)

    time2=time.time()

    os.chdir('Log_text files')


    ##Writing total elapsed time into log file
    theFile = open(LOG_FILENAME,'a')
    theFile.write('\n\n')
    theFile.write('Total Time Elapsed in the Process of trainning is : '+str(time2-time1)+' secs'+'\n')
    theFile.close()


    ##Getting Topic lists from log file
    get_topic_fromlog()



    ##Writing topics to result file
    write_result()
    os.chdir('./..')
    ##Calculating Topic to doc distribution
    f2=open('Log_text files/Topics_'+str(no_top)+'_'+str(pas)+'/Topics_'+str(no_top)+'_pass_'+str(pas)+'.res','a')
    f2.write('\n\n\n<<<<<<<<<<<<<<=========================Topic to document distribution=========================>>>>>>>>>>>>>>')
    time3=time.time()

    for i in range(len(corpus)):
        #print lda[corpus[i]]
        #print '\n\ndone\n'
        f2.write(files[i]+' == '+str(lda[corpus[i]])+'\n\n')

    time4=time.time()

    ##Writing total elapsed time in this module into log file
    f2.write('\n\n'+'Total Time Elapsed in the Process of Topic to Doc is : '+str(time4-time3)+' secs'+'\n')
    f2.close()

    ##Removing saved dictionary and MM index
    remove()


if __name__ == '__main__':
    main()


