from flask import Flask
application=Flask(__name__)

import configparser
from . import views

c = configparser.ConfigParser()
c.read('src/config.ini')
application.secret_key=c['SECRETKEY']['secretKey']


