from datetime import timezone, timedelta

class User:
    def __init__(self, username, authToken, secretToken, timeZone, userId = None):
        self.username = username
        self.authToken = authToken
        self.secretToken = secretToken
        self.timeZone = timeZone
        self.userId = userId
