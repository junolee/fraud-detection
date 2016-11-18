from flask import Flask, request, render_template
from munging_stream import convert_data
from datetime import datetime
import pandas as pd
import numpy as np
import requests
import pickle
import socket
import json
import time
import sys
sys.path.insert(0, '../')

app = Flask(__name__)
PORT = 5000
REGISTER_URL = "http://10.6.80.211:5000/register"
DATA = []
TIMESTAMP = []

@app.route('/score', methods=['POST'])
def score():
    DATA.append(json.dumps(request.json, sort_keys=True, indent=4, separators=(',', ': ')))
    TIMESTAMP.append(time.time())
    return ""

@app.route('/check', methods=['GET'])
def check():
    line1 = "Number of data points: {0}".format(len(DATA))
    if DATA and TIMESTAMP:
        dt = datetime.fromtimestamp(TIMESTAMP[-1])
        data_time = dt.strftime('%Y-%m-%d %H:%M:%S')
        line2 = "Latest datapoint received at: {0}".format(data_time)
        line3 = type(DATA[-1])
        output = "{0}\n\n{1}\n\n{2}".format(line1, line2, line3)
    else:
        output = line1
    return output, 200, {'Content-Type': 'text/css; charset=utf-8'}

@app.route('/run_model', methods=['GET'])
def run_model():
    if len(DATA) < 1:
        return ""
    else:
        df = pd.Series(DATA[-1])
        df = convert_data(df)
        x = df.values
        prediction = model.predict(x)
        return prediction

def register_for_ping(ip, port):
    registration_data = {'ip': ip, 'port': port}
    requests.post(REGISTER_URL, data=registration_data)

if __name__ == '__main__':
    # Register for pinging service
    ip_address = socket.gethostbyname(socket.gethostname())
    print "attempting to register %s:%d" % (ip_address, PORT)
    register_for_ping(ip_address, str(PORT))
    with open("../model.pkl") as f:
        model = pickle.load(f)
    # Start Flask app
    app.run(host='0.0.0.0', port=PORT, debug=True)
