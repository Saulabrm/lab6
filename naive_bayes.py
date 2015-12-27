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
        self.vocabulary_random = len(self.words_random)
        self.vocabulary_fortnow = len(self.words_fortnow)

    def prob_word_category(self, word, category):
        if category == "random":
            if word in self.words_random:
                wf = self.words_random[word]
            else:
                wf = 0
            return (wf+1)/(self.amount_words_random + self.vocabulary_random)
        else:
            if word in self.words_fortnow:
                wf = self.words_fortnow[word]
            else:
                wf = 0
            return (wf+1)/(self.amount_words_fortnow + self.vocabulary_fortnow)

    def prob_class(self, category):
        if category == "random":
            return self.num_docs_random/self.num_docs
        else:
            return self.num_docs_fortnow/self.num_docs

    def classify_doc(self, doc):
        p_random = math.log(self.prob_class("random"), 10)
        p_fortnow = math.log(self.prob_class("fortnow"), 10)
        for w in doc:
            p_random += math.log(self.prob_word_category(w, "random"), 10)
            p_fortnow += math.log(self.prob_word_category(w, "fortnow"), 10)
            
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
        print(random_results)
        print(fortnow_results)


nb = NaiveBayes()
nb.test()
