import tweepy
from crontab import CronTab
from datetime import datetime, timedelta, timezone
import sqlite3
import configparser
import os

conn = sqlite3.connect('../replies.db')
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS replies(message TEXT, reply_id TEXT)")
conn.commit()
conn.close()
config = configparser.ConfigParser()
config.read('config.ini')
PYTHON_PATH = config['PYTHON_PATH']['PATH']
consumer_key = config['TOKEN']['consumerKey']
consumer_secret = config['TOKEN']['consumerSecret']
if 'devAccessToken' in config['TOKEN']:
    access_token = config['TOKEN']['devAccessToken']
    access_token_secret = config['TOKEN']['devAccessSecret']
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
if access_token:
    auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

mentions = api.mentions_timeline(count=10)
counter = 1
for mention in mentions:
    print(str(counter) + ': ' + str(str.encode(mention.text, 'utf-8')))
    #print(dir(mention))
    #print(dir(mention.user))
    print(mention.user.screen_name)
    #print(mention.user.name)
    print(mention.user.id)
    print(mention.id)
    counter += 1

tweetIdToReplyto = input('Which tweet to reply to: ')

while True:
    replyText = input('Reply text (max characters: 140): ')
    conn = sqlite3.connect('../replies.db')
    conn.row_factory = sqlite3.Row
    cur= conn.cursor()
    cur.execute("INSERT INTO replies (message, reply_id) VALUES (?,?)",(replyText, mentions[int(tweetIdToReplyto)].id))
    replyId = cur.lastrowid
    conn.commit()
    conn.close()
    break


d = datetime.now(tz=timezone(timedelta(hours=5, minutes=30)))

print('the time right now is %d:%d'%( d.hour, d.minute))

minutesToReplyIn = int(input('How many minutes to send reply in? '))

tab = CronTab()
command = '%s %s/Reply.py --id=%d'%(PYTHON_PATH, os.getcwd(), replyId)
job = tab.new(command=command, comment=str(replyId))
newD = datetime.now()
print(newD)
job.minute.on((newD + timedelta(minutes=minutesToReplyIn)).minute)
job.hour.on((newD + timedelta(minutes=minutesToReplyIn)).hour)
print(tab.render())
tab.write()
