from flask import Flask
application=Flask(__name__, static_url_path='/replylater/app/static')

import configparser
from . import views

c = configparser.ConfigParser()
c.read('src/config.ini')
application.secret_key=c['SECRETKEY']['secretKey']


