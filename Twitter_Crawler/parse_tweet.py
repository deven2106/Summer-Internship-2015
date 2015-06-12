#!/usr/bin/python
import json
fp=open("a.txt",'r')        # a.txt contain all tweets in json format as crawled from twitter
data=fp.read()
fp.close()
tweet_count=0
for temp in data.split('\n'):
    try:
        tweet = json.loads(temp)
        #print tweet['text']
        try:
            tweet_count+=1
            fname="temp/" + str(tweet_count) + ".txt"
            fp=open(fname,'w+')   # w+ overwrite the existing file and open for both reading and writing
            fp.write(unicode(tweet['text']).encode('ascii','ignore'))
            fp.close()
        except Exception:
            print "failed to write tweet text in file"
            print "tweet is :" + temp
    except Exception:
        print("Failed to parse tweet data")
        print "tweet is :" + temp
        tweet = None
