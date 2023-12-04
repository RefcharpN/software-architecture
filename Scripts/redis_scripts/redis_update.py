import redis

redis = redis.Redis(
     host= 'localhost',
     port= '6379')

key = input("key = ")
new_value = input("new FIO > ")
try:
    redis.getset(key, new_value)
    print(redis.get(key).decode())
except:
    print("Error")