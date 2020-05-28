from flask import (
    Flask,
    jsonify,
    request,
)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import requests

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'root_directory'
app.config['MONGO_URI'] = 'mongodb+srv://admin:OeMp96cSKTBrjtFz@cluster0-anyov.mongodb.net/root_directory?retryWrites=true&w=majority'
mongo = PyMongo(app)

@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    user = mongo.db.users.find_one_or_404({'_id': user_id})
    response = {
        'user_id': user['_id'],
        'user_name': user['name']
    }
    return jsonify({'user': response})

@app.route('/api/v1/users/<int:user_id>/plants', methods=['GET'])
def get_user_plants(user_id):
    user = mongo.db.users.find_one_or_404({'_id': user_id})
    user_plants = mongo.db.plants.find({'user_id': user_id})
    format_plant = lambda plant: {
        'plant_id': plant['_id'],
        'user_id': plant['user_id'],
        'nickname': plant['nickname'],
        'plant_type': plant['plant_type']
    }
    response = list(map(format_plant, list(user_plants)))
    return jsonify({'plants': response})


@app.route('/api/v1/users/<int:user_id>/plants', methods=['POST'])
def create_plant(user_id):
    user = mongo.db.users.find_one_or_404({'_id': user_id})
    plant = {
        '_id': str(ObjectId()),
        'user_id': user_id,
        'plant_name': request.json.get('plant_name', ''),
        'plant_type': request.json.get('plant_type', '')
    }
    mongo.db.plants.insert_one(plant)
    return jsonify(plant)

@app.route('/api/v1/users/<int:user_id>/plants/<string:plant_id>', methods=['DELETE'])
def delete_plant(user_id, plant_id):
    user = mongo.db.users.find_one_or_404({'_id': user_id})
    plant = mongo.db.plants.find_one_or_404({'_id': plant_id})
    mongo.db.plants.delete_one({'_id': plant_id})
    return jsonify(plant)

@app.route('/api/v1/users/<int:user_id>/plants/<string:plant_id>', methods=['PATCH'])
def update_plant(user_id, plant_id):
    user = mongo.db.users.find_one_or_404({'_id': user_id})
    plant = mongo.db.plants.find_one_or_404({'_id': plant_id})
    mongo.db.plants.update_one({'_id': plant_id}, {'$set': request.json})
    updated_plant = mongo.db.plants.find_one({'_id': plant_id})
    return jsonify(updated_plant)

@app.route('/api/v1/users/<int:user_id>/plants/<int:plant_id>/photos', methods=['POST'])
def create_photo(user_id, plant_id):
    user = mongo.db.users.find_one_or_404({'_id': user_id})
    plant = mongo.db.plants.find_one_or_404({'_id': plant_id})
    headers = {'Content-Type': 'application/pdf'}
    files = {'file': request.files['file']}
    r = requests.post('https://2ku6am910d.execute-api.us-west-1.amazonaws.com/v1/post-json/upload', headers=headers, files=files)
    if r.status_code == 200:
        photo = {
            '_id': str(ObjectId()),
            'plant_id': plant_id,
            'photo_url': r.json()["body"]
        }
        mongo.db.photos.insert_one(photo)
        return jsonify(photo)
    return jsonify({"error": "Failed to upload"})


if __name__ == '__main__':
    app.run(debug=True)
