import joblib as jb


filename = 'static/models/apple.sav'

load_model = jb.load(filename)

fb = int(input("Enter food bought : " ))
ppl = int(input('\nEnter Number of people : '))

print('\n\n')

r = load_model.predict([[fb,ppl]])



print('\n\nFood Wasted : '+ str(int(r))) 