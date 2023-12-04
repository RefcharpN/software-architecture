from elasticsearch import Elasticsearch

es = Elasticsearch("http://elastic:uw3yy=ACpH1pmh2EZrEK@localhost:9200")

#Вывести все значения
res = es.search(index="courses", query={"match_all": {}})
print(res)