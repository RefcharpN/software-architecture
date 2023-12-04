import redis
from faker import Faker
import string
import random

redis = redis.Redis(
     host= 'localhost',
     port= '6379')

for _ in range(1):
    redis.set(1,"{'student_id':10,'was': true,'date':'11.11.2022'}")
    redis.set(2,"{'student_id':20,'was': false,'date':'11.11.2022'}")