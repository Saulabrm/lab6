from pymongo import MongoClient
import get_corpus as gc
import counter_map_reducer as cmr
__author__ = 'Maira'


conn = MongoClient()
db = conn.foo
db.corpus = gc.get_corpus()
cmr.get_bag_of_words(db, {})
