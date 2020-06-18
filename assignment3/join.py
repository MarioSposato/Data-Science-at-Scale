import MapReduce
import sys
import json
import itertools
"""
Join
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # table: table name
    # id: field id
    # data: record attributes
    idx = record[1]
    # emit_intermediate genera un dizionario, con key=il primo argomento, value=il secondo
    mr.emit_intermediate(idx, list(record))

#al reducer arrivano gli elementi del dizionario uno alla volta
def reducer(idx, record):

    for index in range(1, len(record)):
        mr.emit(record[0]+record[index])

# Do not modify below this line
# =============================
if __name__ == '__main__':
  # inputdata = open(sys.argv[1])
  inputdata = open('./data/records.json')
  mr.execute(inputdata, mapper, reducer)
