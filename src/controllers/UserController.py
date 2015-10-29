import tweepy
from datetime import timezone, timedelta, datetime
from ..core.messager import TweetAdapter
from ..core.data import DataConfig
from ..core.user.User import User
from ..core.user import UserCRUD

def createUser(accessToken, accessTokenSecret, timeZoneHours=0, timeZoneMinutes=0):
    api = TweetAdapter.createAPIObject()
    auth = api.auth
    auth.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(auth)
    userDetails = api.me()
    return UserCRUD.saveUser(User(userDetails.screen_name, accessToken, accessTokenSecret, timeZone=timezone(timedelta(hours=int(timeZoneHours), minutes=int(timeZoneMinutes)))), DataConfig.UserDataStrategy)

def setTimeZone(timezoneForm, userId):
    user = UserCRUD.getUserById(userId, DataConfig.UserDataStrategy)
    timeZone = timezone(timedelta(hours=int(timezoneForm['tzhour']), minutes=int(timezoneForm['tzminute'])))
    user.timeZone = timeZone
    return UserCRUD.updateUser(user, DataConfig.UserDataStrategy)

def getUserTimeZone(userId):
    user = UserCRUD.getUserById(userId, DataConfig.UserDataStrategy)
    tzInfo = str(user.timeZone)
    if tzInfo.find('-') == -1:
        hours, minutes = tzInfo.split('+')[1].split(':')
        return {"hours": int(hours), "minutes": int(minutes)}
    else:
        hours, minutes = tzInfo.split('-')[1].split(':')
        return {"hours": int(hours)*-1, "minutes": int(minutes)*-1}
