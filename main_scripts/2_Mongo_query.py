from pymongo import MongoClient
import psycopg2

#2 Генерация значений в MongoDB (Institite, Kafedra, Specialnost, Disciplines)
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


CONNECTION_STRING = "mongodb://root:2517Pass@10.66.66.1:27017/?authMechanism=DEFAULT"
client = MongoClient(CONNECTION_STRING)

# client = MongoClient('10.66.66.1',27017)

db = client.smelkin
collection = db.institute

query_for_mongo = ("SELECT i.name, k.name, s.name, d.name, d.technical FROM public.institute i,public.kafedra k,"
"public.specialnost s, public.disciplines d WHERE k.institute_id=i.id AND s.kafedra_id=k.id AND s.id = d.spec_id;")
cursor.execute(query_for_mongo)
res=cursor.fetchall()

for i in range(len(res)):
    collection.insert_one({
        'institute':[
            {
                'name':res[i][0],
                'cafedras':[
                    {
                        'name':res[i][1],
                        'specialnosts':[
                            {
                                'name': res[i][2],
                                'disciplines':[
                                    {
                                        'name':res[i][3],
                                        'technical':res[i][4]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    })

print("Mongo fill")