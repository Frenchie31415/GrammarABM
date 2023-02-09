import numpy as np
import random
dist = []

for i in range(0,5):
    dist.append(random.randint(0,10))

dist_sum = sum(dist)

for i in range(0,5):
    dist[i] = dist[i] / dist_sum

print(dist)
print(sum(dist))