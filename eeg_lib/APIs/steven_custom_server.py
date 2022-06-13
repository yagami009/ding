from flask import Flask, request, jsonify
import json
import sys
import time

app = Flask(__name__)

DEFAULT_FILENAME = r"C:\Users\RISHI\Desktop\FYP\EEG-decoding\eeg_lib\log\newheadset\rishil_test_1_raw.json"

def log_data(payload, filename=None):
    filename = filename or DEFAULT_FILENAME

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=4)

    print(payload)
    print(f"Log file {filename} updated successfully.")

def save_to_txt(payload):
    print(payload)
    f = open("data.txt","a")
    for data in payload["raw_data"]:
        f.write("%d," % data)
    f.write("\n")
    f.close()

@app.route("/", methods=["POST"])
def save_data():
    data = request.get_json(force=True)
    if isinstance(data, str):
        data = json.loads(data)
    if data is not None:
        save_to_txt(data)
        return jsonify(msg="data stored successfully"), 200
    return jsonify(msg="invalid data payload"), 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
