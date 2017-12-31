import json
import glob
import re

files = glob.glob('*.json')
csv = open('trump_tweet_2016_2017.csv', 'w')
print("Loading data into csv...")
column_title = "text\n"
csv.write(column_title)
i = 0
for x in files:
    cur = open(x, 'r')
    cur_file = json.load(cur)
    cur.close()
    for tweet in cur_file:
        text = tweet["text"]
        matchObj = re.match('^RT|^"@', text)
        if matchObj != None:
            continue
        text = "\"" + tweet["text"] + "\""
        row = text + "\n"
        i += 1
        csv.write(row)

csv.close()
print("CSV loaded. %d" % i)
