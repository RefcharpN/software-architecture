import redis
from faker import Faker
import string
import random

redis = redis.Redis(
     host= 'localhost',
     port= '6379')

# def record_book():
#      first_part = ''.join(random.choice(string.digits) for _ in range(2))
#      first_part += first_part.join(random.choice(string.ascii_uppercase) for _ in range(1))
#      sec_pasrt = ''.join(random.choice(string.digits) for _ in range(4))
#      return first_part+sec_pasrt

def get_stud_code():
     return random.randint(1000,9999)

fake = Faker('ru_RU')
for _ in range(10):
     redis.set(get_stud_code(), fake.name())
     print("success create")