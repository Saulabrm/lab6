import os
from codecs import encode, decode
from pymongo import MongoClient

__author__ = 'Maira'


def read_file_content(db, file):
    with open("./blogfiles/" + file) as f:
        text = []
        for line in f:
            for word in line.strip().split():
                word = decode(word.strip(), 'latin2', 'ignore')
                text.append(word)
            if file.find("fortnow"):
                c = "fortnow"
            else:
                c = "random"
            d = {'content': text, 'category': c}
            db.corpus.insert_one(d)


def get_corpus():
    conn = MongoClient()
    db = conn.foo
    # eliminate the corpus db in order to avoid double insertions
    db.corpus.drop()
    files = os.listdir("./blogfiles")
    files.remove('.DS_Store')
    for f in files:
        read_file_content(db, f)
    return db.corpus

# get_corpus()
