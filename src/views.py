from flask import session,url_for,request,redirect,render_template
from . import application
from .controllers import LoginController

BASEPATH = "/replylater/app"

@application.route(BASEPATH + '/login', methods=['GET', 'POST'])
def login():
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
        return "verified"
