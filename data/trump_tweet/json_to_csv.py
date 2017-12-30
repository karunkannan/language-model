import json
import glob

files = glob.glob('*.json')
csv = open('trump_tweet_2016_2017.csv', 'w')
print("Loading data into csv...")
column_title = "id, text\n"
csv.write(column_title)
for x in files:
    cur = open(x, 'r')
    cur_file = json.load(cur)
    cur.close()
    for tweet in cur_file:
        id_str = tweet["id_str"]
        text = "\"" + tweet["text"] + "\""
        row = id_str + "," + text + "\n"
        csv.write(row)

csv.close()
print("CSV loaded.")
