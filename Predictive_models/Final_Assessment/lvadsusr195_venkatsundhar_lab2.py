# -*- coding: utf-8 -*-
"""LVADSUSR195_Venkatsundhar_LAB2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kGLYiWaEn6x-wEN3AaJ6zSjkX8fzMORm
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

1) LOAD

df = pd.read_csv('/content/sample_data/penguins_classification.csv')
df.head()

"""2) Preprocess"""

# To check null values
df.isnull().sum()

df.dropna(inplace=True)

# To check for duplicates
df.duplicated().sum()

# No null and duplicates values

# Finding outliers using boxplot
for c in df.select_dtypes(include=['int64','float64']).columns:
  sns.boxplot(df[[c]])

# There is no significant outliers so we will continue working with the dataset

"""3) EDA"""

df.shape

df.head()

df.info()

df.describe()

df.columns

# We will label encode the categorical values into numerical so that we can improve model performance
L = LabelEncoder()
for c in df[['species','island','year']]:
  df[c] = L.fit_transform(df[c])
df.head()

df.info()

# We will do bivariate analysis to find the relationship between the variables using Correlation matrix
# Correlation to find the strength between variables
sns.heatmap(df.select_dtypes(include=['int64','float64']).corr(),annot=True,fmt='.2f')

df.columns

X = df[['bill_depth_mm','flipper_length_mm']]
y = df['species']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)

s = MinMaxScaler()
X_train = s.fit_transform(X_train)
X_test = s.transform(X_test)

rf = RandomForestClassifier(n_estimators=101,max_depth=3)

rf.fit(X_train,y_train)

predict = rf.predict(X_test)
print("Accuracy:",accuracy_score(y_test,predict))
print("Recall:",recall_score(y_test,predict))
print("F1 Score:",f1_score(y_test,predict))
print("Classification Report:",classification_report(y_test,predict))
print("Confusion Matrix:",confusion_matrix(y_test,predict))

