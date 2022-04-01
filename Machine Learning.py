from sqlite3 import Row
import numpy
from scipy import stats
from pandas import read_csv
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

# #Removes Header
# with open("data.csv",'r') as f:
#     with open("data_nh.csv",'w') as f1:
#         next(f) # skip header line
#         for line in f:
#             f1.write(line)
#Load data
dataSet = read_csv("data.csv")

#Describe the dataset
mean = numpy.mean(dataSet)
median = numpy.median(dataSet)
mode = stats.mode(dataSet)
standardDeviation = numpy.std(dataSet)
variance = numpy.var(dataSet)

X = dataSet.loc[:,["Choice 1",'Choice 2','Choice 3','Choice 4','Choice 5','Choice 6','Choice 7','Choice 8','Choice 9','Choice 10']]
y = dataSet.loc[:,"Final Score"]

#Histogram
# plt.hist(dataSet, 10)
# plt.show()

#Scatterplot only works for two variables correlation
#plt.scatter(x, y)
#plt.show()

#Scatterplot Matrix multiple variable correlation
# df = pd.DataFrame({
# "Choice 1": dataSet.loc[:,"Choice 1"],
# "Choice 2": dataSet.loc[:,"Choice 2"],
# "Choice 3": dataSet.loc[:,"Choice 3"],
# "Choice 4": dataSet.loc[:,"Choice 4"],
# "Choice 5": dataSet.loc[:,"Choice 5"],
# "Choice 6": dataSet.loc[:,"Choice 6"],
# "Choice 7": dataSet.loc[:,"Choice 7"],
# "Choice 8": dataSet.loc[:,"Choice 8"],
# "Choice 9": dataSet.loc[:,"Choice 9"],
# "Choice 10": dataSet.loc[:,"Choice 10"],
# 'Final Result':y})
# df.head()
# scatter_matrix(df)
# plt.show()

#Split the dataset
train_x = X[:80]
train_y = y[:80]

test_x = X[80:]
test_y = y[80:]

#Multiple Regression
#regr = linear_model.LinearRegression()
regr = RandomForestRegressor(n_estimators = 100, random_state = 0)
#Fit the model
regr.fit(train_x, train_y)

#Test the model and show its accuracy
predictions = regr.predict(test_x)
print(r2_score(test_y, predictions))

predictedFinalScore = regr.predict([[3, 3, 3, 3, 3 , 3, 3, 3, 3, 3]])
print(predictedFinalScore)

#Print describing values
#print("Mean \n", mean, "\nMedian \n", median, "\nMode \n", mode, "\nStandard Deviation \n",  standardDeviation, "\nVariance \n", variance, "\n")