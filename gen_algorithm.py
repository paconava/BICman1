import csv
import random
import statistics
import numpy as np
import matplotlib.pyplot as plt

def final_runs(nofruns, num_of_cities, pop_size, gens):
    bestt_in_gen = [0 for x in range(0,nofruns)]
    tour_t = [0 for x in range(0,nofruns)]
    dists_t = [0 for x in range(0,nofruns)]
    bestd_in_gen = [0 for x in range(0,nofruns)]
    wd = [0 for x in range(0,nofruns)]
    ave_dist = [0 for x in range(0,nofruns)]
    std_dist = [0 for x in range(0,nofruns)]
    ave_list = [0 for x in range(0,nofruns)]
    ave_rage = [0 for x in range(0,gens)] 
    for run in range(0,nofruns):
        (bestt_in_gen[run], 
        tour_t[run], 
        dists_t[run], 
        bestd_in_gen[run], 
        wd[run], 
        ave_dist[run], 
        std_dist[run], 
        ave_list[run]) = ga(num_of_cities, pop_size, gens)
    best_distance = dists_t[nofruns-1]
    worst_distance = wd[nofruns-1]
    ave_distance = float(ave_dist[nofruns-1])
    deviation = std_dist[nofruns-1]
    for i in range(0,gens):
        ave_rage[i] = np.mean([float(x[i]) for x in bestd_in_gen])
    return best_distance, worst_distance, ave_distance, ave_rage, deviation

def select_parents(individuals, fitness, elitism):
    best_n = []
    best_f = []
    indexes = sorted(fitness, key=float)
    for i in range(0, elitism):
        best_n.append(individuals[fitness.index(indexes[i])])
        best_f.append(indexes[i])
    parents = [x for x in best_n]

    return parents

def pmx(frcp, srcp, fp, sp):
    child = list(-1 for x in fp)
    for j in range(frcp, srcp):
            child[j] = fp[j]
    for j in range(frcp, srcp):
        flag = True
        aux_val = sp[j]
        if aux_val not in child:
            to_move = aux_val
            while flag:
                aux_index = sp.index(aux_val)
                aux_val = fp[aux_index]
                aux_index2 = sp.index(aux_val)
                if aux_index2 not in range(frcp, srcp):
                    flag = False
            child[aux_index2] = to_move
    for j in range(0,len(sp)):
        if sp[j] not in child:
            child[j] = sp[j]
    return child

def recombine(parents, pop_size):
    children = []
    for i in range(0, int(len(parents)/2)):
        fpi = i * 2
        spi = fpi + 1
        first_parent = list(parents[fpi])
        second_parent = list(parents[spi])
        if len(parents[0]) >= 17 and len(parents[0]) < 25:
            first_rcp = random.randrange(1,len(parents[0])-8)
            second_rcp = first_rcp + 8
        elif len(parents[0]) >= 11 and len(parents[0]) < 17:
            first_rcp = random.randrange(1,len(parents[0])-6)
            second_rcp = first_rcp + 6
        elif len(parents[0]) >= 6 and len(parents[0]) < 11:
            first_rcp = random.randrange(1,len(parents[0])-4)
            second_rcp = first_rcp + 4
        else:
            first_rcp = random.randrange(1,len(parents[0])-2)
            second_rcp = first_rcp + 1
        children.append(pmx(first_rcp, second_rcp, first_parent, second_parent))
        children.append(pmx(first_rcp, second_rcp, second_parent, first_parent))
    return children
           
def ga(num_of_cities, pop_size, gens):
    tours = [init_tour(num_of_cities) for x in range(pop_size)]
    dists = [find_dist(x) for x in tours]
    best_tours = [0 for i in range(gens)]
    best_dist = [0 for i in range(gens)]
    ave_list = [0 for i in range(gens)]
    for i in range(gens):
        new_parents = select_parents(tours, dists, int(pop_size/2))
        new_children = recombine(new_parents, pop_size)
        best_tours[i] = list(new_parents[0])
        best_dist[i] = find_dist(new_parents[0])
        new_pop = new_parents[:len(new_parents)//2]
        new_pop.extend(new_children[:len(new_children)//2])
        new_pop.extend([init_tour(num_of_cities) for x in range(len(new_parents))])
        dists_float = [float(i) for i in dists]
        ave_list[i] = np.mean(dists_float)
        tours = list(new_pop)
        dists = [find_dist(x) for x in tours]
    worst_dist = max(dists_float)
    return (best_tours,
        new_pop[0], 
        find_dist(new_pop[0]), 
        best_dist, 
        worst_dist, 
        format(np.mean(dists_float), '.2f'), 
        format(statistics.stdev(dists_float), '.2f'), 
        ave_list)
    
def find_dist(tour_list):
    new_dist = 0
    for i in range(0,len(tour_list)-1):
        new_dist = new_dist + (float(data[tour_list[i]+1][tour_list[i+1]]))
    new_dist = new_dist + (float(data[tour_list[i+1]+1][tour_list[0]]))
    return format(new_dist, '.2f')
    
def init_tour(num):
    tour = list(range(0,num))
    random.shuffle(tour)
    return tour
        
with open("european_cities.csv", "r") as f:
    data = list(csv.reader(f, delimiter=';'))

cities = 6
gens = cities * 5
pop1 = cities * 8

best_d1, worst_d1, ave_d1, ave_ar1, dev1 = final_runs(20,cities,pop1,gens)
best_d2, worst_d2, ave_d2, ave_ar2, dev2 = final_runs(20,cities,pop1*2,gens)
best_d3, worst_d3, ave_d3, ave_ar3, dev3 = final_runs(20,cities,pop1*4,gens)

print("--- 20 runs ---")
print("Pop\tBest\t\tWorst\t\tAverage\t\tDeviation")
print(pop1, '\t', best_d1, '\t', worst_d1, '\t', format(ave_d1, '.2f'), '\t', dev1)
print(pop1*2, '\t', best_d2, '\t', worst_d2, '\t', format(ave_d2, '.2f'), '\t', dev2)
print(pop1*4, '\t', best_d3, '\t', worst_d3, '\t', format(ave_d3, '.2f'), '\t', dev3)
plt.title("Average fitness per gen")
plt.ylabel("Fitness")
plt.xlabel("Generation")
line1, = plt.plot([i for i in range(1,gens+1)], ave_ar1, 'r', label="Pop. size=" + str(pop1))
line2, = plt.plot([i for i in range(1,gens+1)], ave_ar2, 'g', label="Pop. size="+ str(pop1*2))
line3, = plt.plot([i for i in range(1,gens+1)], ave_ar3, 'b', label="Pop. size="+ str(pop1*4))
plt.legend(handles=[line1, line2, line3])
plt.show()