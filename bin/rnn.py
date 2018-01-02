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
        tweet = "%s" % tweet
        tweet = tweet[2:len(tweet) - 1]
        tweets.append("%s %s %s" % (start, tweet, stop))

    print("processed %d tweets" % len(tweets))

#tokenize
token_tweet = [nltk.word_tokenize(tweet) for tweet in tweets]
frequency = nltk.FreqDist(itertools.chain(*token_tweet))
print("Unique Words: %d" % (frequency.B()))

#Only want to consider words said often
vocab = frequency.most_common(10000)
print("Vocab Size: %d" % len(vocab))

#need to build word to index and index to word list and dictionary
ix_to_word = [x[0] for x in vocab]
unknown = "UNKNOWN_TOKEN"
ix_to_word.append(unknown) #for the words we removed
word_to_ix = {w:i for i,w in enumerate(ix_to_word)}

#inject unknown token into the token tweets
for i, tweet in enumerate(token_tweet):
    token_tweet[i] = [word if word in word_to_ix else unknown for word in tweet]

print("\nEXAMPLE:\n%s \n %s \n" % (tweets[1], token_tweet[1]))

#re-express data as indices instead of words
x_train = np.array([[word_to_ix[w] for w in tweet[:-1]] for tweet in token_tweet])
y_train = np.array([[word_to_ix[w] for w in tweet[1:]] for tweet in token_tweet])

print(x_train[0])
print(y_train[0])
