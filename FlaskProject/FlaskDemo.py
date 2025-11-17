# 1. Create a Flask application with an /api route.
# When this route is accessed, it should return a JSON list.
# The data should be stored in a backend file, read from it, and sent as a response.

from flask import Flask, jsonify
import json
import os

app = Flask(__name__)
# Always use the directory of this script for data.json
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.json')

def read_data_from_file():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            try:
                data = json.load(file)
                return data
            except json.JSONDecodeError:
                return []
    return []

@app.route('/api', methods=['GET'])
def get_data():
    data = read_data_from_file()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
