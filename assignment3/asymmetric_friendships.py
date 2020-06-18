import MapReduce
import sys
import json
import itertools
"""
Asymmetric
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line
def mapper(record):
    #personA = record[0]
    #personB = record[1]
    personA = record[0]
    personB = record[1]
    mr.emit_intermediate(personA, personB)


def reducer(personA, friends):
    for friend in friends:
        if (friend in mr.intermediate.keys() and personA not in mr.intermediate[friend]) or (friend not in mr.intermediate.keys()):
            mr.emit((friend, personA))
            mr.emit((personA, friend))
# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  # inputdata = open('./data/friends.json')
  mr.execute(inputdata, mapper, reducer)
