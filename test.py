import unittest
from flask_pymongo import PyMongo
from app import app

class TestFlaskCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client(self)
        self.app.application.config['MONGO_DBNAME'] = 'test'
        self.app.application.config['MONGO_URI'] = 'mongodb+srv://admin:OeMp96cSKTBrjtFz@cluster0-anyov.mongodb.net/root_directory_test?retryWrites=true&w=majority'
        self.app.application.mongo = PyMongo(self.app.application)
        self.mongo = self.app.application.mongo

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
        response = self.app.get('/api/v1/users/5e12g4a')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected)

    def test_get_user_plants(self):
        plant = {
            '_id': '5e12g5c',
            'user_id': '5e12g4a',
            'plant_name': 'Bob',
            'plant_type': 'snakeplant',
            'timestamp': 1590863754003,
            'last_watered': 1590863754003,
            'image_url': 'www.aws.com/s3/image.jpg',
            'care': {}
        }
        self.mongo.db.plants.insert_one(plant)
        response = self.app.get('/api/v1/users/5e12g4a/plants')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['plants'][0]['plantName'], plant['plant_name'])

    def test_get_one_plant(self):
        plant = {
            '_id': '5e12g5c',
            'user_id': '5e12g4a',
            'plant_name': 'Bob',
            'plant_type': 'snakeplant',
            'timestamp': 1590863754003,
            'last_watered': 1590863754003,
            'image_url': 'www.aws.com/s3/image.jpg',
            'care': {}
        }
        self.mongo.db.plants.insert_one(plant)
        response = self.app.get('/api/v1/users/5e12g4a/plants/5e12g5c')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['plantName'], plant['plant_name'])

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
        plant_result = self.mongo.db.plants.find_one({'user_id': '5e12g4a'})
        journal_result = self.mongo.db.journal.find_one({'plant_id': plant_result['_id']})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['plant_name'], 'Bob')
        self.assertEqual(plant_result['plant_name'], 'Bob')
        self.assertEqual(journal_result['info']['imageURL'], 'www.aws.com/s3/image.jpg')

    def test_update_plant(self):
        plant_doc = {
            '_id': '5e12g5c',
            'user_id': '5e12g4a',
            'plant_name': 'Bob',
            'plant_type': 'snakeplant',
            'timestamp': 1590863754003,
            'last_watered': 1590863754003,
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
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['plant_name'], 'Robert')
        self.assertEqual(result['plant_name'], 'Robert')

    def test_delete_plant(self):
        plant_doc = {
            '_id': '5e12g5c',
            'user_id': '5e12g4a',
            'plant_name': 'Bob',
            'plant_type': 'snakeplant',
            'timestamp': 1590863754003,
            'last_watered': 1590863754003,
            'image_url': 'www.aws.com/s3/image.jpg',
            'care': {}
        }
        self.mongo.db.plants.insert_one(plant_doc)
        plant = self.mongo.db.plants.find_one({'_id': '5e12g5c'})
        self.assertEqual(plant['plant_name'], 'Bob')

        response = self.app.delete('/api/v1/users/5e12g4a/plants/5e12g5c')
        db = list(self.mongo.db.plants.find())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['plant_name'], 'Bob')
        self.assertEqual(len(db), 0)

    def test_get_plant_journal(self):
        plant_doc = {
            '_id': '5e12g5c',
            'user_id': '5e12g4a',
            'plant_name': 'Bob',
            'plant_type': 'snakeplant',
            'timestamp': 1590863754003,
            'last_watered': 1590863754003,
            'image_url': 'www.aws.com/s3/image.jpg',
            'care': {}
        }
        journal_doc = {
            '_id': '5e12g8f',
            'plant_id': '5e12g5c',
            'timestamp': 1590863754003,
            'entry_type': 'image',
            'info': {
                'imageURL': 'www.aws.com/s3/image.jpg',
                'notes': ''
            }

        }
        self.mongo.db.plants.insert_one(plant_doc)
        self.mongo.db.journal.insert_one(journal_doc)
        response = self.app.get('/api/v1/users/5e12g4a/plants/5e12g5c/journal')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['journalEntries'][0]['info']['imageURL'], 'www.aws.com/s3/image.jpg')

    def test_get_journal_entry(self):
        plant_doc = {
            '_id': '5e12g5c',
            'user_id': '5e12g4a',
            'plant_name': 'Bob',
            'plant_type': 'snakeplant',
            'timestamp': 1590863754003,
            'last_watered': 1590863754003,
            'image_url': 'www.aws.com/s3/image.jpg',
            'care': {}
        }
        journal_doc = {
            '_id': '5e12g8f',
            'plant_id': '5e12g5c',
            'timestamp': 1590863754003,
            'entry_type': 'image',
            'info': {
                'imageURL': 'www.aws.com/s3/image.jpg',
                'notes': ''
            }
        }
        self.mongo.db.plants.insert_one(plant_doc)
        self.mongo.db.journal.insert_one(journal_doc)
        response = self.app.get('/api/v1/users/5e12g4a/plants/5e12g5c/journal/5e12g8f')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['info']['imageURL'], 'www.aws.com/s3/image.jpg')

    def test_create_journal_entry(self):
        plant_doc = {
            '_id': '5e12g5c',
            'user_id': '5e12g4a',
            'plant_name': 'Bob',
            'plant_type': 'snakeplant',
            'timestamp': 1590863754003,
            'last_watered': 1590863754003,
            'image_url': 'www.aws.com/s3/none.jpg',
            'care': {}
        }
        journal_request = {
            'entryType': 'image',
            'info': {
                'imageURL': 'www.aws.com/s3/image.jpg',
                'notes': ''
            }

        }
        self.mongo.db.plants.insert_one(plant_doc)
        plant_before = self.mongo.db.plants.find_one({'_id': '5e12g5c'})
        self.assertEqual(plant_before['image_url'], 'www.aws.com/s3/none.jpg')
        response = self.app.post(
            '/api/v1/users/5e12g4a/plants/5e12g5c/journal',
            json=journal_request
        )
        result = self.mongo.db.journal.find_one({'entry_type': 'image'})
        plant_after = self.mongo.db.plants.find_one({'_id': '5e12g5c'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['info']['imageURL'], 'www.aws.com/s3/image.jpg')
        self.assertEqual(result['info']['imageURL'], 'www.aws.com/s3/image.jpg')
        self.assertEqual(plant_after['image_url'], 'www.aws.com/s3/image.jpg')

    def test_water_plant(self):
        plant_doc = {
            '_id': '5e12g5c',
            'user_id': '5e12g4a',
            'plant_name': 'Bob',
            'plant_type': 'snakeplant',
            'timestamp': 1590863754003,
            'last_watered': 1590863754003,
            'image_url': 'www.aws.com/s3/none.jpg',
            'care': {}
        }
        journal_request = {
            'entryType': 'water',
            'info': {
                'imageURL': '',
                'notes': ''
            }

        }
        self.mongo.db.plants.insert_one(plant_doc)
        plant_before = self.mongo.db.plants.find_one({'_id': '5e12g5c'})
        self.assertEqual(plant_before['last_watered'], 1590863754003)
        response = self.app.post(
            '/api/v1/users/5e12g4a/plants/5e12g5c/journal',
            json=journal_request
        )
        plant_after = self.mongo.db.plants.find_one({'_id': '5e12g5c'})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(plant_after['last_watered'], 1590863754003)

    def test_update_journal(self):
        plant_doc = {
            '_id': '5e12g5c',
            'user_id': '5e12g4a',
            'plant_name': 'Bob',
            'plant_type': 'snakeplant',
            'timestamp': 1590863754003,
            'last_watered': 1590863754003,
            'image_url': 'www.aws.com/s3/image.jpg',
            'care': {}
        }
        journal_doc = {
            '_id': '5e12g8f',
            'plant_id': '5e12g5c',
            'timestamp': 1590863754003,
            'entry_type': 'image',
            'info': {
                'imageURL': 'www.aws.com/s3/image.jpg',
                'notes': ''
            }
        }
        journal_request = {
            'notes': 'Forgot to add a note!'
        }
        self.mongo.db.plants.insert_one(plant_doc)
        self.mongo.db.journal.insert_one(journal_doc)
        journal_before = self.mongo.db.journal.find_one({'_id': '5e12g8f'})
        self.assertEqual(journal_before['info']['notes'], '')
        response = self.app.patch(
            '/api/v1/users/5e12g4a/plants/5e12g5c/journal/5e12g8f',
            json=journal_request
        )
        journal_after = self.mongo.db.journal.find_one({'_id': '5e12g8f'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['info']['notes'], 'Forgot to add a note!')
        self.assertEqual(journal_after['info']['notes'], 'Forgot to add a note!')

    def test_delete_journal(self):
        plant_doc = {
            '_id': '5e12g5c',
            'user_id': '5e12g4a',
            'plant_name': 'Bob',
            'plant_type': 'snakeplant',
            'timestamp': 1590863754003,
            'last_watered': 1590863754003,
            'image_url': 'www.aws.com/s3/image.jpg',
            'care': {}
        }
        journal_doc = {
            '_id': '5e12g8f',
            'plant_id': '5e12g5c',
            'timestamp': 1590863754003,
            'entry_type': 'image',
            'info': {
                'imageURL': 'www.aws.com/s3/image.jpg',
                'notes': ''
            }
        }
        self.mongo.db.plants.insert_one(plant_doc)
        self.mongo.db.journal.insert_one(journal_doc)
        journal = self.mongo.db.journal.find_one({'_id': '5e12g8f'})
        self.assertEqual(journal['plant_id'], '5e12g5c')
        response = self.app.delete('/api/v1/users/5e12g4a/plants/5e12g5c/journal/5e12g8f')
        db = list(self.mongo.db.journal.find())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['plant_id'], '5e12g5c')
        self.assertEqual(len(db), 0)


if __name__ == '__main__':
    unittest.main()
