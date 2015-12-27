import os
from codecs import decode
import string
import re
from pymongo import MongoClient
__author__ = 'Maira'


remove_punctuation = True
remove_stop_word = True
regex = re.compile('[%s]' % re.escape(string.punctuation))
cached_stop_words = []
if remove_stop_word:
    with open('stopwords/english', 'r') as file:
        for l in file:
            for w in l.split():
                cached_stop_words.append(w)


def read_file_content(db, file):
    with open("./blogfiles/" + file) as f:
        text = []
        for line in f:
            for word in line.strip().split():
                word = decode(word.strip(), 'latin2', 'ignore')
                if remove_punctuation:
                    word = regex.sub('', word)
                if (not remove_stop_word or word not in cached_stop_words) and (word != ''):
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
