import time
from random import randrange
import math

start = time.time()

def dist(tuple_1, tuple_2):
    return sum((px - qx) ** 2.0 for px, qx in zip(tuple_1, tuple_2))

def random_tuple():
    return (randrange(100), randrange(100), randrange(100))

for i in range(100000):
    d = dist(random_tuple(), random_tuple())

end = time.time()
print(end - start)