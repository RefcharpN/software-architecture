import redis

redis = redis.Redis(
     host= 'localhost',
     port= '6379')

# key = input("key for delete > ")
try:
    keys = redis.keys('*')
    print(redis.delete(*keys))
    print("success delete")
except:
    print("Error")