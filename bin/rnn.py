import numpy as np
import nltk
import sys
import csv
import itertools
#collect arg
file_location = sys.argv[1]
''' Data Prep '''
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
vocab_size = 10000
vocab = frequency.most_common(vocab_size - 1)


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

print(x_train[1])
print(y_train[1])

''' RNN Class '''
class RNN:
    def __init__(self, vocab, hidden_dim = 100, truncate_factor = 4):
        self.vocab_dim = vocab
        self.hidden_dim = hidden_dim
        self.truncate = truncate_factor
        #intialize randomly using tanh optimal values from paper
        #Understanding the difficulty of training deep feedforward neural
        #networks by Glorot and Bengio
        #U matrix from input to hidden
        #V matrix from hidden to output
        #W matrix from hidden to hidden
        self.U = np.random.uniform(-1*np.sqrt(1./self.vocab_dim),
                np.sqrt(1./self.vocab_dim), (hidden_dim, self.vocab_dim))
        self.V = np.random.uniform(-1*np.sqrt(1./hidden_dim),
                np.sqrt(1./hidden_dim), (self.vocab_dim, hidden_dim))
        self.W = np.random.uniform(-1*np.sqrt(1./hidden_dim),
                np.sqrt(1./hidden_dim), (hidden_dim, hidden_dim))

    def forward(self, x):
        t_steps = len(x)

        #encode input as one-hot vector
        one_hot_x = []
        for num in x:
            vec = np.zeros(self.vocab_dim)
            vec[x] = 1
            one_hot_x.append(vec)
        one_hot_x = np.asarray(one_hot_x)

        #init hidden and output states
        h = np.zeros((t_steps + 1, self.hidden_dim))
        o = np.zeros((t_steps, self.vocab_dim))
        for t in np.arange(t_steps):
            h[t] = np.tanh(self.U.dot(one_hot_x[t]) + self.W.dot(h[t-1]))
            o[t] = self.softmax(self.V.dot(h[t]))
        return o, h

    def softmax(self, x):
        arr = np.exp(x)
        sum_arr = np.sum(arr)
        return arr/sum_arr

rnn = RNN(vocab_size)
o, h = rnn.forward(x_train[1])
print(o.shape)
