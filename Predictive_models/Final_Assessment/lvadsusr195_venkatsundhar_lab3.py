# -*- coding: utf-8 -*-
"""LVADSUSR195_Venkatsundhar_LAB3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1vSW14uaDyZsI5SEpJDzKuLOJLuyNLuhQ
"""

import numpy as np
import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
from sklearn.tree import export_graphviz
from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier, GradientBoostingClassifier, IsolationForest
from sklearn.model_selection import cross_val_score
from xgboost import XGBClassifier
import xgboost
from lightgbm import LGBMClassifier
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import confusion_matrix, classification_report, f1_score, roc_curve, roc_auc_score, precision_recall_curve, auc, r2_score, mean_squared_error, accuracy_score, recall_score, silhouette_score, silhouette_samples,mean_absolute_error
warnings.filterwarnings('ignore')

"""1) LOAD DATA"""

df = pd.read_csv('/content/sample_data/customer_segmentation.csv')
df.head()

"""2) PREPROCESSING"""

df.info()

# To check null values
df.isnull().sum()

24/2240
# Only 1 percent of null values we will remove it

df.dropna(inplace=True)

df.isnull().sum()

# To check for duplicates
df.duplicated().sum()

# We have no duplicates

# Outlier check
for c in df.select_dtypes(include=['int64','float64']).columns:
  plt.figure(figsize=(10,7))
  sns.boxplot(df[c])

# There are outliers and we will treat it
for c in df.select_dtypes(include=['int64','float64']).columns:
  q1 = df[c].quantile(0.25)
  q3 = df[c].quantile(0.75)
  iqr = q3-q1
  lwr = q1-1.5*iqr
  upr = q3+1.5*iqr
  df.loc[df[c]>upr,c]=upr
  df.loc[df[c]<lwr,c]=lwr

# Outlier re-check
for c in df.select_dtypes(include=['int64','float64']).columns:
  plt.figure(figsize=(10,7))
  sns.boxplot(df[[c]])

# Outlier have been removed

"""3) EDA"""

df.columns

df.head()

df.info()

df.head()

L = LabelEncoder()
for c in df[['Year_Birth', 'Education', 'Marital_Status']]:
  df[c]=L.fit_transform(df[c])
df.head()

corr = df[['Year_Birth', 'Education', 'Marital_Status', 'Income', 'Kidhome',
       'Teenhome','Recency','NumDealsPurchases', 'NumWebPurchases',
       'NumCatalogPurchases', 'NumStorePurchases', 'NumWebVisitsMonth']].corr()
sns.heatmap(corr,annot=True,fmt='.2f')

scaler = MinMaxScaler()
for c in df.select_dtypes(include = ['int64','float64','int32']):
  df[c] = scaler.fit_transform(df[[c]])

"""4) MODEL"""

km = KMeans(n_clusters=3)
predict = km.fit_predict(df[['Income','NumCatalogPurchases']])
df['cluster'] = predict
print(km.cluster_centers_)

df1 = df[df['cluster']==0]
df2 = df[df['cluster']==1]
df3 = df[df['cluster']==2]

plt.scatter(df1.Income,df1['NumCatalogPurchases'],color='green')
plt.scatter(df2.Income,df2['NumCatalogPurchases'],color='black')
plt.scatter(df3.Income,df3['NumCatalogPurchases'],color='red')
plt.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],color='purple',marker='*',label='centroid')
plt.xlabel('Income')
plt.ylabel('NumCatalogPurchases')
plt.legend()

"""5) EVAL METRICS"""

silhouette_score(df[['Income','NumCatalogPurchases']],predict)

sse = [] # The sum of Squared Errors =SSE
for k in range(1,11):
   km = KMeans(n_clusters=k)
   km.fit(df[['Income','NumCatalogPurchases']])
   sse.append(km.inertia_)

plt.xlabel('K')
plt.ylabel('Sum of squared error')
plt.plot(range(1,11),sse)

