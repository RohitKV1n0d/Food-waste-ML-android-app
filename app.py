
from enum import unique
from math import frexp
import os
from flask import request, Flask, jsonify,render_template, session,redirect,url_for

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from flask_wtf import FlaskForm
from sqlalchemy.orm import backref
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import validators
from wtforms.validators import InputRequired, Email, Length

from flask_sqlalchemy import SQLAlchemy

import joblib as jb
import numpy as np

app  = Flask(__name__)
app.secret_key = 'asdaasdasdsdasdasasdasddasdasdasdaveasdaqvq34c'




ENV = 'dev'

if ENV == 'dev' :
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
    app.config['SECRET_KEY'] = 'asdas123dasdasdasddasdassdaveqvq34c'

else:
    app.debug = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SECRET_KEY'] = SECRET_KEY
    
SQLALCHEMY_TRACK_MODIFICATIONS = False






db =SQLAlchemy(app)





class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30),unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)






login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired('username is required'),Length(min=8,max=20) ])
    password = PasswordField('password', validators= [InputRequired(), Length(min=8, max=81, message=('8 letters!')) ])
    submit = SubmitField("Regiseter")
    
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired('username is required'),Length(min=8,max=20), ])
    password = PasswordField('password', validators= [InputRequired(), Length(min=8, max=81, message=('8 letters!')) ])
    submit = SubmitField("Login")
    


@app.route('/')
@app.route('/home')
@login_required
def home():
    return render_template('home.html')


@app.route('/signup',methods = ["GET",'POST'])
def signup(): 
    form = RegisterForm()

    # if request.method == 'POST':
    #     usrname = request.form['username']
    #     user = Users.query.filter_by(username=usrname).first
    #     if user == None:
    #         user = Users(username=usrname, password=request.form['password'])
    #         db.session.add(user)    
    #         db.session.commit()
    #         return render_template('login.html')

    if form.validate_on_submit():
        addUser = Users(username=form.username.data, password=form.password.data)
        db.session.add(addUser)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html',form=form)


        

@app.route('/login', methods = ["GET",'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if form.password.data == user.password:
                login_user(user)
                return redirect(url_for('home'))

    return render_template('login.html',form=form)


@app.route('/newlist')
@login_required
def shop1():
    return render_template('new-grocery-list.html')

@app.route('/glist')
@login_required
def shop2():
    return render_template('grocery-checklist.html')

@app.route('/wasted')
@login_required
def delete():
    return render_template('grocery-wasted-list.html')

@app.route('/dash')
@login_required
def dash():
    return render_template('dashboard.html')

@app.route('/logout',methods = ["GET",'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)






# @app.route('/predict', methods = ['POST'])
# def predict():
#     fw = request.form.get('fw')
#     ppl = request.form.get('ppl')
    
#     filename = 'ml_modle.sav'

#     load_model = jb.load(filename)
#     res = load_model.predict([[fw,ppl]])
    

#     return jsonify({'result':int(res)})


