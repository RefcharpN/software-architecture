from elasticsearch import Elasticsearch

es = Elasticsearch("http://elastic:2517Pass@10.66.66.1:9200")

try:
    es.indices.delete(index='materialssmelkin')
    print("docs delete")
    # es.delete(index="materials")
except:
    print("Error delete!!!")