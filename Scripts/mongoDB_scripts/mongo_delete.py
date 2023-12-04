from pymongo import MongoClient

client = MongoClient('localhost',27017)

db = client.university
col = db.institute


# Удалить все документы из коллекции
try:
   col.delete_many({})
except:
    print("Not found!")
