
from flask import request, Flask, jsonify,render_template

import joblib as jb
import numpy as np

app  = Flask(__name__)

@app.route('/signUp')
def signUp():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/shop-1')
def shop1():
    return render_template('new-grocery-list.html')

@app.route('/shop-2')
def shop2():
    return render_template('grocery-checklist.html')

@app.route('/delete')
def delete():
    return render_template('grocery-wasted-list.html')

@app.route('/dash')
def dash():
    return render_template('dash.html')


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


