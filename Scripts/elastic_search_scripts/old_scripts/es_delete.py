from elasticsearch import Elasticsearch

es = Elasticsearch("http://elastic:uw3yy=ACpH1pmh2EZrEK@localhost:9200")

_id=input("Введите id:")

try:
    es.delete(index="courses", id=_id)
except:
    print("Error delete")