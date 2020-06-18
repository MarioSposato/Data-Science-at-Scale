import MapReduce
import sys
import json
"""
Inverted Index problem
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # document_id: document identifier
    # text: document contents
    document_id = record[0]
    text = record[1]
    doc_dict = {}
    for w in text.split():
        doc_dict[w] = document_id
    for k, v in doc_dict.items():
        mr.emit_intermediate(k, v)


def reducer(word, list_of_values):
    # word: word
    # list_of_values: list of document_ids
    mr.emit((word, list_of_values))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
