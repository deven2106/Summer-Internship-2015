__author__ = 'mayankgupta'
import json
import tweepy
from tweepy import Stream, OAuthHandler
from time import clock
import time,sys
import settings
import datetime


def main():
    auth = OAuthHandler(settings.consumer_key, settings.consumer_secret)
    auth.set_access_token(settings.access_token, settings.access_token_secret)

    #twitterStream=Stream(auth,listener(),timeout=120)
    api=tweepy.API(auth)

    users = ['TimesNow', 'timesofindia', 'TheHindu', 'ibnlive', 'BDUTT', 'BBCBreaking','abpnewstv', 'htTweets',
             'narendramodi','PMOIndia', 'BarackObama', 'BJP4India', 'INCIndia', 'smritiirani', 'SushmaSwaraj', 'ShashiTharoor']
    ids=[ '240649814','134758540','177829660','6509832','19929890','5402612','39240673','36327407','18839785','471741741','813286',
          '207809313','1153045459','130104041','219617448','24705126']

    str1=''
    i=0
    j=0
    datetofind = datetime.datetime.now() - datetime.timedelta(days=12)
    for j in range(5,10):
        id=ids[j]
        counter=200
        log = open("rest.txt", "a")
        tweets=api.user_timeline(id,count=200)
        for tweet in tweets:
            log.write(str(tweet))
            log.write("\n\n")
            i=i+1
        last=tweets.max_id
        while(counter<3200):
            tweets = api.user_timeline(user_id=id, count=200, max_id=last)
            counter+=200
            last = tweets.max_id
            if(tweets[0].created_at<datetofind):
                break
            for tweet in tweets:
                log.write(str(tweet))
                log.write("\n\n")
                i=i+1
        print "term ",j
        print i
        log.write('\n\n\n\n')
        log.close()
    return True


if __name__ == "__main__":
    main()
