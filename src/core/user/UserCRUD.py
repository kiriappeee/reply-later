def saveUser(userToSave, userDataStrategy):
    validationResult = validateUser(userToSave)
    if validationResult != {}:
        return {"result": "error", "value": validationResult}
    saveResult = userDataStrategy.saveUser(userToSave)
    if saveResult:
        return {"result": "success", "value": saveResult}

def updateUser(userToUpdate, userDataStrategy):
    validationResult = validateUser(userToUpdate)
    if validationResult != {}:
        return {"result": "error", "value": validationResult}
    if userDataStrategy.updateUser(userToUpdate):
        return {"result": "success"}

def validateUser(userToValidate):
    errorList = {}
    if userToValidate.username == '' or userToValidate.username is None:
        errorList['usernameError'] = "Username cannot be empty"
    if userToValidate.authToken == '' or userToValidate.authToken is None:
        errorList['tokenError'] = "Token cannot be empty"
    if userToValidate.secretToken == '' or userToValidate.secretToken is None:
        errorList['secretError'] = "Secret cannot be empty"
    return errorList

def getUserById(userId, userDataStrategy):
    return userDataStrategy.getUserById(userId)

def getUserByUsername(username, userDataStrategy):
    return userDataStrategy.getUserByUsername(username)
