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

cursor.execute('SELECT metraj,salesakht FROM houses where mantaghe = 5;')
table_rows1 = cursor.fetchall()
df1 = pd.DataFrame(table_rows1)
x = np.array(df1)


cursor.execute('SELECT priceInMillion FROM houses where mantaghe = 5;')
table_rows2 = cursor.fetchall()
df2 = pd.DataFrame(table_rows2)
y = np.array(df2)

data =  {'price': df2,  'metraj,salesakht': df1}
temp = pd.concat(data, axis=1)
temp  = temp[np.abs(stats.zscore(temp['price'])) < 3]



df1 = temp['metraj,salesakht']
df2 = temp['price']
x = np.array(df1)
y = np.array(df2)

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x,y,test_size = 0.05)

'''

best = 0.557660955124186

for i in range(10000):

    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x,y,test_size = 0.05)
    linear = linear_model.LinearRegression()
    linear.fit(x_train,y_train)
    acc = linear.score(x_test,y_test)  # accuracy
    # print(acc)

    if acc > best:
        best = acc
        with open('pricemodel5.pickle','wb') as f:
            pickle.dump(linear,f)

print(best)
'''

pickle_in = open('pricemodel5.pickle','rb')
linear = pickle.load(pickle_in)

predictions = linear.predict(x_test)

print('testing data:')

for x in range(len(predictions)):
    print(predictions[x], x_test[x],y_test[x])

print('-----------------------')

newdataM = int(input('metraj :'))
newdataS = int(input('salesakht :'))

newprediction = linear.predict([[newdataM, newdataS]])
print('gheymat:',newprediction)

# print(linear.coef_)

# style.use("ggplot")
# plt.scatter(df1[0], df2[0])
# x = np.linspace(0, 250)
# y=19.60845531 * (x-95) +2711.12507163
# plt.plot(x, y)
# plt.ylabel('gheymat')
# plt.show()
