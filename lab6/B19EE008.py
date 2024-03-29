# -*- coding: utf-8 -*-
"""B19EE008_Lab_6.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ByaZStCAWRkiyciaf-iNm8FwfO5dyPzi
"""

import pandas  as pd #Data manipulation
import numpy as np #Data manipulation
import matplotlib.pyplot as plt # Visualization
import seaborn as sns #Visualization
plt.rcParams['figure.figsize'] = [8,5]
plt.rcParams['font.size'] =14
plt.rcParams['font.weight']= 'bold'
plt.style.use('seaborn-whitegrid')

# Import dataset
# path ='dataset/'
path = '/content/'
df = pd.read_csv(path+'insurance.csv')
print('\nNumber of rows and columns in the data set: ',df.shape)

df.head()

# desribe the dataset (Exploratory data analysis) 
df.describe()

df.info()

#Check for missing value
plt.figure(figsize=(15,5))
sns.heatmap(df.isnull(),cbar=False,cmap='viridis',yticklabels=False)
plt.title('Missing data value in the data');

# To find the correlation among the columns
corr_p = df.corr(method ='pearson') #'pearson’, ‘kendall’, ‘spearman'
corr_p

# correlation plot
sns.heatmap(corr_p, cmap = 'Wistia', annot= True);

"""from Kendall method

"""

corr_k = df.corr(method ='kendall') #'pearson’, ‘kendall’, ‘spearman'
corr_k

# correlation plot for kendall method
sns.heatmap(corr_k, cmap = 'Wistia', annot= True);

f= plt.figure(figsize=(15,5))

ax=f.add_subplot(121)
sns.distplot(df['charges'],color='g',ax=ax)
ax.set_title('Distribution of Insurance charges')
ax=f.add_subplot(122)
sns.distplot(np.log10(df['charges']),color='y',ax=ax)
ax.set_title('Distribution of Insurance charges in log')
ax.set_xscale('log');

"""#Convert categorical data into numbers


*   Label Enocding
*   One hot Encoding


#Lable Encoding
Label encoding refers to transforming the word labels into numerical form so that the algorithms can understand how to operate on them.

#One hot Encoding
A One hot encoding is a representation of categorical variable as binary vectors.It allows the representation of categorical data to be 
more expresive. This first requires that the categorical values be mapped to integer values, that is label encoding. Then, each integer 
value is represented as a binary vector that is all zero values except the index of the integer, which is marked with a 1.

You may take help of pandas get_dummies function for this.

lable encoding
"""

df["sex"] = df["sex"].astype('category')
df["smoker"] = df["smoker"].astype('category')
df["region"] = df["region"].astype('category')

df["sex"] = df["sex"].cat.codes
df["smoker"] = df["smoker"].cat.codes
df["region"] = df["region"].cat.codes

df.head()

# Log transform of dependent variable
df['charges'] = np.log(df['charges'])

#Train Test split
from sklearn.model_selection import train_test_split
X = df.drop('charges',axis=1)
y = df['charges'] 

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=35)

"""#Model building"""

# Step 1: add x0 =1 to dataset
X_train_theta = np.c_[np.ones((X_train.shape[0],1)),X_train]
X_test_theta = np.c_[np.ones((X_test.shape[0],1)),X_test]
# Step2: build model
theta = np.matmul(np.linalg.inv( np.matmul(X_train_theta.T,X_train_theta) ), np.matmul(X_train_theta.T,y_train)) 
# The parameters for linear regression model
all_theta = []
for i in range(X_train_theta.shape[1]):
  all_theta.append('theta-'+str(i))
feachers = ['intersect:x_0=1'] + list(X.columns.values)
df_feachers = pd.DataFrame({'All_thetas':all_theta,'feachers':feachers,'theta':theta})
df_feachers

# Scikit Learn module
from sklearn.linear_model import LinearRegression
lr = LinearRegression()
lr.fit(X_train,y_train)

#Parameter
sk_theta = [lr.intercept_]+list(lr.coef_)
df_feachers = df_feachers.join(pd.Series(sk_theta, name='sk_theta'))
df_feachers

"""#Model evaluation"""

# prediction
y_pred =  np.matmul(X_test_theta,theta) 

#Evaluvation: MSE (Write your MSE equation from scratch)
J_mse = np.sum((y_pred - y_test)**2)/ (X_test_theta.shape[0])

y_pred

print('The Mean Square Error(MSE) or J(theta) is: ',J_mse)

# sklearn regression module
y_pred_sk = lr.predict(X_test)

#Evaluvation: MSE
from sklearn.metrics import mean_squared_error as mse
J_mse_sk = mse(y_pred_sk, y_test)

y_pred_sk

print('The Mean Square Error(MSE) or J(theta) is: ',J_mse_sk)

# Check for Linearity
f = plt.figure(figsize=(15,5))
# from normal prediction
ax = f.add_subplot(121)
sns.scatterplot(y_test,y_pred,ax=ax,color='g')
ax.set_title(' Actual Vs Predicted value from normal model')
# from sklearn prediction
ax = f.add_subplot(122)
sns.scatterplot(y_test,y_pred_sk,ax=ax,color='y')
ax.set_title(' Actual Vs Predicted value from sklearn')