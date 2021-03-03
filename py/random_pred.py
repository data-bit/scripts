import matplotlib.pyplot as plt
import numpy as np
import pandas
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import sqlalchemy
import pypyodbc
import pyodbc

# Load dataset
url = "AirPassengers.csv"
names = ['Serial Number', 'Time', 'Air Passengers']
dataset = pandas.read_csv(url, names=names)
print(dataset.describe())
print(dataset)


#Creating Validation Sets

array = dataset.values
X = array[1:, 0:4]
Y = array[1: ,2]
validation_size = 0.30
seed = 5
X_train, X_validation, Y_train, Y_validation = 
model_selection.train_test_split(X,Y,test_size=validation_size, 
random_state=seed)

#Test Harness and Evaluation Metrics 
seed = 5
scoring = 'accuracy'

#Building Models

models = []
models.append(('LR', LogisticRegression()))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC()))
# evaluate each model in turn
results = []
names = []

for name, model in models:
    kfold = model_selection.KFold(n_splits=10, random_state=seed)
    cv_results = model_selection.cross_val_score(model, X_train, Y_train, 
cv=kfold, scoring=scoring)
    results.append(cv_results)
    names.append(name)
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)



conn = pyodbc.connect(
    r'DRIVER={ODBC Driver 11 for SQL Server};'
    r'SERVER=Q3GN0570\MSSQLSERVER1;'
    r'DATABASE=AdventureWorksDW2014;'
    r'Trusted_Connection=yes;'
    )

cursorexec = conn.cursor()

cursorexec.execute("INSERT INTO pythonTest(LR,LDA,KNN,CART,NB,SVM) VALUES 
(?,?,?,?,?,?)", results)

cursorexec.commit()

conn.close()