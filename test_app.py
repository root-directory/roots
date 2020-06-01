import pytest
import requests
from app import app

def test_get_one_user():
    response = requests.get("https://root-directory-server.herokuapp.com/api/v1/users/5ed2a8ad338bcf64692b07ac")
    expected = {
        "id":"5ed2a8ad338bcf64692b07ac",
        "timestamp":1590863754003,
        "userName":"Default"
        }
    assert response.status_code == 200
    assert response.headers['Content-Type'] == "application/json"
    assert response.json() == expected

def test_get_user_plants():
    response = requests.get("https://root-directory-server.herokuapp.com/api/v1/users/5ed2a8ad338bcf64692b07ac/plants")
    expected = {
          "plants": [
            {
              "care": {
                "notes": "I'm upset that you don't have pH so... I guess I'll write it here.",
                "soil": {
                  "last": "2020-05-28T20:22:51.215Z",
                  "notes": "Sand is best for this type",
                  "type": "sand"
                },
                "sunlight": {
                  "direction": "west",
                  "duration": 8,
                  "notes": "Second floor bedroom window works best"
                },
                "watering": {
                  "frequency": 7,
                  "last": "2020-06-28T20:22:51.215Z",
                  "notes": "Should be watered with about 8oz"
                }
              },
              "id": "5ed2aecbbe7270109dad3dd6",
              "imageURL": "https://hips.hearstapps.com/vader-prod.s3.amazonaws.com/1557179245-the-sill-houseplant-zz-plant-1-6-014-2230x-progressive-1557179231.jpg",
              "plantName": "Phineas",
              "plantType": "Common Fern",
              "userId": "5ed2a8ad338bcf64692b07ac"
            },
            {
              "care": {
                "notes": "I love this plant",
                "soil": {
                  "last": "2020-05-28T20:22:51.215Z",
                  "notes": "make sure it has drainage",
                  "type": "standard potting mix"
                },
                "sunlight": {
                  "direction": "west",
                  "duration": 7,
                  "notes": "Keep as close to window as possible needs lots of light"
                },
                "watering": {
                  "frequency": 7,
                  "last": "2020-06-28T20:22:51.215Z",
                  "notes": "It should be watered through once a week"
                }
              },
              "id": "5ed2af46be7270109dad3dd7",
              "imageURL": "https://hips.hearstapps.com/vader-prod.s3.amazonaws.com/1557179245-the-sill-houseplant-zz-plant-1-6-014-2230x-progressive-1557179231.jpg",
              "plantName": "Favorite plant",
              "plantType": "Rubber Tree",
              "userId": "5ed2a8ad338bcf64692b07ac"
            }
          ]
        }
    assert response.status_code == 200
    assert response.headers['Content-Type'] == "application/json"
    assert response.json() == expected

def test_get_one_plant():
    response = requests.get("https://root-directory-server.herokuapp.com/api/v1/users/5ed2a8ad338bcf64692b07ac/plants/5ed2af46be7270109dad3dd7")
    expected = {
          "plant": {
            "care": {
              "notes": "I love this plant",
              "soil": {
                "last": "2020-05-28T20:22:51.215Z",
                "notes": "make sure it has drainage",
                "type": "standard potting mix"
              },
              "sunlight": {
                "direction": "west",
                "duration": 7,
                "notes": "Keep as close to window as possible needs lots of light"
              },
              "watering": {
                "frequency": 7,
                "last": "2020-06-28T20:22:51.215Z",
                "notes": "It should be watered through once a week"
              }
            },
            "id": "5ed2af46be7270109dad3dd7",
            "imageURL": "https://hips.hearstapps.com/vader-prod.s3.amazonaws.com/1557179245-the-sill-houseplant-zz-plant-1-6-014-2230x-progressive-1557179231.jpg",
            "plantName": "Favorite plant",
            "plantType": "Rubber Tree",
            "timestamp": 1590865734298,
            "userId": "5ed2a8ad338bcf64692b07ac"
          }
        }
    assert response.status_code == 200
    assert response.headers['Content-Type'] == "application/json"
    assert response.json() == expected

def test_get_journal_entry():
    response = requests.get("https://root-directory-server.herokuapp.com/api/v1/users/5ed2a8ad338bcf64692b07ac/plants/5ed2af46be7270109dad3dd7/journal/5ed2b6c6100aa90e61c45e05")
    expected = {
          "entryType": "image",
          "id": "5ed2b6c6100aa90e61c45e05",
          "info": {
            "imageURL": "https://hips.hearstapps.com/vader-prod.s3.amazonaws.com/1557179245-the-sill-houseplant-zz-plant-1-6-014-2230x-progressive-1557179231.jpg",
            "notes": "Phineas seems to be enjoying the extra sunlight in his new spot!"
          },
          "plantId": "5ed2af46be7270109dad3dd7",
          "timestamp": 1590867654664
        }
    assert response.status_code == 200
    assert response.headers['Content-Type'] == "application/json"
    assert response.json() == expected

def test_get_plant_journal():
    response = requests.get("https://root-directory-server.herokuapp.com/api/v1/users/5ed2a8ad338bcf64692b07ac/plants/5ed2af46be7270109dad3dd7/journal")
    expected = {
  "journalEntries": [
            {
              "entryType": "image",
              "id": "5ed2b6c6100aa90e61c45e05",
              "info": {
                "imageURL": "https://hips.hearstapps.com/vader-prod.s3.amazonaws.com/1557179245-the-sill-houseplant-zz-plant-1-6-014-2230x-progressive-1557179231.jpg",
                "notes": "Phineas seems to be enjoying the extra sunlight in his new spot!"
              },
              "plantId": "5ed2af46be7270109dad3dd7",
              "timestamp": 1590867654664
            },
            {
              "entryType": "water",
              "id": "5ed2bbb900f41d88ad5c91c0",
              "info": {
                "notes": "test # 2"
              },
              "plantId": "5ed2af46be7270109dad3dd7",
              "timestamp": 1590868921508
            }
          ]
        }
    assert response.status_code == 200
    assert response.headers['Content-Type'] == "application/json"
    assert response.json() == expected
