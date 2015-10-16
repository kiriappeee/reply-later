from flask import session,url_for,request,redirect,render_template
from . import application

BASEPATH = "/replylater/app"

@application.route(BASEPATH + '/login', methods=['GET', 'POST'])
def login():
    return 'Hello world'
