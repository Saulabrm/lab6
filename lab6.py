from pymongo import MongoClient

__author__ = 'Maira'

conn = MongoClient()
db = conn.test

db.testing.insert({"j": 5, "k": 6, "m": "nopqr"})
db.testing.insert({"j": 15, "k": 6, "m": "nopqr"})

d = {'j': 10, 'k': 6}
for i in range(4):
    d['a' * i] = i

db.testing.insert(d)

d = {'j': 8, 'k': 6, 'b': "Hi there!"}
db.testing.insert(d)

docs = db.testing.find({"j": 10})

for doc in docs:
    print("(j:10)", doc)

for doc in db.testing.find({"k": {"$lt": 7}}):
    print("(k<7)", doc)

for doc in db.testing.find({"j": {"$gt": 9}}):
    print("(j>9)", doc)

db.testing.remove({"k": 6})
