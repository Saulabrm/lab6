from pymongo import MongoClient
import get_corpus as gc
import dwc_mr as dwc
import twc_mr as twc
import math
__author__ = 'Maira'


class NaiveBayes:
    def __init__(self):
        conn = MongoClient()
        db = conn.foo
        db.corpus = gc.get_corpus()
        # Just setting static values for the number of documents from each class.
        self.num_docs = 60.0
        self.num_docs_random = 30.0
        self.num_docs_fortnow = 30.0
        self.random_docs_test = db.corpus.find({"category": "random", "file_id": {"$gt": 30}})
        self.fortnow_docs_test = db.corpus.find({"category": "fortnow", "file_id": {"$gt": 30}})
        dwr = dwc.get_bag_of_words(db.corpus, {"category": "random", "file_id": {"$lt": 31}})
        dwr = dwr.find()
        self.words_random = dict((r['_id'], r['value']) for r in dwr)
        dwf = dwc.get_bag_of_words(db.corpus, {"category": "fortnow", "file_id": {"$lt": 31}})
        dwf = dwf.find()
        self.words_fortnow = dict((r['_id'], r['value']) for r in dwf)
        twcr = twc.get_bag_of_words(db.corpus, {"category": "random", "file_id": {"$lt": 31}})
        twcr = twcr.find()
        for r in twcr:
            self.amount_words_random = r['value']
        twcf = twc.get_bag_of_words(db.corpus, {"category": "fortnow", "file_id": {"$lt": 31}})
        twcf = twcf.find()
        for r in twcf:
            self.amount_words_fortnow = r['value']
        v = self.words_random.copy()
        v.update(self.words_fortnow)
        self.vocabulary_size = len(v)

    def prob_word_category(self, word, category):
        if category == "random":
            if word in self.words_random:
                wf = self.words_random[word]
            else:
                wf = 0
            return (wf+1)/(self.amount_words_random + self.vocabulary_size)
        else:
            if word in self.words_fortnow:
                wf = self.words_fortnow[word]
            else:
                wf = 0
            return (wf+1)/(self.amount_words_fortnow + self.vocabulary_size)

    def prob_class(self, category):
        if category == "random":
            return self.num_docs_random/self.num_docs
        else:
            return self.num_docs_fortnow/self.num_docs

    def classify_doc(self, doc):
        p_random = math.log(self.prob_class("random"))
        p_fortnow = math.log(self.prob_class("fortnow"))
        for word in doc:
            p_random += math.log(self.prob_word_category(word, "random"))
            p_fortnow += math.log(self.prob_word_category(word, "fortnow"))
        if p_random > p_fortnow:
            return "random"
        return "fortnow"

    def test(self):
        random_results = []
        fortnow_results = []
        for d in self.random_docs_test:
            c = self.classify_doc(d["content"])
            random_results.append(c)
        for d in self.fortnow_docs_test:
            c = self.classify_doc(d["content"])
            fortnow_results.append(c)
        print("             fortnow     random")
        print("_______________________________")
        print("fortnow        "+str(fortnow_results.count("fortnow"))+"           "+str(fortnow_results.count("random")))
        print("random         "+str(random_results.count("fortnow"))+"          "+str(random_results.count("random")))




nb = NaiveBayes()
nb.test()