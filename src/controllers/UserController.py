import tweepy
from datetime import timezone, timedelta
from ..core.messager import TweetAdapter
from ..core.data import DataConfig
from ..core.user.User import User
from ..core.user import UserCRUD

def createUser(accessToken, accessTokenSecret):
    api = TweetAdapter.createAPIObject()
    auth = api.auth
    auth.set_access_token(accessToken, accessTokenSecret)
    userDetails = api.me()
    return UserCRUD.saveUser(User(userDetails.username, accessToken, accessTokenSecret, timeZone=timezone(timedelta(hours=0))), DataConfig.UserDataStrategy)

def setTimeZone(timezoneForm, userId):
    user = UserCRUD.getUserById(userId, DataConfig.UserDataStrategy)
    timeZone = timezone(timedelta(hours=timezoneForm['tzhour'], minutes=timezoneForm['tzminute']))
    user.timeZone = timeZone
    return UserCRUD.updateUser(user, DataConfig.UserDataStrategy)
