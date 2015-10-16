import configparser
from datetime import datetime

from crontab import CronTab
def scheduleReply(replyId, dateAndTime):
    pythonPath, dataStrategyInitializer = getConfig()
    command = '/bin/sh /replylater/src/core/runmessage.sh --id=%s --data=%s'%(str(replyId), dataStrategyInitializer)
    timeToPost = datetime.fromtimestamp(dateAndTime.timestamp())
    cron = CronTab(user=True)
    job = cron.new(command=command, comment=str(replyId))
    job.minute.on(timeToPost.minute)
    job.hour.on(timeToPost.hour)
    job.day.on(timeToPost.day)
    job.month.on(timeToPost.month)
    cron.write()

def updateReply(replyId, dateAndTime):
    pythonPath, dataStrategyInitializer = getConfig()
    command = '/bin/sh /replylater/src/core/runmessage.sh --id=%s --data=%s'%(str(replyId), dataStrategyInitializer)
    timeToPost = datetime.fromtimestamp(dateAndTime.timestamp())
    cron = CronTab(user=True)
    job = cron.remove_all(comment=str(replyId))
    job = cron.new(command=command, comment=str(replyId))
    job.minute.on(timeToPost.minute)
    job.hour.on(timeToPost.hour)
    job.day.on(timeToPost.day)
    job.month.on(timeToPost.month)
    cron.write()

def removeReply(replyId):
    pythonPath, dataStrategyInitializer = getConfig()
    cron = CronTab(user=True)
    cron.remove_all(comment=str(replyId))
    cron.write()

def getConfig():
    config = configparser.ConfigParser()
    config.read('src/config.ini')
    pythonPath = config['CONFIG']['pythonPath']
    dataStrategyInitializer = config['CONFIG']['dataStrategyInitializer']
    return pythonPath, dataStrategyInitializer
