import unittest
from flask_pymongo import PyMongo
from app import app

class TestFlaskCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client(self)
        self.mongo = PyMongo(app)

    def tearDown(self):
        self.mongo.db.plants.drop()
        self.mongo.db.journal.drop()
        self.mongo.db.photos.drop()

    def test_get_one_user(self):
        expected = {
            'id': '5e12g4a',
            'userName': 'test user',
            'timestamp': 1590863754003
        }
        result = self.app.get('/api/v1/users/5e12g4a')
        self.assertEqual(result.json, expected)

    def test_get_user_plants(self):
        plant = {
            '_id': '5e12g5c',
            'user_id': '5e12g4a',
            'plant_name': 'Bob',
            'plant_type': 'snakeplant',
            'timestamp': 1590863754003,
            'image_url': 'www.aws.com/s3/image.jpg',
            'care': {}
        }
        self.mongo.db.plants.insert_one(plant)
        result = self.app.get('/api/v1/users/5e12g4a/plants')
        self.assertEqual(result.json['plants'][0]['id'], plant['_id'])

    def test_create_plant(self):
        plant = {
            'plantName': 'Bob',
            'plantType': 'snakeplant',
            'imageURL': 'www.aws.com/s3/image.jpg',
            'care': {
                'notes': 'Low maintenance'
            }
        }
        response = self.app.post(
            '/api/v1/users/5e12g4a/plants',
            json=plant
        )
        result = self.mongo.db.plants.find_one({'user_id': '5e12g4a'})
        self.assertEqual(response.json['plant_name'], 'Bob')
        self.assertEqual(result['plant_name'], 'Bob')

    def test_update_plant(self):
        plant_doc = {
            '_id': '5e12g5c',
            'user_id': '5e12g4a',
            'plant_name': 'Bob',
            'plant_type': 'snakeplant',
            'timestamp': 1590863754003,
            'image_url': 'www.aws.com/s3/image.jpg',
            'care': {}
        }
        patch_request = {
            'plant_name': 'Robert'
        }
        self.mongo.db.plants.insert_one(plant_doc)
        response = self.app.patch(
            '/api/v1/users/5e12g4a/plants/5e12g5c',
            json=patch_request
        )
        result = self.mongo.db.plants.find_one({'_id': '5e12g5c'})
        self.assertEqual(response.json['plant_name'], 'Robert')
        self.assertEqual(result['plant_name'], 'Robert')

    def test_delete_plant(self):
        plant_doc = {
            '_id': '5e12g5c',
            'user_id': '5e12g4a',
            'plant_name': 'Bob',
            'plant_type': 'snakeplant',
            'timestamp': 1590863754003,
            'image_url': 'www.aws.com/s3/image.jpg',
            'care': {}
        }
        self.mongo.db.plants.insert_one(plant_doc)
        plant = self.mongo.db.plants.find_one({'_id': '5e12g5c'})
        self.assertEqual(plant['plant_name'], 'Bob')
        response = self.app.delete('/api/v1/users/5e12g4a/plants/5e12g5c')
        db = list(self.mongo.db.plants.find())
        self.assertEqual(response.json['plant_name'], 'Bob')
        self.assertEqual(len(db), 0)

if __name__ == '__main__':
    unittest.main()
