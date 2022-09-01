import joblib as jb

# Setting saved model location
filename = 'static/models/apple.sav'

# Loading the model
load_model = jb.load(filename)

# Getting input from the user 
fb = int(input("Enter food bought : " ))
ppl = int(input('\nEnter Number of people : '))

print('\n\n')

# Making predictions based on user inputs
r = load_model.predict([[fb,ppl]])
print('\n\nFood Wasted : '+ str(int(r))) 