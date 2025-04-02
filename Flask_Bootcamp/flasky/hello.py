from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
import os


# from flask import request
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
moment = Moment(app)


# Config Database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize the database and migration tool
migrate = Migrate(app, db)

# Initialize Flask-Mail
mail = Mail(app)

#Form Classes
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        old_name = session['name']
        if old_name is not None and old_name != form.name.data:
            flash('Your name has been changed!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', current_time = datetime.utcnow(), form = form, name = session.get('name'), known = session.get('known', False))

@app.route('/user/<name>')
def user(name=None):
    return render_template('user.html', user = name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

#Role and User model definition
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    
    def __repr__(self):
        return '<Role %r>' % self.name
    
    users = db.relationship('User', backref = 'role')
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)
    
    def __repr__(self):
        return '<User %r>' % self.username
    
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
# Shell command to create database
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Role': Role}
