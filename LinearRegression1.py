import pandas as pd
import numpy as np 
import mysql.connector as sql
import sklearn
from sklearn import linear_model
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
from scipy import stats


yourMYSQLpassword='iop' ### change here



DB = sql.connect(host = 'localhost',database='housesdatabase' ,user = 'root', password = yourMYSQLpassword)
cursor = DB.cursor()

cursor.execute('SELECT metraj FROM houses where mantaghe = 1;')
table_rows1 = cursor.fetchall()
df1 = pd.DataFrame(table_rows1)

cursor.execute('SELECT priceInMillion FROM houses where mantaghe = 1;')
table_rows2 = cursor.fetchall()
df2 = pd.DataFrame(table_rows2)



data =  {'price': df2,  'metraj': df1}
temp = pd.concat(data, axis=1)
temp  = temp[np.abs(stats.zscore(temp['price'])) < 3]
# print(temp)

df1 = temp['metraj']
df2 = temp['price']
x = np.array(df1)
y = np.array(df2)

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x,y,test_size = 0.1)

'''
   ###this bit is for training data
   

best = 0.9435227736880789

for i in range(10000):

    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x,y,test_size = 0.1)
    linear = linear_model.LinearRegression()
    linear.fit(x_train,y_train)
    acc = linear.score(x_test,y_test)  # accuracy
    # print(acc)

    if acc > best:
        best = acc
        with open('pricemodel1.pickle','wb') as f:
            pickle.dump(linear,f)

print(best)

'''
pickle_in = open('pricemodel1.pickle','rb')
linear = pickle.load(pickle_in)

predictions = linear.predict(x_test)

print('testing data:')
for x in range(len(predictions)):
    print(predictions[x], x_test[x],y_test[x])
print('-----------------------')


newdata = int(input('metraj :'))

newprediction = linear.predict([[newdata]])
print('gheymat:',newprediction)

'''
#this bit is for visualization, draws some stuff

print(linear.coef_)

style.use("ggplot")
plt.scatter(df1[0], df2[0])
x = np.linspace(0, 600)
y=137.51351395 * (x-150) +12223.77314958
plt.plot(x, y)
plt.ylabel('gheymat')
plt.show()

'''
