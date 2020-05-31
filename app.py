from flask import (
    Flask,
    jsonify,
    request,
)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import requests
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['MONGO_DBNAME'] = 'root_directory'
app.config['MONGO_URI'] = 'mongodb+srv://admin:OeMp96cSKTBrjtFz@cluster0-anyov.mongodb.net/root_directory?retryWrites=true&w=majority'
mongo = PyMongo(app)

@app.route('/api/v1/users/<string:user_id>', methods=['GET'])
def get_one_user(user_id):
    user = mongo.db.users.find_one_or_404({'_id': user_id})
    response = {
        'id': user['_id'],
        'userName': user['name'],
        'timestamp': user['timestamp']
    }
    return jsonify(response)

@app.route('/api/v1/users/<string:user_id>/plants', methods=['GET'])
def get_user_plants(user_id):
    user = mongo.db.users.find_one_or_404({'_id': user_id})
    user_plants = mongo.db.plants.find({'user_id': user_id})
    format_plant = lambda plant: {
        'id': plant['_id'],
        'userId': plant['user_id'],
        'plantName': plant['plant_name'],
        'plantType': plant['plant_type'],
        'imageURL': plant['image_url'],
        'care': plant['care']
    }
    response = list(map(format_plant, list(user_plants)))
    return jsonify({'plants': response})

@app.route('/api/v1/users/<string:user_id>/plants/<string:plant_id>', methods=['GET'])
def get_one_plant(user_id, plant_id):
    user = mongo.db.users.find_one_or_404({'_id': user_id})
    plant = mongo.db.plants.find_one_or_404({'_id': plant_id})
    response = {
        'id': plant_id,
        'userId': user_id,
        'plantName': plant['plant_name'],
        'plantType': plant['plant_type'],
        'timestamp': plant['timestamp'],
        'imageURL': plant['image_url'],
        'care': plant['care']
    }
    return jsonify({'plant': response})

@app.route('/api/v1/users/<string:user_id>/plants', methods=['POST'])
def create_plant(user_id):
    user = mongo.db.users.find_one_or_404({'_id': user_id})
    timestamp = int(datetime.now().timestamp() * 1000)
    plant = {
        '_id': str(ObjectId()),
        'user_id': user_id,
        'plant_name': request.json.get('plantName', ''),
        'plant_type': request.json.get('plantType', ''),
        'timestamp': timestamp,
        'image_url': request.json.get('imageURL', ''),
        'care': request.json.get('care', {})
    }
    mongo.db.plants.insert_one(plant)
    return jsonify(plant)

@app.route('/api/v1/users/<string:user_id>/plants/<string:plant_id>', methods=['DELETE'])
def delete_plant(user_id, plant_id):
    user = mongo.db.users.find_one_or_404({'_id': user_id})
    plant = mongo.db.plants.find_one_or_404({'_id': plant_id})
    mongo.db.plants.delete_one({'_id': plant_id})
    return jsonify(plant)

@app.route('/api/v1/users/<string:user_id>/plants/<string:plant_id>', methods=['PATCH'])
def update_plant(user_id, plant_id):
    user = mongo.db.users.find_one_or_404({'_id': user_id})
    plant = mongo.db.plants.find_one_or_404({'_id': plant_id})
    mongo.db.plants.update_one({'_id': plant_id}, {'$set': request.json})
    updated_plant = mongo.db.plants.find_one({'_id': plant_id})
    return jsonify(updated_plant)

@app.route('/api/v1/photos', methods=['POST'])
def create_photo():
    headers = {'Content-Type': 'application/jpg'}
    files = request.files['file']
    r = requests.post('https://2ku6am910d.execute-api.us-west-1.amazonaws.com/v1/post-json/upload', headers=headers, data=files)
    if r.status_code == 200:
        timestamp = int(datetime.now().timestamp() * 1000)
        photo = {
            '_id': str(ObjectId()),
            'timestamp': timestamp,
            'photo_url': r.json()['body']
        }
        mongo.db.photos.insert_one(photo)
        return jsonify(photo)
    return jsonify({'error': 'Failed to upload'})

@app.route('/api/v1/users/<string:user_id>/plants/<string:plant_id>/journal', methods=['POST'])
def create_journal_entry(user_id, plant_id):
    user = mongo.db.users.find_one_or_404({'_id': user_id})
    plant = mongo.db.plants.find_one_or_404({'_id': plant_id})
    timestamp = int(datetime.now().timestamp() * 1000)
    journal_entry = {
        '_id': str(ObjectId()),
        'plant_id': plant_id,
        'entry_type': request.json.get('entryType', ''),
        'timestamp': timestamp,
        'info': request.json.get('info', ''),
    }
    mongo.db.journal.insert_one(journal_entry)
    return jsonify(journal_entry)

@app.route('/api/v1/users/<string:user_id>/plants/<string:plant_id>/journal/<string:journal_id>', methods=['GET'])
def get_journal_entry(user_id, plant_id, journal_id):
    user = mongo.db.users.find_one_or_404({'_id': user_id})
    plant = mongo.db.plants.find_one_or_404({'_id': plant_id})
    journal = mongo.db.journal.find_one_or_404({'_id': journal_id})
    journal_entry = {
        'id': journal['_id'],
        'plantId': plant_id,
        'entryType': journal['entry_type'],
        'timestamp': journal['timestamp'],
        'info': journal['info'],
    }
    return jsonify(journal_entry)

@app.route('/api/v1/users/<string:user_id>/plants/<string:plant_id>/journal', methods=['GET'])
def get_plant_journal(user_id, plant_id):
    user = mongo.db.users.find_one_or_404({'_id': user_id})
    plant = mongo.db.plants.find_one_or_404({'_id': plant_id})
    plant_journal = mongo.db.journal.find({'plant_id': plant_id})
    format_journal = lambda journal: {
        'id': journal['_id'],
        'plantId': plant_id,
        'entryType': journal['entry_type'],
        'timestamp': journal['timestamp'],
        'info': journal['info'],
    }
    response = list(map(format_journal, list(plant_journal)))
    return jsonify({'journalEntries': response})

@app.route('/api/v1/users/<string:user_id>/plants/<string:plant_id>/journal/<string:journal_id>', methods=['DELETE'])
def delete_journal(user_id, plant_id, journal_id):
    user = mongo.db.users.find_one_or_404({'_id': user_id})
    plant = mongo.db.plants.find_one_or_404({'_id': plant_id})
    journal = mongo.db.journal.find_one_or_404({'_id': journal_id})
    mongo.db.journal.delete_one({'_id': journal_id})
    return jsonify(journal)

@app.route('/api/v1/users/<string:user_id>/plants/<string:plant_id>/journal/<string:journal_id>', methods=['PATCH'])
def update_journal(user_id, plant_id, journal_id):
    user = mongo.db.users.find_one_or_404({'_id': user_id})
    plant = mongo.db.plants.find_one_or_404({'_id': plant_id})
    journal = mongo.db.journal.find_one_or_404({'_id': journal_id})
    mongo.db.journal.update_one({'_id': journal_id}, {'$set': {'info': {'notes': request.json.get('notes', journal['info']['notes'])}}})
    updated_journal = mongo.db.journal.find_one({'_id': journal_id})
    return jsonify(updated_journal)

if __name__ == '__main__':
    app.run(debug=True)
