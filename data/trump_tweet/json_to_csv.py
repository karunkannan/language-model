import json
import glob

files = glob.glob('*.json')
csv = open('trump_tweet_2016_2017.csv', 'w')
i = 0
for x in files:
    cur = open(x, 'r')
    cur_file = json.load(cur)
    cur.close()
    for tweet in cur_file:
        print(tweet['id_str'], i)
        i += 1
