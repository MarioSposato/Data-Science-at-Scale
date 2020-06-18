import MapReduce
import sys
import json
import itertools
"""
Asymmetric
"""

mr = MapReduce.MapReduce()
a = []

# =============================
# Do not modify above this line
def mapper(record):
    #personA = record[0]
    #personB = record[1]
    sequence_id = record[0]
    nucleotides = record[1][:-10]
    mr.emit_intermediate(sequence_id, nucleotides)

def reducer(sequence_id, nucleotides):
    if nucleotides not in a:
        a.append(nucleotides)
        mr.emit(nucleotides[0])



# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  # inputdata = open('./data/dna.json')
  mr.execute(inputdata, mapper, reducer)
