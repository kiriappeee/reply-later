from flask import session,url_for,request,redirect,render_template
from . import application
from .controllers import LoginController, UserController

BASEPATH = "/replylater/app"

@application.route(BASEPATH, methods=['GET'])
def index():
    if 'userid' in session:
        return 'hello ' + str(session['userid'])
    else:
        redirect(url_for('login'))

@application.route(BASEPATH + '/login', methods=['GET', 'POST'])
def login():
    if 'userid' in session:
        return redirect(url_for(index))
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
        return redirect(url_for('index'))

@application.route(BASEPATH + '/addtimezone', methods=['GET', 'POST'])
def addtimezone():
    if 'userid' not in session:
        return redirect(url_for(login))
    if request.method == 'GET':
        return render_template('updatetimezone.html')
    else:
        UserController.setTimeZone(request.form, session['userid'])
        return redirect(url_for('index'))
