__author__ = 'mayankgupta'
import json
import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream, OAuthHandler
from time import clock
import time,sys,datetime
import settings

class listener(StreamListener):
    def __init__(self):
        self.tweet_count = 0

    def on_data(self, data):
        try:
            tweet = json.loads(data)
            print tweet['text']
        except Exception:
            print("Failed to parse tweet data")
            tweet = None

        if tweet.has_key('id') and tweet.has_key("text"):
            fp=open("tweets.txt",'a')
            fp.write(data)
            fp.close()
            self.tweet_count+=1
            #print tweet['text'][0:10].encode('ascii','ignore')
            #print self.tweet_count
        return True

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        time.sleep(10)
        return True

    def on_error(self, status_code):
        print 'Error: ' + repr(status_code)
        time.sleep(5)
        return True
    def on_limit(self, track):
        """Called when a limitation notice arrvies"""
        print "!!! Limitation notice received: %s" % str(track)
        return


def main():
    auth = OAuthHandler(settings.consumer_key, settings.consumer_secret)
    auth.set_access_token(settings.access_token, settings.access_token_secret)
 
    while True:
        try:
            twitterStream=Stream(auth,listener(),timeout=120)
            print "trying"
            fp=open("log.txt",'a')
            t1=datetime.datetime.now()
            t1=str(t1)
            fp.write(t1)
            fp.write("\n")
            fp.close()
            twitterStream.filter(follow=[ '240649814','134758540','177829660','6509832','19929890','5402612','39240673','36327407','18839785','471741741','813286','207809313','1153045459','130104041','219617448','24705126'])
        except KeyboardInterrupt:
            print "keyboard interrupt"
            sys.exit(0)
        except:
            print "exception"
            fp=open("log.txt",'a')
            t1=datetime.datetime.now()
            t1=str(t1)
            fp.write(t1)
            fp.write("\n")
            fp.close()
            time.sleep(10)

if __name__ == "__main__":
    main()
