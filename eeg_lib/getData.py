from flask import Flask, request, jsonify
import json

app = Flask(__name__)

def load_array_data_online(file_path):
    data_file = open(file_path, "r")
    data_file = data_file.read().split(',')            
    values = [float(i) for i in data_file]
    return values

def average_every_n(values, size):
    return [sum(group) / size for group in zip(*[iter(values)]*size)]

blocks = [i for i in range(1,7)]

data = []
data_file_7 = []
data_file_10 = []
data_file_12 = []

for channel in [4,8]:
    
    for block in blocks:
        data_file_7 += average_every_n(load_array_data_online(r"C:\Users\RISHI\Desktop\FYP\EEG-decoding\eeg_lib\log\mnakanishi\8hz\8hz_channel_0{c}_0{b}".format(c=channel,b=block)),5)

    for block in blocks:
        data_file_10 += average_every_n(load_array_data_online(r"C:\Users\RISHI\Desktop\FYP\EEG-decoding\eeg_lib\log\mnakanishi\10hz\10hz_channel_0{c}_0{b}".format(c=channel,b=block)),5)

    for block in blocks:
        data_file_12 += average_every_n(load_array_data_online(r"C:\Users\RISHI\Desktop\FYP\EEG-decoding\eeg_lib\log\mnakanishi\12hz\12hz_channel_0{c}_0{b}".format(c=channel,b=block)),5)

data_file_7_split = []
data_file_10_split = []
data_file_12_split = []

train = 3
count = -1

for i in range(0,len(data_file_7),50):
    data_file_7_split.append(data_file_7[i:i+50])
    data_file_10_split.append(data_file_10[i:i+50])
    data_file_12_split.append(data_file_12[i:i+50])

# split channels POz, Oz
data_file_7_split_1 = data_file_7_split[:30]
data_file_7_split_2 = data_file_7_split[30:]
data_file_10_split_1 = data_file_10_split[:30]
data_file_10_split_2 = data_file_10_split[30:]
data_file_12_split_1 = data_file_12_split[:30]
data_file_12_split_2 = data_file_12_split[30:]

calib_1 = {
            7: data_file_7_split_1[:train],
           10: data_file_10_split_1[:train],
           12: data_file_12_split_1[:train]
          }
calib_2 = {
            7: data_file_7_split_2[:train],
           10: data_file_10_split_2[:train],
           12: data_file_12_split_2[:train]
          }
test_1 = {
            7: data_file_7_split_1[train:],
           10: data_file_10_split_1[train:],
           12: data_file_12_split_1[train:]
          }
test_2 = {
            7: data_file_7_split_2[train:],
           10: data_file_10_split_2[train:],
           12: data_file_12_split_2[train:]
          }


@app.route("/calib_1_7", methods=["GET"])
def calib_7_1():
    return {7: calib_1[7]}, 200

@app.route("/calib_1_10", methods=["GET"])
def calib_10_1():
    return {10: calib_1[10]}, 200
    
@app.route("/calib_1_12", methods=["GET"])
def calib_12_1():
    return {12: calib_1[12]}, 200

@app.route("/test_7_1", methods=["GET"])
def test_7_1():
    count = int(request.args.get('count'))
    return {'test': test_1[7][count]}, 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)