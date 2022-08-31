
from enum import unique
from math import frexp
from datetime import date, datetime
import os
import re
from urllib.response import addclosehook
from flask import request, Flask, jsonify,render_template, session,redirect,url_for

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from flask_wtf import FlaskForm
from sqlalchemy.orm import backref
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import validators
from wtforms.validators import InputRequired, Email, Length

from flask_sqlalchemy import SQLAlchemy
import string

import joblib as jb
import numpy as np

app  = Flask(__name__)
app.secret_key = 'asdaasdasdsdasdasasdasddasdasdasdaveasdaqvq34c'




ENV = 'prod'

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
   # __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30),unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)

    aglist = db.relationship('AllGrosseryLists', backref='aglist')
    fwlist = db.relationship('FoodWastedList', backref='fwlist')
    glist1 = db.relationship('GrosseryList', backref='glist1')






class AllGrosseryLists(db.Model):
    __tablename__ = 'allgrosserylists'
    agid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    date = db.Column(db.String(300), nullable=False) 
    alllist_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    glist = db.relationship('GrosseryList', backref='glist')
 

class GrosseryList(db.Model):
    __tablename__ = 'grosserylist'
    gid = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    expirydate = db.Column(db.String(300), nullable=False)  
    members = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(10), nullable=False)
    ifwasted = db.Column(db.Boolean, default=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    agid = db.Column(db.Integer, db.ForeignKey('allgrosserylists.agid'))





class FoodWastedList(db.Model):
    __tablename__ = 'foodwastedlist'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    fb = db.Column(db.Integer, nullable=False)
    ppl = db.Column(db.Integer, nullable=False)
    fw = db.Column(db.Integer)
    fw_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    






login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired('username is required'),Length(min=8,max=20) ])
    password = PasswordField('password', validators= [InputRequired(), Length(min=8, max=81, message=('8 letters!')) ])
    submit = SubmitField("Register")
    
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired('username is required'),Length(min=8,max=20), ])
    password = PasswordField('password', validators= [InputRequired(), Length(min=8, max=81, message=('8 letters!')) ])
    submit = SubmitField("Login")



    




@app.route('/')
@app.route('/home',methods = ["GET",'POST'])
@login_required
def home():
    cid = current_user.id
    today = date.today()
    allglist = GrosseryList.query.filter_by(creator_id=cid).order_by(GrosseryList.expirydate).all()
    cdata=()
    l1=[]

    for i in allglist:
        fdate = i.expirydate
        y =int(fdate[0:4])
        m = int(fdate[5:7])
        d =int(fdate[8:10])
        future = date(y,m,d)
        diff = future - today
        days = diff.days
        if days < 5:
            daysleft = str(days)+" Days Left"
            cdata=()
            cdata=(i.name,'-',daysleft)
            l1.append(cdata)
    
    return render_template('home.html',data=l1)


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


@app.route('/newitem/<int:agid>', methods = ["GET",'POST'])
@login_required
def newitem(agid):
    if request.method == 'POST':
        agid = agid
        cid = current_user.id
        addlist = GrosseryList(type=request.form['type'], name=request.form['name'], expirydate=request.form.get('exdate'),
                                members=int(request.form['members']), quantity=int(request.form['quantity']), unit=request.form['unit'],
                                agid=agid, creator_id=cid )
        db.session.add(addlist)
        db.session.commit()
        
        return redirect(url_for('gclist',id=agid))
    return render_template('new-grocery-list.html')


@app.route('/newlist', methods = ["GET",'POST'])
@login_required
def newlist():
    
    if request.method == 'POST':
        cid = current_user.id
        today = date.today()
        addnewlistname = AllGrosseryLists(name=request.form['name'] ,date=today.strftime("%d/%m/%Y") ,alllist_id=cid )
        db.session.add(addnewlistname)
        db.session.commit()
        return redirect(url_for('glist'))

    return render_template('new-list.html')

@app.route('/glist',methods = ["GET",'POST'])
@login_required
def glist():
    cid = current_user.id
    list_data = AllGrosseryLists.query.filter_by(alllist_id=cid).all()
    cdata=()
    l1=[]
    for i in list_data:
        cdata=()
        cdata=(i.agid,i.name,i.date)
        l1.append(cdata)
    print(l1)
    return render_template('grocery-list.html',data=l1)

@app.route('/gclist/<int:id>',methods = ["GET",'POST'])
@login_required
def gclist(id):
    gid=id
    list_data= GrosseryList.query.filter_by(agid=id).all()
    cdata=()
    l1=[]
    for i in list_data:
        cdata=()
        cdata=(i.gid,i.name,i.quantity,i.unit)
        l1.append(cdata)
    return render_template('grocery-checklist.html',id=id,data=l1,i=1)


@app.route('/wasted')
@login_required
def delete():
    cid = current_user.id
    today = date.today()
    allglist = GrosseryList.query.filter_by(creator_id=cid).order_by(GrosseryList.expirydate).all()
    cdata=()
    l1=[]

    for i in allglist:
        fdate = i.expirydate
        y =int(fdate[0:4])
        m = int(fdate[5:7])
        d =int(fdate[8:10])
        future = date(y,m,d)
        diff = future - today
        days = diff.days
        daysleft = str(days)+" Days Left"
        cdata=()
        if i.ifwasted == False:
            cdata=(i.gid,i.name,i.quantity,daysleft)
            l1.append(cdata)

    return render_template('grocery-wasted-list.html',data=l1)

@app.route('/dash')
@login_required
def dash():
    return render_template('dashboard.html')


@app.route('/repwasted/<int:id>', methods=['POST','GET'])
@login_required
def repwasted(id):
    glist = GrosseryList.query.filter_by(gid=id).first()
    if request.method == 'POST':
        cid=current_user.id
        addWasted = FoodWastedList(type=glist.type, name=glist.name ,fb=glist.quantity,
                                     ppl=glist.members, fw=request.form['quantity'], fw_id=cid)
        db.session.add(addWasted)
        
        # addwated2 = GrosseryList(ifwasted=True)
        glist.ifwasted=True
        db.session.commit()
        return redirect(url_for('delete'))

    return render_template('report-wasted.html',glist=glist) 

@app.route('/delete/<int:id>', methods=['POST','GET'])
@login_required
def deleteg(id):
    to_delete = AllGrosseryLists.query.get_or_404(id)
    try:
        db.session.delete(to_delete)
        db.session.commit()
        return redirect(url_for('glist'))
    except:
        return "Somthing went wrong"

@app.route('/deleteitem/<int:id>/<int:agid>', methods=['POST','GET'])
def deleteitem(id,agid):
    to_delete = GrosseryList.query.get_or_404(id)
    try:
        db.session.delete(to_delete)
        db.session.commit()
        return redirect(url_for('gclist',id=id,agid=agid))
    except:
        return "Somthing went wrong"


@app.route('/predict/<int:fb>/<int:ppl>/<string:name>', methods = ['POST','GET'])
def predict(fb,ppl,name):
    fb = fb
    ppl = ppl
    name=name
    filename = 'static/models/'+name.lower()+'.sav'

    load_model = jb.load(filename)
    res = load_model.predict([[fb,ppl]])
    
    return str(int(res))

@app.route('/logout',methods = ["GET",'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# if __name__=='__main__':
#     app.run(debug=True,host='0.0.0.0',port=5000)
if __name__=='__main__':
    app.run(debug=True)









