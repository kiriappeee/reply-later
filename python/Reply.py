import tweepy
import argparse
import sqlite3
import os
import configparser

dir = os.path.abspath(os.path.join((os.path.dirname(os.path.realpath(__file__))), '..'))
config = configparser.ConfigParser()
config.read(os.path.join(dir, 'python', 'config.ini'))
consumer_key = config['TOKEN']['consumerKey']
consumer_secret = config['TOKEN']['consumerSecret']
if 'devAccessToken' in config['TOKEN']:
    access_token = config['TOKEN']['devAccessToken']
    access_token_secret = config['TOKEN']['devAccessSecret']
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
if access_token:
    auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--id")
args = parser.parse_args()
if args.id:
    conn = sqlite3.connect(dir + '/replies.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT message, reply_id FROM replies WHERE ROWID = (?)", (args.id,))
    result = cur.fetchone()
    if result:
        message = result['message']
        replyId = result['reply_id']
#api.update_status(args.message, args.id)
messagesToSend = []
if len(message) > 140:
    print(message)
    tweet = api.get_status(replyId)
    username = tweet.user.screen_name
    messagesToSend.append(message[:140])
    message = "@%s %s"%(username, message[140:].lstrip())
    while message!="":
        print(message)
        if len(message) > 140:
            if message[139] != " ":
                cutOffIndex = message[0:140].rfind(" ") + 1
            else:
                cutOffIndex = 140
            messagesToSend.append(message[:cutOffIndex])
            
            message = "@%s %s"%(username, message[cutOffIndex:].lstrip())
        else:
            messagesToSend.append(message)
            break
else:
    messagesToSend.append(message)

if len(messagesToSend) == 1:
    api.update_status(messagesToSend[0], replyId)
else:
    for messageText in messagesToSend:
        print(messageText)
        print(replyId)
        replyId = (api.update_status(messageText, replyId)).id
#f = open('/replylater/myfile', 'r')
f = open( dir + '/myfile', 'r')
lines = f.readlines()
f.close()
#f = open('/replylater/myfile', 'w')
f = open(dir + '/myfile', 'w')
lines.append('hello %s %s %d \n'%(message, replyId, (len(lines) + 1)))
f.writelines(lines)
f.close()
