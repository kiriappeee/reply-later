from ...data.sqlite import ReplyDataStrategy as SqliteReply, UserDataStrategy as SqliteUser
ReplyDataStrategy = None
UserDataStrategy = None

def initializeDataStrategy(dataStrategyType):
    global ReplyDataStrategy
    global UserDataStrategy
    if dataStrategyType == "sqllite":
        ReplyDataStrategy = SqliteReply
        UserDataStrategy = SqliteUser
