import numpy as np
import pandas as pd
import cPickle as pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, precision_score, recall_score

def split_data(df):
    y = df.pop('fraud').values
    X = df.values
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    return X_train, X_test, y_train, y_test

def model_fit(X_train, X_test, y_train, y_test):
    rf = RandomForestClassifier(n_estimators=100)
    rf.fit(X_train, y_train)
    return rf

def confuse(model, X_test, y_test):
    y_predict = model.predict(X_test)
    return confusion_matrix(y_test, y_predict), y_predict

def score(model, X_test, y_test):
    score = model.score(X_test, y_test)
    return score

if __name__ == "__main__":
    filepath = '../data/clean_data.csv'
    df = pd.read_csv(filepath)
    X_train, X_test, y_train, y_test = split_data(df)
    model= model_fit(X_train, X_test, y_train, y_test)
    mat, y_pred = confuse(model, X_test, y_test)
    acc = score(model, X_test, y_test)
    print "Accuracy:", acc

    with open("model.pkl", 'w') as f:
        pickle.dump(model, f)
