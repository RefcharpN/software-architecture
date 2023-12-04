# import random
# from pymongo import MongoClient

# client = MongoClient('localhost',27017)

# db = client.university
# col = db.groups

# def get_group_name():
#     array1 = ["БСБО","БББО","БИСО","БОСО","БАСО"]
#     array2 = ["01","02","03","04","05"]
#     array3 = ["19","20","21","22"]
#     return random.choice(list(array1))+"-"+random.choice(list(array2))+"-"+random.choice(list(array3))

# def get_cathedra():
#     array = ["Кибербезопасности и цифровых технологий","Искусственного интеллекта","Информационных технологий","Радиоэлектроники и информатики","Технологий управления"]
#     return random.choice(list(array))


# for i in range(2):
#     db.groups.insert_one({
#         'name':get_group_name(),
#         'cathedra': get_cathedra(),
#         'course': random.randint(1, 4)
#     })

import random
from pymongo import MongoClient

client = MongoClient('localhost',27017)

db = client.university
col = db.institute

for i in range(1):
    db.institute.insert_one({
        'institutes':[
            {
                'name':'Институт кибербезопасности и цифровых технологий',
                'cafedras':[
                    {
                        'name':'КБ-2',
                        'specialnosts':[
                            {
                                'name':'Информационные системы и технологии'
                            }

                        ]
                    }
                ]
            }
        ]
    })

# db = client.university
# col = db.kathedra

# for i in range(1):
#     db.kathedra.insert_one({
#         'name':'КБ-2',
#         'institute_id':'6381c26285c61653f7e07227'
#     })

# db = client.university
# col = db.specialnost

# for i in range(1):
#     db.specialnost.insert_one({
#         'name':'Информационные системы и технологии',
#         'kathedra_id':'6381c45ab1bee22516258186'
#     })