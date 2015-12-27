from bson.code import Code
__author__ = 'Maira'

mapper = Code("""
    function(){
        for(var i = 0; i < this.content.length; i++) {
            emit("", 1);
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


def get_bag_of_words(db, query, limit):
    return db.map_reduce(mapper, reducer, "count", query=query, limit=limit)
