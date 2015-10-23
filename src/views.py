from flask import session,url_for,request,redirect,render_template
from datetime import timedelta, datetime, timezone
from . import application
from .controllers import LoginController, UserController, ReplyController

BASEPATH = "/replylater/app"

@application.route(BASEPATH+"/clearAll", methods=['GET'])
def clearAll():
    session.pop('userid')

@application.route(BASEPATH, methods=['GET'])
def index():
    if 'userid' in session:
        mentions = ReplyController.getMentions(session['userid'])
        return render_template('replyscheduler.html', mentions=mentions)
    else:
        return redirect(url_for('login'))

@application.route(BASEPATH + '/login', methods=['GET', 'POST'])
def login():
    if 'userid' in session:
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        return redirect(LoginController.getStartingUrl())

@application.route(BASEPATH + '/completelogin', methods=['GET'])
def completelogin():
    if 'denied' in request.args:
        return "DENIEEED"
    else:
        accessToken, accessTokenSecret = LoginController.getAuth(request.args.get('oauth_verifier'), request.args.get('oauth_token'))
        result = UserController.createUser(accessToken, accessTokenSecret)
        print(result)
        session['userid'] = result['value']
        print(session['userid'])
        if(result['updated']):
            return redirect(url_for('index'))
        else:
            return redirect(url_for('addtimezone'))

@application.route(BASEPATH + '/addtimezone', methods=['GET', 'POST'])
def addtimezone():
    if 'userid' not in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('updatetimezone.html')
    else:
        UserController.setTimeZone(request.form, session['userid'])
        return redirect(url_for('index'))

@application.route(BASEPATH + '/reply', methods=['GET', 'POST'])
def scheduleReply():
    if 'userid' not in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        print( 'replying to ' + request.args['id'])
        tweet = ReplyController.getTweet(request.args['id'], session['userid'])
        userTimeZoneInfo = UserController.getUserTimeZone(session['userid'])
        print(userTimeZoneInfo)
        return render_template('createreply.html',tweet = tweet,
                timeZoneInformation=userTimeZoneInfo,
                timeToPost = datetime.now(tz=timezone(timedelta(hours=userTimeZoneInfo['hours'], minutes=userTimeZoneInfo['minutes'])))+timedelta(hours=1))
    else:
        scheduleResult = ReplyController.createReply(request.form, session['userid'])
        print(scheduleResult)
        if scheduleResult['result'] == 'success':
            return redirect(url_for('index'))
        else:
            return "FAIL"
@application.route(BASEPATH + '/viewschedule', methods=['GET'])
def viewSchedule():
    if 'userid' not in session:
        return redirect(url_for('login'))
    if ('view') not in request.args:
        return redirect(url_for('viewSchedule', view='unsent'))
    if request.args['view'] != 'unsent' and request.args['view'] != 'sent' and request.args['view'] != 'cancelled':
        return redirect(url_for('viewSchedule', view='unsent'))
    replies = ReplyController.getScheduledReplies(session['userid'], request.args['view'])
    return render_template('viewschedule.html', replySchedule = replies)

@application.route(BASEPATH+'/cancelreply', methods=['POST'])
def cancelReply():
    if 'userid' not in session:
        return redirect(url_for('login'))
    cancelResult = ReplyController.cancelReply(session['userid'], request.form['replyid'])
    if cancelResult['result'] == "success":
        return redirect(url_for('viewSchedule', view='unsent'))
