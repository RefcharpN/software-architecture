# Очистить все таблицы в БД
from pymongo import MongoClient
import psycopg2
import redis
from elasticsearch import Elasticsearch
from neo4j import GraphDatabase


# Монго Удалить все документы из коллекции
CONNECTION_STRING = "mongodb://root:2517Pass@10.66.66.1:27017/?authMechanism=DEFAULT"
client = MongoClient(CONNECTION_STRING)

db = client.smelkin
collection = db.institute

try:
   collection.delete_many({})
   print("1) Mongo clear")
except Exception as err:
    print("Mongo error! ",err)


# Посгрес
database_name = "smelkin"
user_name = "mireaUser"
password = "2517Pass!Ab0ba"
host_ip = "10.66.66.1"
host_port ="5433"

connection = psycopg2.connect(
            database = database_name,
            user = user_name,
            password = password,
            host = host_ip,
            port = host_port
)

connection.autocommit = True
cursor = connection.cursor()
try:
    delete_query = "DROP TABLE public.visits;"
    cursor.execute(delete_query)
    delete_query = "DROP TABLE public.students;"
    cursor.execute(delete_query)
    delete_query = "DROP TABLE  public.\"timeTable\"; "
    cursor.execute(delete_query)
    delete_query = "DROP TABLE  public.group; "
    cursor.execute(delete_query)
    delete_query = "DROP TABLE  public.lecture;"
    cursor.execute(delete_query)
    delete_query = "DROP TABLE  public.disciplines;"
    cursor.execute(delete_query)
    delete_query = "DROP TABLE  public.specialnost; "
    cursor.execute(delete_query)
    delete_query = "DROP TABLE  public.kafedra;"
    cursor.execute(delete_query)
    delete_query = "DROP TABLE  public.institute;"
    cursor.execute(delete_query)
    print('2) Postgres clear')
except Exception as err:
    print("Error in Postgres delete",err)

#Redis
redis = redis.Redis(
     host= '10.66.66.1',
     port= '6379', db=1)

try:
    keys = redis.keys('*')
    redis.delete(*keys)
    print("3) Redis clear")
except Exception as err:
    print("Error in redis delete ", err)

# ES
es = Elasticsearch("http://elastic:2517Pass@10.66.66.1:9200")

try:
    es.indices.delete(index='materialssmelkin')
    print("4) ElasticSearch clear")
except Exception as err:
    print("Error in ES delete!!! ",err)

# Neo
uri = "bolt://10.66.66.1:7687"
userName = "neo4j"
password = "2517Pass"

graphDB_Driver  = GraphDatabase.driver(uri, auth=(userName, password))

#Удалить всё
with graphDB_Driver.session(database="smelkin") as neo_session:
        neo_session.run("MATCH (n) DETACH DELETE n")
        print("5) Neo4J clear")