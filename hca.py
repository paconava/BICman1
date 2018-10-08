import csv
# import time
import random
import numpy as np
import statistics

def final_props(cities, reps):
    print("\n\nNumber of cities: ", cities)
    print("Repetitions: ", reps)
    cl = [0 for x in range(reps)]
    md = [0 for x in range(reps)]
    for x in range(0,reps):
        cl[x], md[x] = tsp(cities, data)
        md[x] = float(md[x])
    print('Min: ', min(md))
    print('Max: ', max(md))
    print('Min trip: ')
    print(cl[md.index(min(md))])
    print('Max trip: ')
    print(cl[md.index(max(md))])    
    print('Mean: ', np.mean(md))
    print('Standard deviation: ', statistics.stdev(md))

def find_dist(tour_list):
    new_dist = 0
    for i in range(0,len(tour_list)-1):
        new_dist = new_dist + (float(data[tour_list[i]+1][tour_list[i+1]]))
    return format(new_dist, '.2f')
    
def init_tour(num):
    tour = list(range(0,num))
    random.shuffle(tour)
    tour.append(tour[0])
    return tour
        
def tsp(num_of_cities, data):
    cities = []
    tour = init_tour(num_of_cities)
    dist = find_dist(tour)
    minNotFound = True
    while minNotFound:
        i = 1
        aux_tour = list(tour)
        examBrotherhood = True
        while examBrotherhood:
            if i != num_of_cities - 1:
                auxTL = aux_tour[i+1]
                aux_tour[i+1] = aux_tour[i]
                aux_tour[i] = auxTL
                aux_dist = find_dist(aux_tour)
                if aux_dist < dist:
                    dist = aux_dist
                    tour = list(aux_tour)
                    examBrotherhood = False
                else:
                    aux_tour = list(tour)
            else:
                examBrotherhood = False
                minNotFound = False
            i = i + 1
    for i in tour:
        cities.append(data[0][i])
    return cities, dist

with open("european_cities.csv", "r") as f:
    data = list(csv.reader(f, delimiter=';'))

final_props(10,20)