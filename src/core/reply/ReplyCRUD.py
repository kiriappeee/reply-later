from datetime import datetime, timezone, timedelta
from ..scheduler import Scheduler

def saveReply(replyToSave, replyDataStrategy):
    validationResult = validateReply(replyToSave)
    if validationResult is not None:
        return {"result": "error", 
                "value": validationResult}

    saveResult = replyDataStrategy.saveReply(replyToSave)
    if saveResult is None:
        return {}
    Scheduler.scheduleReply(saveResult, replyToSave.scheduledTime)
    return {"result": "success", "value": saveResult}

def getReplyByReplyId(replyId, replyDataStrategy):
    return replyDataStrategy.getReplyByReplyId(replyId)

def updateReply(replyToUpdate, replyDataStrategy):
    if replyIsPostedAlready(replyToUpdate.replyId, replyDataStrategy):
        return {"result": "error", "value": "Reply has already been sent"}
    
    validationResult = validateReply(replyToUpdate)
    if validationResult is not None:
        return {"result": "error", "value": validationResult}
    
    updateResult = replyDataStrategy.updateReply(replyToUpdate)

    if updateResult:
        if replyToUpdate.sentStatus == "sent":
            Scheduler.removeReply(replyToUpdate.replyId)
        else:
            Scheduler.updateReply(replyToUpdate.replyId, replyToUpdate.scheduledTime)
        return {"result": "success"}

def cancelReply(replyToCancel, replyDataStrategy):
    if replyIsPostedAlready(replyToCancel.replyId, replyDataStrategy):
        return {"result": "error", "value": "Reply has already been sent"}

    validationResult = validateReply(replyToCancel)
    if validationResult is not None:
        return {"result": "error", "value": validationResult}

    replyToCancel.sentStatus = "cancelled"
    cancelResult = replyDataStrategy.cancelReply(replyToCancel)
    if cancelResult:
        Scheduler.removeReply(replyToCancel.replyId)
        return {"result": "success"}

def getRepliesByUserId(userId, replyDataStrategy):
    replies = replyDataStrategy.getRepliesByUserId(userId)
    return replies

def getRepliesByUserIdAndStatus(userId, status, replyDataStrategy):
    replies = replyDataStrategy.getRepliesByUserIdAndStatus(userId, status, replyDataStrategy)
    return replies

def validateReply(replyToValidate):
    currentDateTime = datetime.now(tz=replyToValidate.timeZone)
    if currentDateTime > replyToValidate.scheduledTime:
        return "Scheduled time cannot be earlier than current time"

def replyIsPostedAlready(replyId, replyDataStrategy):
    replyStatus = replyDataStrategy.getReplyByReplyId(replyId).sentStatus
    if replyStatus == "sent":
        return True
    else:
        return False
