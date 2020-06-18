import MapReduce
import sys
import json
import itertools
"""
Asymmetric
"""

mr = MapReduce.MapReduce()
a = []
b = []
# =============================
# Do not modify above this line
def mapper(record):
    matrix = record[0]
    i = record[1]
    j = record[2]
    value = record[3]
    mr.emit_intermediate((matrix, i, j), value)

def reducer(matrix, values):
    sum = 0
    pass


# Do not modify below this line
# =============================
if __name__ == '__main__':
  # inputdata = open(sys.argv[1])
  inputdata = open('./data/matrix.json')
  mr.execute(inputdata, mapper, reducer)
