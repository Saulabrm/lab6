from bson.code import Code
__author__ = 'Maira'

mapper = Code("""
    function(){
        for(var i = 0; i < this.content.length; i++) {
            emit(this.content[i], 1);
        }
    }
    """)

reducer = Code("""
    function(key, values) {
        var total = 0;
        for(var i = 0; i < values.length; i++) {
            total += values[i];
        }
        return total;
    }

""")


def get_bag_of_words(db_name, condition):
    db_name.corpus.map_reduce(mapper, reducer, "counts")
    bag_of_words = db_name.counts.find(condition).sort([("value", -1)])
    for w in bag_of_words:
        print(w)

