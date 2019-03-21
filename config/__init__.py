from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd22068be55575b2dabd7f45817036a97bd499d81fb8e4098'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c1883100:auzAc5h4R3r3jKJ@csmysql.cs.cf.ac.uk:3306/c1883100'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'home'

from config import extra		
from config import routes