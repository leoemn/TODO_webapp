from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my.db'
app.config['SECRET_KEY'] = 'a3ky2jfu2andgth78f'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


from todo import routes