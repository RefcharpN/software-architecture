from elasticsearch import Elasticsearch, helpers
from neo4j import GraphDatabase
import psycopg2
import redis

# elasticsearch
index_name = "materials_smelkin"
es = Elasticsearch("http://elastic:2517Pass@10.66.66.1:9200")

# Neo4j
uri = "bolt://10.66.66.1:7687"
userName = "neo4j"
password = "2517Pass"

graphDB_Driver  = GraphDatabase.driver(uri, auth=(userName, password))

#postgresql
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

#Redis
redis = redis.Redis(host= '10.66.66.1', port= '6379', db=1)

# Значения для запроса
student_limit = 10
phrase = 'разъясню'
begin_date = '2023-09-01'
end_date = '2024-05-29'

query_body = {
    #"size":100,
    "query": {
        "query_string": {
            "query":  "*%s*" % (phrase),
			"default_field": "description"
        }
    }
}

#1
# id лекцции из материалов где фраза
materials_with_phrase = es.search(index='materialssmelkin', body=query_body)
# print("выборка из elastic")
# print(materials_with_phrase)
materials_with_phrase_ids = []
for lection_id in materials_with_phrase['hits']['hits']:
	materials_with_phrase_ids.append(lection_id['_source']['lecture_id'])
print(materials_with_phrase_ids)

#2 студенты, посещающие занятия
students = []
# print("выборка  из neo")
for lection_id in materials_with_phrase_ids:
    for student in graphDB_Driver.session(database="smelkin").run("MATCH (l:Lecture{iid:$id})--(d:Disciplines)--(s:Specialnost)--(g:Group)--(st:Student) RETURN  st", id=str(lection_id)).data():
        students.append(student['st']['id_stud_code'])
        # print(student)

#3 статистика посещаемости
querry_pattern = '''SELECT (CAST(SUM(CASE WHEN visited THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*)) AS percent, student_id
FROM visits
WHERE student_id in (%s)
AND date_visit between '%s' AND '%s'
GROUP BY student_id
ORDER BY percent
LIMIT '%s'
'''
cursor.execute(querry_pattern % (','.join(map(str,students)), str(begin_date), str(end_date), str(student_limit)))
result=cursor.fetchall()
# print("выборка из pg")
# print(result)

#4 формирование отчёта
print("\nОтчет:")
for i in result:
    print("№ "+str(i[1])+"\t"+redis.get(i[1]).decode()+"\t"+str(int(i[0]*100))+"%\t"+ "c "+ str(begin_date)+"\tпо "+str(end_date)+" - "+phrase)
