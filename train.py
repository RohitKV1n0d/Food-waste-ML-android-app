# Importing the necessary libraries 
from sklearn import linear_model
import pandas
import joblib
import time

# Preparing the Dataset for training
df = pandas.read_csv("static/datasets/yogurt.csv")

# Assigning the data set to each axis
x = df[['fb','ppl']]
y = df['fw']

# Creating a Regression model object
regr = linear_model.LinearRegression()
# Traning the model
regr.fit(x,y)

# Saving the model to a location
filename = 'static/models/yogurt.sav'
joblib.dump(regr,filename)


print('\nModel Successfully Created! -> ' + filename) 