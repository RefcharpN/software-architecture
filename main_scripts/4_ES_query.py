from elasticsearch import Elasticsearch, helpers
import psycopg2
import random

file = open("./lecture_text/random_text.txt", "r")
texts = file.readlines()


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

#4 в ES таблица Materials
kolvo_materials = 100
get_array_lecture_id = "SELECT array_agg(id) FROM public.lecture"
cursor.execute(get_array_lecture_id)
array_lecture_ids=cursor.fetchall()

def get_lecture_id():
    l_id = random.randint(0,len(array_lecture_ids[0][0])-1)
    lecture_id = array_lecture_ids[0][0][l_id]
    return lecture_id

mappings = {
        "properties": {
            "description": {"type": "text"},
            "lecture_id": {"type": "integer"}
    }
}

index_name = "materialssmelkin"

es = Elasticsearch("http://elastic:2517Pass@10.66.66.1:9200")

try:
    es.indices.create(index="materialssmelkin", mappings=mappings)
except:
    print("index materials exists")

docs = []
try:
    for i in range(kolvo_materials):
        docs.append({
            'description': random.choice(texts),
            'lecture_id' : get_lecture_id()
        })
    helpers.bulk(es, docs, index=index_name)
except Exception as err:
    print("Error in creating docs in ES (materials)!!! ", err)

print("ES fill")