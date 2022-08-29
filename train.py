
from sklearn import linear_model
import pandas
import joblib
import time

df = pandas.read_csv("trail_data.csv")


x = df[['fb','ppl']]
y = df['fw']

regr = linear_model.LinearRegression()
regr.fit(x,y)

filename = 'ml_modle.sav'
joblib.dump(regr,filename)


print('\nModel Successfully Created! -> ' + filename)