from flask import (
    Flask,
    jsonify,
    request,
)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'root_directory'
app.config['MONGO_URI'] = 'mongodb+srv://admin:OeMp96cSKTBrjtFz@cluster0-anyov.mongodb.net/root_directory?retryWrites=true&w=majority'
mongo = PyMongo(app)

@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    user = mongo.db.users.find_one_or_404({'_id': user_id})
    user_plants = list(mongo.db.plants.find({'user_id': user_id}))
    response = {
        'user_id': user['_id'],
        'user_name': user['name'],
        'plants': user_plants
    }
    return jsonify({'user': response})

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

if __name__ == '__main__':
    app.run(debug=True)
