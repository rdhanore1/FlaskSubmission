from flask import Flask, request, jsonify
from pymongo import MongoClient
import config

app = Flask(__name__)

# MongoDB connection
client = MongoClient(config.MONGO_URI)
db = client[config.DB_NAME]
todo_collection = db[config.COLLECTION_NAME]

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    data = request.get_json()

    # Validate required fields
    item_name = data.get("itemName")
    item_description = data.get("itemDescription")

    if not item_name:
        return jsonify({"error": "itemName is required"}), 400

    # Create document
    todo_item = {
        "itemName": item_name,
        "itemDescription": item_description
    }

    # Insert into MongoDB
    inserted_id = todo_collection.insert_one(todo_item).inserted_id

    return jsonify({
        "message": "To-Do item stored successfully",
        "id": str(inserted_id),
        "data": todo_item
    }), 201


if __name__ == "__main__":
    app.run(debug=True)
