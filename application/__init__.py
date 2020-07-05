from flask import Flask
from flask_mysqldb import MySQL
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Aniket@4112'
app.config['MYSQL_DB'] = 'HMS'

# Intialize MySQL
mysql = MySQL(app)

from application import routes