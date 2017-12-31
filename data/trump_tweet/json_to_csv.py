import json
import glob
import re

files = glob.glob('*.json')
csv = open('trump_tweet_2016_2017.csv', 'w')
print("Loading data into csv...")
column_title = "id, text\n"
csv.write(column_title)
i = 0
for x in files:
    cur = open(x, 'r')
    cur_file = json.load(cur)
    cur.close()
    for tweet in cur_file:
        id_str = tweet["id_str"].encode('utf-8')
        text = tweet["text"]
        matchObj = re.match('^RT|^"@', text)
        if matchObj != None:
            continue
        text = "\"" + tweet["text"].encode('ascii', 'ignore') + "\""
        row = id_str + "," + text + "\n"
        i += 1
        csv.write(row)

csv.close()
print("CSV loaded. %d" % i)
