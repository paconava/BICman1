import csv
import time
from itertools import permutations

start_time = time.time()
def tsp(num_of_cities, data):
    tour = list(range(0,num_of_cities))
    dist = 0
    min_dist = 999999999
    tour_list = []
    cities = []
    tour_array = list(permutations(tour, num_of_cities))
    for perms in tour_array:
        dist = 0
        for i in range(0,num_of_cities-1):
            dist = dist + float(data[perms[i]+1][perms[i+1]])
        dist = dist + float(data[perms[num_of_cities-1]+1][perms[0]])
        if dist < min_dist:
            min_dist = dist
            tour_list = list(perms)
    tour_list.append(tour_list[0])
    for i in tour_list:
        cities.append(data[0][i])
    return cities, format(min_dist, '.2f')


with open("european_cities.csv", "r") as f:
    data = list(csv.reader(f, delimiter=';'))

cl, md = tsp(6, data)

print('Shortest tour:\n', cl)
print('Total length of tour: ', md)
print('Time of exec: ', time.time() - start_time)