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

# Sample data to be stored in data.json:
# [
#     {"id": 1, "name": "Item 1"},
#     {"id": 2, "name": "Item 2"},
#     {"id": 3, "name": "Item 3"}
# ]
# Save the above JSON data in a file named data.json in the same directory as this script
# before running the Flask application.
# To run the application, use the command below from this directory:
#   python FlaskDemo.py
# Or, if you are in a different directory, use the full path:
#   python D:\PythonAssignment\AssignmentSubmission\FlaskAssignment\FlaskProject\FlaskDemo.py
# Then access the API at: http://localhost:5000/api
# If you get an empty list, make sure data.json exists and is valid JSON.
# If you run from a different working directory, the script will still find data.json correctly.
