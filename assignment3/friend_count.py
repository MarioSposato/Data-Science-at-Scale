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
    #personA = record[0]
    #personB = record[1]
    personA = record[0]
    personB = record[1]
    mr.emit_intermediate(personA, personB)

#al reducer arrivano gli elementi del dizionario uno alla volta
def reducer(personA, personB):
    mr.emit((personA, len(personB)))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
