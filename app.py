from flask import (
    Flask,
    jsonify,
    request
)
from flask_pymongo import PyMongo
import pdb

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

if __name__ == '__main__':
    app.run(debug=True)
