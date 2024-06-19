import os
from flask import Flask, Response, request, jsonify, make_response
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId

load_dotenv()

app = Flask(__name__)
mongo_db_url = os.getenv("MONGO_DB_URL")

client = MongoClient(mongo_db_url)
db = client['JuneCore']
students_collection = db['students']  # Ensure this is the correct collection name

@app.route("/api/students", methods=["GET"])
def get_students():
    user_id = request.args.get('userID')
    filter = {} if user_id is None else {"userID": user_id}
    students = list(students_collection.find(filter))

    response = Response(
        response=dumps(students), status=200, mimetype="application/json")
    return response



@app.route("/api/students", methods=["POST"])
def add_student():
    _json = request.json
    students_collection.insert_one(_json)

    resp = jsonify({"message": "Student added successfully"})
    resp.status_code = 200
    return resp

@app.route("/api/students/<id>", methods=["DELETE"])
def delete_student(id):
    students_collection.delete_one({'_id': ObjectId(id)})

    resp = jsonify({"message": "Student deleted successfully"})
    resp.status_code = 200
    return resp 

@app.route("/api/students/<id>", methods=["PUT"])
def update_student(id):
    _json = request.json
    students_collection.update_one({'_id': ObjectId(id)}, {"$set": _json})

    resp = jsonify({"message": "Student updated successfully"})
    resp.status_code = 200
    return resp

if __name__ == "__main__":
    app.run(debug=True)


@app.errorhandler(400)
def handle_400_error(error):
    return make_response(jsonify({
        "errorCode": error.code, 
        "errorDescription": "Bad request!",
        "errorDetailedDescription": error.description,
        "errorName": error.name
    }), 400)

@app.errorhandler(404)
def handle_404_error(error):
    return make_response(jsonify({
        "errorCode": error.code, 
        "errorDescription": "Resource not found!",
        "errorDetailedDescription": error.description,
        "errorName": error.name
    }), 404)

@app.errorhandler(500)
def handle_500_error(error):
    return make_response(jsonify({
        "errorCode": error.code, 
        "errorDescription": "Internal Server Error",
        "errorDetailedDescription": error.description,
        "errorName": error.name
    }), 500)

if __name__ == "__main__":
    app.run(debug=True)