from flask import Flask, request, jsonify
import json
import sys
import time
import numpy as np
import pandas as pd
from cca import GCCA_SSVEP
from cca import MsetCCA_SSVEP

app = Flask(__name__)

DEFAULT_FILENAME = r"C:\Users\RISHI\Desktop\FYP\EEG-decoding\eeg_lib\log\\"

stim_freqs = [7,10,12] # stim freqs used
fs = 256 # sampling freq
Ns = 256 # number of sample points to consider
Nh = 1 # number of harmonics for CCA-based algos
number_train = 4

gcca = GCCA_SSVEP(stim_freqs, fs, Nh=Nh)
mset_cca = MsetCCA_SSVEP(stim_freqs)

train7 = []
train10 = []
train12 = []

def write_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def read_json(filename):
    with open(filename) as f:
        return json.load(f)

def flatten(t):
    return [item for sublist in t for item in sublist]

@app.route('/7hz', methods=["POST"])
def cal7():
    data = request.get_json(force=True)
    train7.append(data['7'])
    return jsonify(msg="successfully received"), 200

@app.route('/10hz', methods=["POST"])
def cal10():
    data = request.get_json(force=True)
    train10.append(data['10'])
    return jsonify(msg="successfully received"), 200

@app.route('/12hz', methods=["POST"])
def cal12():
    data = request.get_json(force=True)
    train12.append(data['12'])
    return jsonify(msg="successfully received"), 200

@app.route('/message', methods=["POST"])
def message():
    data = request.get_json(force=True)
    print(data)
    return jsonify(msg="successfully received"), 200

@app.route('/isCalibrated', methods=["GET"])
def calibrate():

    sourceFile = open(DEFAULT_FILENAME+'7hz_calibration.txt', 'w')
    print(flatten(train7) , file = sourceFile)
    sourceFile.close()
  
    sourceFile = open(DEFAULT_FILENAME+'10hz_calibration.txt', 'w')
    print(flatten(train10) , file = sourceFile)
    sourceFile.close()

    sourceFile = open(DEFAULT_FILENAME+'12hz_calibration.txt', 'w')
    print(flatten(train12) , file = sourceFile)
    sourceFile.close()

    train7_reshape = np.array(train7).reshape(number_train,fs)
    train7_cal = train7_reshape.T.reshape(1,fs,number_train)

    train10_reshape = np.array(train10).reshape(number_train,fs)
    train10_cal = train10_reshape.T.reshape(1,fs,number_train)

    train12_reshape = np.array(train12).reshape(number_train,fs)
    train12_cal = train12_reshape.T.reshape(1,fs,number_train)

    cal_data = np.array([train7_cal, train10_cal, train12_cal])

    gcca.fit(cal_data)
    mset_cca.fit(cal_data)

    # print(data_tensor[0,:,:,0].shape)
    # print(mset_cca.classify(data_tensor[0,:,:,0]))
    return "calibrated", 200

decoding_data = []

@app.route('/decode', methods=["POST"])
def decoding():
    decode_data = request.get_json(force=True)

    decoding_data.append(decode_data['raw_data'])

    sourceFile = open(DEFAULT_FILENAME+'decoding_data.txt', 'w')
    print(flatten(decoding_data) , file = sourceFile)
    sourceFile.close()

    decode_data = np.array(decode_data['raw_data']).reshape(1,Ns)

    mset_res = mset_cca.classify(decode_data)
    gcca_res = gcca.classify(decode_data)

    print(max(mset_res, key=mset_res.get), mset_res)
    print(max(gcca_res, key=gcca_res.get), gcca_res)

    return jsonify(msg="successfully received"), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)