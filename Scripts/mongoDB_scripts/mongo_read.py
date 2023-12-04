from pymongo import MongoClient

client = MongoClient('localhost',27017)

db = client.university

col = db.institute

try:
    for document in db.institute.find():
        print(document)
except:
    print("Not found!")