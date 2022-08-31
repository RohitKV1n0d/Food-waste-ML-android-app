
from sklearn import linear_model
import pandas
import joblib
import time

df = pandas.read_csv("static/datasets/yogurt.csv")


x = df[['fb','ppl']]
y = df['fw']

regr = linear_model.LinearRegression()
regr.fit(x,y)

filename = 'static/models/yogurt.sav'
joblib.dump(regr,filename)


print('\nModel Successfully Created! -> ' + filename) 