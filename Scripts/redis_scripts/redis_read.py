from xml.dom import NotFoundErr
import redis

redis = redis.Redis(
     host= 'localhost',
     port= '6379')

key = input("key = ")
try:
     print(redis.get(key).decode())
except:
     print("Not found")