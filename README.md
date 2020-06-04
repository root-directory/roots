# Roots

## Background and Description
Roots is the backend API for our capstone project Root-Directory. Root-Directory is an app to track plant care schedules and growth by uploading pictures and care events such as waterings to a timeline. 

production link: https://root-directory-server.herokuapp.com/api/v1/users/5ed2a8ad338bcf64692b07ac/plants

## Tech Stack
Python<br>
Flask<br>
MongoDB<br>
AWS S3<br>
Unittest<br>
TravisCI<br>

## Key Learnings
* This was our first time using any of these technologies in building out an API.
* One specific learning was using a document database. 

## Implementation Instructions

Clone down this repository `git clone git@github.com:root-directory/roots.git`<br />
Run `python3 -m venv env` to setup your virtual environment. If you don't have venv already installed run `python3 -m pip install --user virtualenv` first.<br />
Run `pip3 install -r requirements.txt` to download all necessary dependencies.<br />
Run `python3.8 app.py` to start up your local server on localhost:5000.<br />
Use your browser or postman to make any of the api calls outlined below.<br />

### Endpoints
  
  #### &nbsp;&nbsp;User: <br /><br />
   &nbsp;&nbsp;&nbsp;&nbsp;GET api/v1/users/<user_id><br />
    
  
  <pre><code> {
  "id": "5ed2a8ad338bcf64692b07ac",
  "timestamp": 1590863754003,
  "userName": "Samantha"
    }</pre></code><br /><br />
  
   #### &nbsp;&nbsp;Plant: <br /><br />
  &nbsp;&nbsp;&nbsp;&nbsp;POST Plant api/v1/users/<user_id>/plants<br />
  <pre><code>{
  "_id": "5ed667d318aac0a977b05d23",
  "care": {
    "notes": "its crawling up a trellance at my house",
    "soil": {
      "last": "2020-05-28T20:22:51.215Z",
      "notes": "drainage is best",
      "type": "potting soil"
    },
    "sunlight": {
      "direction": "south",
      "duration": 8,
      "notes": "likes more light if it can have it"
    },
    "watering": {
      "frequency": 7,
      "last": "2020-06-28T20:22:51.215Z",
      "notes": "let it dry out between waterings"
    }
  },
  "image_url": "htto://first_photo",
  "plant_name": "crawler",
  "plant_type": "silver pothos",
  "timestamp": 1591109587777,
  "user_id": "5ed2a8ad338bcf64692b07ac"
}</pre></code><br /><br /><br />

   &nbsp;&nbsp;&nbsp;&nbsp;GET Plant api/v1/users/<user_id>/plants/<plant_id><br />
    
   <pre><code>{
  "plant": {
    "care": {
      "notes": "its crawling up a trellance at my house",
      "soil": {
        "last": "2020-05-28T20:22:51.215Z",
        "notes": "drainage is best",
        "type": "potting soil"
      },
      "sunlight": {
        "direction": "south",
        "duration": 8,
        "notes": "likes more light if it can have it"
      },
      "watering": {
        "frequency": 7,
        "last": "2020-06-28T20:22:51.215Z",
        "notes": "let it dry out between waterings"
      }
    },
    "id": "5ed667d318aac0a977b05d23",
    "imageURL": "http://second_URL",
    "plantName": "crawler",
    "plantType": "silver pothos",
    "timestamp": 1591109587777,
    "userId": "5ed2a8ad338bcf64692b07ac"
  }
}
</pre></code><br /><br /><br />

&nbsp;&nbsp;&nbsp;&nbsp;GET Plants api/v1/users/<user_id>/plants<br />
    
   <pre><code>{
    "plants": [
        {
            "care": {
                "soil": {
                    "last": "",
                    "notes": "",
                    "type": ""
                },
                "sunlight": {
                    "direction": "",
                    "duration": "",
                    "notes": ""
                },
                "watering": {
                    "frequency": "3",
                    "last": "",
                    "notes": ""
                }
            },
            "id": "5ed8163ae895dac0bc1361fa",
            "imageURL": "https://cassie-test-bucket123.s3-us-west-1.amazonaws.com/1591219769180863.jpg",
            "plantName": "Wakachaka",
            "plantType": "",
            "userId": "5ed2a8ad338bcf64692b07ac"
        }
    ]
}
</pre></code><br /><br /><br />

&nbsp;&nbsp;&nbsp;&nbsp;POST Plant api/v1/users/<user_id>/plants<br />
    
   <pre><code>{
  "plant": {
    "care": {
      "notes": "its crawling up a trellance at my house",
      "soil": {
        "last": "2020-05-28T20:22:51.215Z",
        "notes": "drainage is best",
        "type": "potting soil"
      },
      "sunlight": {
        "direction": "south",
        "duration": 8,
        "notes": "likes more light if it can have it"
      },
      "watering": {
        "frequency": 7,
        "last": "2020-06-28T20:22:51.215Z",
        "notes": "let it dry out between waterings"
      }
    },
    "id": "5ed667d318aac0a977b05d23",
    "imageURL": "http://second_URL",
    "plantName": "crawler",
    "plantType": "silver pothos",
    "timestamp": 1591109587777,
    "userId": "5ed2a8ad338bcf64692b07ac"
  }
}
</pre></code><br /><br /><br />

&nbsp;&nbsp;&nbsp;&nbsp;PATCH Plant api/v1/users/<user_id>/plants/<plant_id><br />
    
   <pre><code>{
  "plant": {
    "care": {
      "notes": "its crawling up a trellance at my house",
      "soil": {
        "last": "2020-05-28T20:22:51.215Z",
        "notes": "drainage is best",
        "type": "potting soil"
      },
      "sunlight": {
        "direction": "south",
        "duration": 8,
        "notes": "likes more light if it can have it"
      },
      "watering": {
        "frequency": 7,
        "last": "2020-06-28T20:22:51.215Z",
        "notes": "let it dry out between waterings"
      }
    },
    "id": "5ed667d318aac0a977b05d23",
    "imageURL": "http://second_URL",
    "plantName": "crawler",
    "plantType": "satin pothos",
    "timestamp": 1591109587777,
    "userId": "5ed2a8ad338bcf64692b07ac"
  }
}
</pre></code><br /><br /><br />

&nbsp;&nbsp;&nbsp;&nbsp;DELETE Plant api/v1/users/<user_id>/plants/<plant_id><br />
    
   <pre><code>{
  "plant": {
    "care": {
      "notes": "its crawling up a trellance at my house",
      "soil": {
        "last": "2020-05-28T20:22:51.215Z",
        "notes": "drainage is best",
        "type": "potting soil"
      },
      "sunlight": {
        "direction": "south",
        "duration": 8,
        "notes": "likes more light if it can have it"
      },
      "watering": {
        "frequency": 7,
        "last": "2020-06-28T20:22:51.215Z",
        "notes": "let it dry out between waterings"
      }
    },
    "id": "5ed667d318aac0a977b05d23",
    "imageURL": "http://second_URL",
    "plantName": "crawler",
    "plantType": "satin pothos",
    "timestamp": 1591109587777,
    "userId": "5ed2a8ad338bcf64692b07ac"
  }
}
</pre></code><br /><br /><br />

#### &nbsp;&nbsp;Journal: <br /><br />
&nbsp;&nbsp;&nbsp;&nbsp;POST Journal api/v1/users/<user_id>/plants/<plant_id>/journal<br />

  <pre><code>{
  "_id": "5ed667e718aac0a977b05d25",
  "entry_type": "image",
  "info": {
    "imageURL": "http://second_URL",
    "notes": "A new image"
  },
  "plant_id": "5ed667d318aac0a977b05d23",
  "timestamp": 1591109607616
}</pre></code>
  
   &nbsp;&nbsp;&nbsp;&nbsp;GET Journal api/v1/users/<user_id>/plants/<plant_id>/journal/<journal_id><br />
    
   <pre><code>{
  "entryType": "",
  "id": "5ed52b52b310cf4990e32a81",
  "info": {
    "imgUrl": "",
    "notes": "hjkl"
  },
  "plantId": "5ed2af46be7270109dad3dd7",
  "timestamp": 1591028562338
}
    </pre></code><br /><br /><br />
    
  &nbsp;&nbsp;&nbsp;&nbsp;GET All Journal Entries api/v1/users/<user_id>/plants/<plant_id>/journal<br />
  
  <pre><code>
  {
  "journalEntries": [
    {
      "entryType": "image",
      "id": "5ed667d318aac0a977b05d24",
      "info": {
        "imageURL": "htto://first_photo",
        "notes": "Plant added to garden!"
      },
      "plantId": "5ed667d318aac0a977b05d23",
      "timestamp": 1591109587777
    },
    {
      "entryType": "image",
      "id": "5ed667e718aac0a977b05d25",
      "info": {
        "imageURL": "http://second_URL",
        "notes": "A new image"
      },
      "plantId": "5ed667d318aac0a977b05d23",
      "timestamp": 1591109607616
    }
  ]
}

</pre></code><br /><br /><br />
  
  &nbsp;&nbsp;&nbsp;&nbsp;PATCH Journal Entry /api/v1/users/<user_id>/plants/<plant_id>/journal/<journal_id><br />
  
  <pre><code>{
  "entryType": "image",
  "id": "5ed52b52b310cf4990e32a81",
  "info": {
    "imgUrl": "http://real_url",
    "notes": "Look how much its grown!"
  },
  "plantId": "5ed2af46be7270109dad3dd7",
  "timestamp": 1591028562338
}</pre></code><br /><br /><br />

</pre></code><br /><br /><br />
  
  &nbsp;&nbsp;&nbsp;&nbsp;DELETE Journal Entry api/v1/users/<user_id>/plants/<plant_id>/journal/<journal_id><br />
  
  <pre><code>{
  "entryType": "",
  "id": "5ed52b52b310cf4990e32a81",
  "info": {
    "imgUrl": "",
    "notes": "hjkl"
  },
  "plantId": "5ed2af46be7270109dad3dd7",
  "timestamp": 1591028562338
}</pre></code><br /><br /><br />
 
