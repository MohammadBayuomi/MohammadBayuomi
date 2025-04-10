from pymongo import MongoClient
client =MongoClient('mongodb://localhost:27017')
db = client['Resturants_Info']
collections = db['Resturants']

all_collection = collections.find({'cuisine':"Bakery"})

for x in all_collection:
    print(x)