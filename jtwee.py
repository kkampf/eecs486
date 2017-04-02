import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
 
NFL_TEAMS = [] 


class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key='Dh4kxOtgNgiDCx54EAUV3HsQ9'
        consumer_secret='D1BT4k5k63aNcN2llizJfTVo0dFLNo8x6DNcMBEfZQqY7iEhDR'
        access_token='286507548-C8UhCxN7IQnTe9k1DKUHNpnDCHLKrIWIox6PIbvo'
        access_token_secret='PgrTVjLDEDcERCAJiyhfChWucabRxGOqbfOfWBVYk883g'
 
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")
 
    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])\
                                    |(\w+:\/\/\S+)", " ", tweet).split())
 
    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
 
    def get_tweets(self, query, count = 10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []
 
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q = query, count = count)
 
            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
 
                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
 
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
 
            # return parsed tweets
            return tweets
 
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))
 
def main():
    # creating object of TwitterClient Class
    api = TwitterClient()

    NFL_TEAMS.append('giants')
    NFL_TEAMS.append('dallascowboys')
    NFL_TEAMS.append('redskins')
    NFL_TEAMS.append('eagles')

    NFL_TEAMS.append('nyjets')
    NFL_TEAMS.append('patriots')
    NFL_TEAMS.append('buffalobills')
    NFL_TEAMS.append('miamidolphins')

    NFL_TEAMS.append('packers')
    NFL_TEAMS.append('vikings')
    NFL_TEAMS.append('lions')
    NFL_TEAMS.append('chicagobears')

    NFL_TEAMS.append('azcardinals')
    NFL_TEAMS.append('seahawks')
    NFL_TEAMS.append('ramsnfl')
    NFL_TEAMS.append('49ers')

    NFL_TEAMS.append('saints')
    NFL_TEAMS.append('tbbuccaneers')
    NFL_TEAMS.append('atlantafalcons')
    NFL_TEAMS.append('panthers')

    NFL_TEAMS.append('steelers')
    NFL_TEAMS.append('bengals')
    NFL_TEAMS.append('browns')
    NFL_TEAMS.append('ravens')

    NFL_TEAMS.append('raiders')
    NFL_TEAMS.append('broncos')
    NFL_TEAMS.append('chiefs')
    NFL_TEAMS.append('chargers')

    NFL_TEAMS.append('titans')
    NFL_TEAMS.append('colts')
    NFL_TEAMS.append('houstontexans')
    NFL_TEAMS.append('jaguars')

    # calling function to get tweets
    tweets = api.get_tweets(query = 'Donald Trump', count = 200)
 
    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    # percentage of neutral tweets
    print("Neutral tweets percentage: {} % ".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))
 
    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])
 
    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])
 
if __name__ == "__main__":
    # calling main function
    main()