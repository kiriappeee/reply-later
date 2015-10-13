from datetime import datetime, timezone, timedelta
def saveReply(replyToSave, replyDataStrategy):
    validationResult = validateReply(replyToSave)
    if validationResult is not None:
        return {"result": "error", 
                "value": validationResult}

    saveResult = replyDataStrategy.saveReply(replyToSave)
    if saveResult is None:
        return {}
    return {"result": "success", 
            "value": saveResult}

def validateReply(replyToValidate):
    currentDateTime = datetime.now(tz=replyToValidate.timeZone)
    if currentDateTime >= replyToValidate.scheduledTime:
        return "Scheduled time cannot be earlier than current time"
