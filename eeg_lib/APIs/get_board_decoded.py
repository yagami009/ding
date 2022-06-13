from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route("/decoded", methods=["POST"])
def collect_data():
    data = request.get_json(force=True)
    if isinstance(data, str):
        data = json.loads(data)
    if data is not None:
        print(data)
    
    return jsonify(msg="data collected"), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)