import random,math
import sys
from random import randint
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
import itertools


#sc = SparkConf().setAppName('LSH')
#sc = SparkContext(conf=conf)

class minhash_mapper:
    def __init__(self, num_hashes, mod_val, hash_funcs = None):
        self.num_hashes = num_hashes
        self.mod_val = mod_val
        max_ = math.pow(2,10)-1#tentative! need to change it, test purpose
        self.hash_funcs = self.hash_params_generate(max_,hash_funcs)


    def hash_params_generate(self, max_,hash_funcs): #same for the entire system
        if not hash_funcs:
             return [(randint(0,max_),randint(1,max_)) for i in xrange(k)]
        return hash_funcs

    def min_hash_val(self, data, hash_func):
        return data.map(lambda x: (hash_func[0]*x+hash_func[1])%self.mod_val).reduce(min)

    #run min_hash_val on each hash_func -> extend the list (flatMap)
    def min_hash_operate(data):
        for hash_func in self.hash_funcs:
            yield min_hash_val(data,hash_func,self.mod_val)

           
            

def min_hash_val(data, hash_func, mod_val):
    return data.map(lambda x: (hash_func[0]*x+hash_func[1])%mod_val)#.reduce(min)




#run min_hash_val on each hash_func -> extend the list (flatMap)
def min_hash_operate(data, hash_funcs, mod_val):
    for hash_func in hash_funcs:
        yield min_hash_val(data,hash_func,mod_val)

        
def min_hash_operate1(data, hash_funcs, mod_val):
    return [min_hash_val(data,hash_func,mod_val).reduce(min) for i,hash_func in enumerate(hash_funcs)]




k = 20
max_= 30
params = hash_params_generate(k,24)
#indices = sc.parallelize([[1,2,3,4,5],[2,4,7],[9,20,30],[10,7],[9,20]]) 
mod_val = 24 #retrieved from DB: largest index value
hash_funcs = [[3000,3032],[2513,7142]]

index = sc.parallelize([1,2,3,4,9,20])
result = min_hash_operate(index,hash_funcs,mod_val)

indices = sc.parallelize([[1,2,3,4,5],[2,4,7],[9,20,30],[10,7],[9,20]]) 

out = []

for hash_func in hash_funcs:
    indices.map(lambda index: 

#map key: (post_id,hash_id), value: hash_value
#reduce: min

                
#from pyspark.mllib.linalg.distributed import RowMatrix

# Create an RDD of vectors.
rows = sc.parallelize([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12,10242,24124,421421,4242],[214,1,352,3512,413,5325,235253],[12421,4,124,2],[4421412,24,124,214,12],[424,214,124,42]])

# Create a RowMatrix from an RDD of vectors.
#mat = RowMatrix(rows)
# Get the rows as an RDD of vectors again.
#rowsRDD = mat.rows

                
k=20
mod_val = 13213
rows = sc.parallelize([[1]*1000 for i in xrange(10000)])
hash_funcs = [(randint(0,max_),randint(1,max_)) for i in xrange(k)]
def calcMinHash(row,hash_funcs):
    #return min(map(lambda x:(x*3+4)%5, row))
    return [min(map(lambda x:(x*hash_func[0]+hash_func[1])%mod_val, row)) for hash_func in hash_funcs]

                
rows.map(lambda row:calcMinHash(row,hash_funcs))
