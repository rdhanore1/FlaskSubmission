# 2. Create a form on the frontend that, when submitted, inserts data into MongoDB Atlas.
# Upon successful submission, the user should be redirected to another page displaying the message "Data submitted successfully".
# If there's an error during submission, display the error on the same page without redirection.

# Note:
# 1. Replace "your_mongodb_atlas_connection_string", "your_database_name", and "your_collection_name" with your actual MongoDB Atlas connection details.
# 2. To run the application, use the command below from this directory:
#    python FlaskDemo1.py
# 3. Then access the form at: http://localhost:5000/
# 4. Upon submission, you will be redirected to a success page or see an error message on the same page if there was an issue.

from flask import Flask, request, redirect, url_for, render_template_string
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import os

app = Flask(__name__)
# MongoDB Atlas connection string, database, and collection from environment variables
MONGO_URI = os.environ.get("MONGO_URI")
DB_NAME = os.environ.get("DB_NAME")
COLLECTION_NAME = os.environ.get("COLLECTION_NAME")

missing_config = None
if not MONGO_URI or not DB_NAME or not COLLECTION_NAME:
    missing_config = "MongoDB configuration missing. Please set MONGO_URI, DB_NAME, and COLLECTION_NAME as environment variables."

mongo_error = None
collection = None
if not missing_config:
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.server_info()  # Force connection on startup
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
    except Exception as e:
        mongo_error = f"MongoDB connection error: {str(e)}"

FORM_HTML = '''
<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Data Submission Form</title>
    </head>
    <body>
        <h1>Submit Data</h1>
        {% if error %}
            <p style="color:red;">{{ error }}</p>
        {% endif %}
        {% if mongo_error %}
            <p style="color:red;">{{ mongo_error }}</p>
        {% endif %}
        {% if missing_config %}
            <p style="color:red;">{{ missing_config }}</p>
        {% endif %}
        <form method="post" action="/">
            <label for="data">Data:</label>
            <input type="text" id="data" name="data" required>
            <input type="submit" value="Submit">
        </form>
    </body>
</html>
'''
SUCCESS_HTML = '''
<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Success</title>
    </head>
    <body>
        <h1>Data submitted successfully</h1>
    </body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def submit_data():
    global mongo_error, missing_config
    if request.method == 'POST':
        if missing_config:
            return render_template_string(FORM_HTML, error=None, mongo_error=None, missing_config=missing_config)
        if mongo_error:
            return render_template_string(FORM_HTML, error=None, mongo_error=mongo_error, missing_config=None)
        data = request.form.get('data', '').strip()
        if not data:
            return render_template_string(FORM_HTML, error="Data field cannot be empty.", mongo_error=None, missing_config=None)
        try:
            collection.insert_one({'data': data})
            return redirect(url_for('success'))
        except PyMongoError as e:
            error_message = f"An error occurred: {str(e)}"
            return render_template_string(FORM_HTML, error=error_message, mongo_error=None, missing_config=None)
    return render_template_string(FORM_HTML, error=None, mongo_error=mongo_error, missing_config=missing_config)

@app.route('/success')
def success():
    return render_template_string(SUCCESS_HTML)

if __name__ == '__main__':
    app.run(debug=True)

# Ensure you run this script with the same Python interpreter where you installed pymongo.
# If you still see 'unresolved reference' errors, check your IDE's interpreter settings or run 'python -m pip install pymongo' with the correct python.
