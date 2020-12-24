import multiprocessing as mp
import time
import sys
import argparse
import os
import random
import math

def node_selection(R):
    Sk = set()
    rr_cover_cnt = [0 for i in range(n+1)]
    node_to_rr_index = {}
    count = 0
    for i in range(len(R)):
        for rr_node in R[i]:
            rr_cover_cnt[rr_node] += 1
            if rr_node not in node_to_rr_index.keys(): 
                node_to_rr_index[rr_node] = set()
            node_to_rr_index[rr_node].add(i) 

    for i in range(k):
        max_index = rr_cover_cnt.index(max(rr_cover_cnt))
        Sk.add(max_index)
        count += len(node_to_rr_index[max_index])
        index_set = [rr for rr in node_to_rr_index[max_index]]
        for j in index_set:
            for rr_node in R[j]:
                node_to_rr_index[rr_node].remove(j)
                rr_cover_cnt[rr_node] -= 1
    return Sk, count/len(R)


def sampling():
    R = []
    while time.time() - start_time < time_limit/2:
        R.append(generate_rr(random.randint(1, n)))
    return R


def generate_rr(v):
    if model == 'IC':
        return generate_rr_ic(v)
    return generate_rr_lt(v)


def generate_rr_ic(node):
    activity_set = [node]
    total_set = [node]
    while len(activity_set) > 0:
        new_activity_set = []
        for index in activity_set:
            seed = nodes[index]
            for i in range(len(seed[0])):
                neighbor = seed[0][i]
                if neighbor in total_set:
                    continue
                influence = seed[1][i]
                if random.random() < influence:
                    new_activity_set.append(neighbor)
                    total_set.append(neighbor)
        activity_set = new_activity_set
    
    return total_set


def generate_rr_lt(node):
    activity_set = node
    total_set = [node]

    while activity_set != -1:
        new_activity_set = -1
        
        neighbors = nodes[activity_set][0];
        if len(neighbors) == 0:
            break
        neighbor = neighbors[random.randint(0, len(neighbors)-1)]
        if neighbor not in total_set:
            new_activity_set = neighbor
            total_set.append(neighbor)
        activity_set = new_activity_set
    return total_set


def imm():
    R = sampling()
    Sk, z = node_selection(R)
    return Sk


def logcnk(n, k):
    comp_result = 0
    for i in range(n-k+1, n+1):
        comp_result += math.log(i)
    for i in range(1, k+1):
        comp_result -= math.log(i)
    return comp_result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--file_name', type=str, default='network2.txt')
    parser.add_argument('-k', '--seed_size', type=int, default=500)
    parser.add_argument('-m', '--model', type=str, default='IC')
    parser.add_argument('-t', '--time_limit', type=int, default=120)

    args = parser.parse_args()
    file_name = args.file_name
    k = args.seed_size
    model = args.model
    time_limit = args.time_limit

    nodes = {}

    msg = ''
    n = 0
    edge_num = 0

    with open(file_name, 'r') as f:
        n, edge_num = f.readline().strip('\n').split(' ')
        n, edge_num = int(n), int(edge_num)

        for i in range(int(n) + 1):
            nodes[i] = [[],[]]
        
        for line in f.readlines():
            n1, n2, w = line.strip("\n").split(' ')
            n1, n2, w = int(n1), int(n2), float(w)
            nodes[n2][0].append(n1)
            nodes[n2][1].append(w)

    start_time = time.time() 
    seeds = imm()

    for seed in seeds:
        print(seed)

    msg += str(time.time()- start_time)
    print(msg)
