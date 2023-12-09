from elasticsearch import Elasticsearch, helpers
from neo4j import GraphDatabase
import psycopg2
import redis
from pymongo import MongoClient

# config
# ES
index_name = "materialssmelkin"
es = Elasticsearch("http://elastic:2517Pass@10.66.66.1:9200")

# Neo
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

#Mongo
CONNECTION_STRING = "mongodb://root:2517Pass@10.66.66.1:27017/?authMechanism=DEFAULT"
client = MongoClient(CONNECTION_STRING)

db = client.smelkin
collection = db.institute

# Значения для запроса
semestr_for_query = 1 # 1 или 2
year_for_query = 2023 # 2023 или 2024

def get_dates(semestr,year):
    if semestr == 1:
            year = str(year)
            return (str(year + "-09-01"), str(year + "-12-29"))
    elif semestr == 2:
        year = str(year + 1)
        return (str(year + "-01-09"), str(year + "-05-31"))

detes_period = get_dates(semestr_for_query,year_for_query)


#1 названия курсов из NEO с требованиями к тех.средствам +
discip_names = []
discip_names =  graphDB_Driver.session(database="smelkin").run("MATCH (d:Disciplines) where d.technical<>'' return d.name",yaer=str(year_for_query), semestr=str(semestr_for_query)).value()
print(discip_names)


#id занятий которые проводятся в x семестре y года +
lec_id=[]
with graphDB_Driver.session(database="smelkin") as neo_session:
        lec_id.append(neo_session.run("MATCH (d:Disciplines)--(l:Lecture)--(tt:TimeTable) WHERE d.technical<>'' and tt.lecture_id=l.iid and date($start) <= date(tt.date) and date(tt.date)<date($end) RETURN  l.iid",start=str(detes_period[0]),end=str(detes_period[1])).data())

lec_ids=[]
for i in range(len(lec_id[0])):
        lec_ids.append((lec_id[0][i]['l.iid']))
print(lec_ids)
#TODO:объединение в один запрос без цикла ниже

#вывод дисциплины и слушателей в периоде
array = []

with graphDB_Driver.session(database="smelkin") as neo_session:
    for disc in discip_names:
        count_st=(neo_session.run("MATCH (d:Disciplines)--(l:Lecture)--(tt:TimeTable)--(gr:Group)--(st:Student) WHERE d.name = $name and l.iid in $lec RETURN count (distinct st)",name=disc,lec=(lec_ids)).data())
        count = (count_st[0]['count (distinct st)'])
        array.append((disc,count))
print(array)

# #формирование отчёта
print("\nОтчет:")
for line in array:
    cur=(collection.find({"institute.cafedras.specialnosts.disciplines.name": line[0]}))
    for document in cur:
        print("\nДисциплина:",document['institute'][0]['cafedras'][0]['specialnosts'][0]['disciplines'][0]['name'])
        print("Слушателей: "+str(line[1])+" за "+str(semestr_for_query)+" семестр "+str(year_for_query)+" года")
        print("Институт:",document['institute'][0]['name'])
        print("\tКафедра:",document['institute'][0]['cafedras'][0]['name'])
        print("\tСпециальность:",document['institute'][0]['cafedras'][0]['specialnosts'][0]['name'])
        print("\tТехническое оборудование:",document['institute'][0]['cafedras'][0]['specialnosts'][0]['disciplines'][0]['technical'])