from flask import Flask, request, jsonify
import json
import sys
import time
import numpy as np
import pandas as pd
from cca import GCCA_SSVEP
from cca import MsetCCA_SSVEP

app = Flask(__name__)

DEFAULT_FILENAME = "/Users/rishil/Desktop/FYP/EEG-decoding/eeg_lib/logs/rishil_test_1_raw.json"

stim_freqs = [7,10,12] # stim freqs used
fs = 256 # sampling freq
Ns = 256 # number of sample points to consider
Nh = 1 # number of harmonics for CCA-based algos

cal = [{'7':[]},{'10':[]},{'12':[]}]
pre_cal = {}
proc_calibration = {}

index_pos = dict(zip(["Nc", "Ns", "Nt"], range(3)))

gcca = GCCA_SSVEP(stim_freqs, fs, Nh=Nh)
mset_cca = MsetCCA_SSVEP(stim_freqs)

def write_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def read_json(filename):
    with open(filename) as f:
        return json.load(f)


def log_data(payload, filename=None):

    filename = filename or DEFAULT_FILENAME
    session_id = payload.get("session_id", f"default_session_{int(time.time())}")
    try:
        existing_data = read_json(filename)
    except FileNotFoundError:
        existing_data = {}

    if session_id in existing_data:
        existing_data[session_id].append(payload)
        del payload["session_id"]
    else:
        existing_data[session_id] = [payload]
    write_json(filename, existing_data)
    test(payload)
    print(f"Log file {filename} updated successfully.")

def test(payload):
    print(payload)

@app.route("/", methods=["POST"])
def save_data():
    data = request.get_json(force=True)
    if isinstance(data, str):
        data = json.loads(data)
    if data is not None:
        log_data(data)
        return jsonify(msg="data stored successfully"), 200
    return jsonify(msg="invalid data payload"), 400

@app.route('/7hz', methods=["POST"])
def cal7():
    data = request.get_json(force=True)
    cal[0]['7'].append(data['7'])
    # print(cal[0]['7'])
    print(data)
    return jsonify(msg="successfully received"), 200

@app.route('/10hz', methods=["POST"])
def cal10():
    data = request.get_json(force=True)
    cal[1]['10'].append(data['10'])
    print(data)
    return jsonify(msg="successfully received"), 200

@app.route('/12hz', methods=["POST"])
def cal12():
    data = request.get_json(force=True)
    cal[2]['12'].append(data['12'])
    # print(cal[2]['12'])
    print(data)
    return jsonify(msg="successfully received"), 200

@app.route('/message', methods=["POST"])
def message():
    data = request.get_json(force=True)
    print(data)
    return jsonify(msg="successfully received"), 200

@app.route('/raw', methods=["POST"])
def raw():
    data = request.get_json(force=True)
    # print(cal[2]['12'])
    print(data)
    return jsonify(msg="successfully received"), 200

@app.route('/isCalibrated', methods=["GET"])
def calibrate():
    # print(cal)
    for i in cal:
        for key, value in i.items():
            pre_cal[key] = value
    # print(pre_cal)
    # print(len(pre_cal['7'][0]))
    tests = {
            7: ['7'], 
            10: ['10'], 
            12: ['12']
        }

    for f, test_set in tests.items():
        proc_calibration[f] = []
        
        for test in test_set:
            values = pre_cal[test]
            proc_data = np.array([values[i] for i in range(len(values))])
            proc_calibration[f].append(proc_data[:, :Ns].reshape((1, Ns, -1)))

    # print(proc_calibration)
    # del all_data    

    for f, proc_data in proc_calibration.items():
        if len(proc_data) <= 1:
            proc_calibration[f] = proc_data[0]
        else:
            proc_calibration[f] = np.concatenate([*proc_data], axis=-1) # merge data from across trials
    # print(proc_calibration)
    
    data_tensor = np.array([test_set[:, :, :] for test_set in proc_calibration.values()])

    print("Data tensor shape: ", data_tensor.shape)

    gcca.fit(data_tensor)
    mset_cca.fit(data_tensor)

    # print(data_tensor[0,:,:,0].shape)
    # print(mset_cca.classify(data_tensor[0,:,:,0]))
    return "calibrated", 200

@app.route('/decode', methods=["POST"])
def decoding():
    decode_data = request.get_json(force=True)
    decode_data = np.array(decode_data['raw_data']).reshape(1,Ns)
    # print(decode_data.shape)
    # print(decode_data)

    mset_res = mset_cca.classify(decode_data)
    gcca_res = gcca.classify(decode_data)
    highest_mset = 0
    highest_mset_freq = -1

    for freq, acc in mset_res.items():
            if abs(acc) > highest_mset:
                highest_mset_freq = freq
                highest_mset = abs(acc)

    print(highest_mset_freq, highest_mset)

    highest_gcca = 0
    highest_gcca_freq = -1

    for freq, acc in gcca_res.items():
            if abs(acc) > highest_gcca:
                highest_gcca_freq = freq
                highest_gcca = abs(acc)

    print(highest_gcca_freq, highest_gcca)

    return jsonify(msg="successfully received"), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)