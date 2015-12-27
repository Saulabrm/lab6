from pymongo import MongoClient
import get_corpus as gc
import dwc_mr as dwc
import twc_mr as twc
__author__ = 'Maira'


class NaiveBayes:
    def __init__(self):
        conn = MongoClient()
        db = conn.foo
        db.corpus = gc.get_corpus()
        # Just setting static values for the number of documents from each class.
        self.num_docs = 60
        self.num_docs_random = 30
        self.num_docs_fortnow = 30
        self.random_docs_test = db.corpus.find({"category": "random"}).limit(30).skip(30)
        self.fortnow_docs_test = db.corpus.find({"category": "fortnow"}).limit(30).skip(30)
        dwr = dwc.get_bag_of_words(db.corpus, {"category": "random"}, 30)
        dwr = dwr.find()
        self.words_random = dict((r['_id'], r['value']) for r in dwr)
        dwf = dwc.get_bag_of_words(db.corpus, {"category": "fortnow"}, 30)
        dwf = dwf.find()
        self.words_fortnow = dict((r['_id'], r['value']) for r in dwf)
        twcr = twc.get_bag_of_words(db.corpus, {"category": "random"}, 30)
        twcr = twcr.find()
        for r in twcr:
            self.amount_words_random = r['value']
        twcf = twc.get_bag_of_words(db.corpus, {"category": "fortnow"}, 30)
        twcf = twcf.find()
        for r in twcf:
            self.amount_words_fortnow = r['value']


NaiveBayes()
