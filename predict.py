import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cPickle as pickle

if __name__ == "__main__":

    # read in a single example and vectorize
    df = pd.read_csv('../data/test_script_examples.csv').iloc[0]
    y = df.pop('fraud')
    x = df.values.reshape(1, -1)

    # unpickle model
    with open("model.pkl") as f:
        model = pickle.load(f)

    # predict probability
    y = model.predict(x)[0]

    # print probability
    print y
