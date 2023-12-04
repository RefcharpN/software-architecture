from pymongo import MongoClient

client = MongoClient('localhost',27017)

db = client.university
col = db.groups

update_group  = { "name":input("Группа >")}
new_values = { "$set": { "name": input("назв. группы> "), "cathedra": input("назв. кафедры> "), "course": input("№ курса> ")} }

try:
    db.groups.update_one(update_group,new_values)
except:
    print("Not found!")