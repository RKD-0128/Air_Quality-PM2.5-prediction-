# -*- coding: utf-8 -*-
"""Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zsKVS7ES58dxI-H_xaYOGcAYhbtNI7aq
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as snc
import tensorflow as tf
from tensorflow import keras
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from tensorflow.python.keras.layers.core import Dense, Activation

from google.colab import drive
drive.mount('/content/drive')

air_quality = pd.read_csv("/content/drive/MyDrive/fprojdata - final project data.csv", sep=",", decimal=",")
air_quality

air_quality.dropna(axis=0, how= 'all', inplace=True)
air_quality.dropna(axis=1, inplace=True)

air_quality.replace(to_replace= -200, value= np.NaN, inplace= True)
air_quality

air_quality.fillna(air_quality.mean(), inplace= True)

air_quality.loc[:,'Date']=air_quality['Date']
air_quality

from datetime import datetime
Date= []
for i in air_quality['Date']:
    Date.append(datetime.strptime(i,'%m/%d/%Y'))
air_quality.dtypes

date=pd.Series(Date)
air_quality['Date']=pd.to_numeric(date)

air_quality['Date']=air_quality['Date'].astype(float)
air_quality.dtypes
air_quality

air_quality.loc[:,'Time']=air_quality['Time']
 air_quality

from datetime import datetime
Time= []
for i in air_quality['Time']:
    Time.append(datetime.strptime(i,'%H:%M:%S'))
air_quality.dtypes

time=pd.Series(Time)
air_quality['Time']=pd.to_numeric(time)

air_quality['Time']=air_quality['Time'].astype(float)
air_quality['CO'] = pd.to_numeric(air_quality['CO'],errors = 'coerce')
air_quality['Benzene'] = pd.to_numeric(air_quality['Benzene'],errors = 'coerce')
air_quality['SO2'] = pd.to_numeric(air_quality['SO2'],errors = 'coerce')
air_quality['NO2'] = pd.to_numeric(air_quality['NO2'],errors = 'coerce')
air_quality['NO'] = pd.to_numeric(air_quality['NO'],errors = 'coerce')
air_quality.dtypes

air_quality.tail()

air_quality2=air_quality.corr('pearson')
air_quality2

abs(air_quality2['PM 2.5']).sort_values(ascending=False)

air_quality.tail()

from sklearn.preprocessing import MinMaxScaler

num = air_quality.keys()
scaler = MinMaxScaler()
scaler.fit(air_quality[num])
air_quality[num] = scaler.transform(air_quality[num])

snc.pairplot(air_quality[["Date","Time","CO","PM 10","NO","NOx","PM 2.5","SO2","NO2","Benzene"]],diag_kind = "auto")

features=air_quality
target=air_quality['PM 2.5']
features

features=features.drop('Date',axis=1)
features=features.drop('Time',axis=1)
features=features.drop('PM 2.5',axis=1)
features=features.drop('NO',axis=1)
features=features.drop('CO',axis=1)
features=features.drop('Benzene',axis=1)


features

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(features, target)

y_test.tail()

"""# Linear Regression"""

from sklearn.linear_model import LinearRegression

regressor = LinearRegression(normalize=True)
regressor.fit(X_train, y_train)

print("Predicted values of PM 2.5:", regressor.predict(X_test))
y_pred = regressor.predict(X_test)
y_pred.shape

print("R^2 score for liner regression: ", regressor.score(X_test, y_test))

plt.figure(figsize=(8,6))
plt.scatter(y_test,y_pred,color='maroon')
plt.title('Linear Regression')
plt.xlabel("True Values")
plt.ylabel("Predictions")
plt.show()

x = np.array(y_test)
y = np.array(y_pred)
plt.figure(figsize=(8,6))
plt.plot(x, color='grey')
plt.plot(y,color='red')
plt.xlim(0,100)
plt.xlabel("Index", color='maroon')
plt.ylabel("PM 2.5", color='maroon')
plt.legend(["actual values", "predicted values"], loc ="upper right")

plt.show()

"""# Lasso Regression"""

from sklearn.linear_model import Lasso

a=Lasso(alpha=0.5)
a.fit(X_train, y_train)

print("R^2 on train set : {}".format(a.score(X_train, y_train)))

print("Predicted values of PM 2.5:", a.predict(X_test))
y_predl = regressor.predict(X_test)
y_predl.shape

print("R^2 on test set : {}".format(a.score(X_test, y_test)))

plt.figure(figsize=(8,6))
plt.scatter(y_test,y_predl,color='orange')
plt.title('Lasso Regression')
plt.xlabel("True Values")
plt.ylabel("Predictions")
plt.show()

x = np.array(y_test)
y = np.array(y_predl)
plt.figure(figsize=(8,6))
plt.plot(x, color='black')
plt.plot(y, color='orange')
plt.xlim(0,100)
plt.xlabel("Index", color='maroon')
plt.ylabel("PM 2.5", color='maroon')
plt.legend(["actual values", "predicted values"], loc ="upper right")

plt.show()

"""# Decision Tree Regression"""

from sklearn.tree import DecisionTreeRegressor

dtr = DecisionTreeRegressor()
dtr.fit(X_train, y_train)

print("Coefficient of determination R^2 <-- on train set: {}".format(dtr.score(X_train, y_train)))

print("Predicted values of PM 2.5:", dtr.predict(X_test))
y_predt = regressor.predict(X_test)
y_predt.shape

print("Coefficient of determination R^2 <-- on test set: {}".format(dtr.score(X_test, y_test)))

plt.figure(figsize=(8,6))
plt.scatter(y_test,y_predt,color='purple')
plt.title('Decision Tree Regression')
plt.xlabel("True Values")
plt.ylabel("Predictions")
plt.show()

x = np.array(y_test)
y = np.array(y_predt)
plt.figure(figsize=(8,6))
plt.plot(x, color='red')
plt.plot(y, color='purple')
plt.xlim(0,100)
plt.xlabel("Index", color='maroon')
plt.ylabel("PM 2.5", color='maroon')
plt.legend(["actual values", "predicted values"], loc ="upper right")

plt.show()

"""# AdaBoost Regression"""

from sklearn.ensemble import AdaBoostRegressor

adb = AdaBoostRegressor()
adb.fit(X_train, y_train)

print("Coefficient of determination R^2 <-- on train set: {}".format(adb.score(X_train, y_train)))

print("Predicted values of PM 2.5:", adb.predict(X_test))
y_pred = regressor.predict(X_test)
y_pred.shape

print("Coefficient of determination R^2 <-- on test set: {}".format(adb.score(X_test, y_test)))

plt.figure(figsize=(8,6))
plt.scatter(y_test,y_pred,color='green')
plt.title('Adaboost Regression')
plt.xlabel("True Values")
plt.ylabel("Predictions")
plt.show()

x = np.array(y_test)
y = np.array(y_pred)
plt.figure(figsize=(8,6))
plt.plot(x, color='gold')
plt.plot(y,color='green')
plt.xlim(0,100)
plt.xlabel("Index", color='maroon')
plt.ylabel("PM 2.5", color='maroon')
plt.legend(["actual values", "predicted values"], loc ="upper right")

plt.show()

"""# K-Nearest Neighbors"""

from sklearn.neighbors import KNeighborsRegressor

knn = KNeighborsRegressor()
knn.fit(X_train, y_train)

print("Coefficient of determination R^2 <-- on train set: {}".format(knn.score(X_train, y_train)))

print("Predicted values of PM 2.5:", knn.predict(X_test))
y_pred = regressor.predict(X_test)
y_pred.shape

print("Coefficient of determination R^2 <-- on test set: {}".format(knn.score(X_test, y_test)))

plt.figure(figsize=(8,6))
plt.scatter(y_test,y_pred,color='hotpink')
plt.title('KNN Regression')
plt.xlabel("True Values")
plt.ylabel("Predictions")
plt.show()

x = np.array(y_test)
y = np.array(y_pred)
plt.figure(figsize=(8,6))
plt.plot(x,color='royalblue')
plt.plot(y,color='hotpink')
plt.xlim(0,100)
plt.xlabel("Index", color='maroon')
plt.ylabel("PM 2.5", color='maroon')
plt.legend(["actual values", "predicted values"], loc ="upper right")

plt.show()

"""# Random Forest Regression"""

from sklearn.ensemble import RandomForestRegressor
forest = RandomForestRegressor()
forest.fit(X_train, y_train)

f'Coefficient of determination R^2 on train set {forest.score(X_train, y_train)}'
# must be close to 1, 1 is perfect fit

print("Predicted values of PM 2.5:", dtr.predict(X_test))
y_pred = regressor.predict(X_test)
y_pred.shape

f'Coefficient of determination R^2 on test set {forest.score(X_test, y_test)}'

plt.figure(figsize=(8,6))
plt.scatter(y_test,y_pred,color='navy')
plt.title('Random Forest Regression')
plt.xlabel("True Values")
plt.ylabel("Predictions")
plt.show()

x = np.array(y_test)
y = np.array(y_pred)
plt.figure(figsize=(8,6))
plt.plot(x)
plt.plot(y)
plt.xlim(0,100)
plt.xlabel("Index", color='maroon')
plt.ylabel("PM 2.5", color='maroon')
plt.legend(["actual values", "predicted values"], loc ="upper right")

plt.show()

"""# Performance Comparion"""

x=['linear','LASSO','Decision-Tree','RandomForest','Adaboost','KNN']
y=[regressor.score(X_test, y_test),a.score(X_test, y_test),dtr.score(X_test, y_test),forest.score(X_test, y_test),adb.score(X_test, y_test),knn.score(X_test, y_test)]
plt.figure(figsize=(9,7))
plt.bar(x,y, width = 0.7 ,color='lightgreen')
plt.xlabel('REGRESSIONS', color='maroon')
plt.ylabel("ACCURACY", color='maroon' )
plt.title('Comparison of R^2', color='navy')
plt.show()