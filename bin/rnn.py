import numpy as np
import nltk
import sys
import csv
import itertools
#collect arg
file_location = sys.argv[1]

#import data and remove retweets
start = "START_TWEET"
stop = "STOP_TWEET"
with open(file_location, 'r') as f:
    reader = csv.reader(f, skipinitialspace=True)
    reader.__next__() #skip the header
    tweets = []
    for x in reader:
        tweet = x[0].encode('ascii', 'ignore').lower()
        tweets.append("%s %s %s" % (start, tweet, stop))

    print("processed %d tweets" % len(tweets))

#tokenize
token_tweet = [nltk.word_tokenize(tweet) for tweet in tweets]
frequency = nltk.FreqDist(itertools.chain(*token_tweet))
print("Unique Words: %d" % len(frequency.items()))

