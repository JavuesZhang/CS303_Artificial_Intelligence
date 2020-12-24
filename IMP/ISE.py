# -*- coding: utf-8 -*-
# written by mark zeng 2018-11-14
# modified by Yao Zhao 2019-10-30
# re-modified by Yiming Chen 2020-11-04

import multiprocessing as mp
import time
import sys
import argparse
import os
import numpy as np
import random

core = 8
iteration = 1000
result = []

def IC_Sample(seeds, nodes):
    activity_set = seeds.copy()
    total_set = seeds.copy()
    count = len(activity_set) 
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
        count += len(new_activity_set)
        activity_set = new_activity_set
    return count

def LT_Sample(seeds, nodes):
    activity_set = seeds.copy()
    total_set = seeds.copy()
    count = len(activity_set)
    threshold = np.zeros(int(len(nodes)))
    cumulate = np.zeros(int(len(nodes)))
    for i in range(len(nodes)):
        rdm = random.random()
        threshold[i] = rdm
        if rdm == 0 and i > 0:
            activity_set.append(i)

    for index in activity_set:
        seed = nodes[index]
        for i in range(len(seed[0])):
            neighbor = seed[0][i]
            cumulate[neighbor] += seed[1][i]

    while len(activity_set) > 0:
        new_activity_set = []
        for index in activity_set:
            seed = nodes[index]
            for i in range(len(seed[0])):
                neighbor = seed[0][i]
                if neighbor not in total_set and cumulate[neighbor] >= threshold[neighbor]:
                    new_activity_set.append(neighbor)
                    total_set.append(neighbor)
                    for j in range(len(nodes[neighbor][0])):
                        cumulate[nodes[neighbor][0][j]] += nodes[neighbor][1][j]
        count += len(new_activity_set)
        activity_set = new_activity_set
    return count

if __name__ == '__main__':
    sys.setrecursionlimit(10000)

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--file_name', type=str, default='network2.txt')
    parser.add_argument('-s', '--seed', type=str, default='network_seeds.txt')
    parser.add_argument('-m', '--model', type=str, default='IC')
    parser.add_argument('-t', '--time_limit', type=int, default=120)

    args = parser.parse_args()
    file_name = args.file_name
    seed = args.seed
    model = args.model
    time_limit = args.time_limit
    start_time = time.time()
    
    nodes = {}
   
    with open(file_name, 'r') as f:
        node_num, edge_num = f.readline().strip('\n').split(' ')
        
        for i in range(int(node_num) + 1):
            nodes[i] = [[],[],[],[]]
        
        for line in f.readlines():
            n1, n2, w = line.strip("\n").split(' ')
            n1, n2, w = int(n1), int(n2), float(w)
            nodes[n1][0].append(n2)
            nodes[n1][1].append(w)

    with open(seed, 'r') as f:
        seeds = []
        for line in f.readlines():
            seeds.append(int(line.strip('\n')))
    

    # np.random.seed(0)

    # a = LT_Sample(seeds, nodes)
    # print(a)


    msg = ''
    pool = mp.Pool(core)
    summa = 0
    if model == 'IC':
        Sample_Method = IC_Sample
    else:
        Sample_Method = LT_Sample
    
    # print(nodes)
    # print(seeds)
    async_result = []
    a = 1
    for i in range(iteration):
        res = pool.apply_async(func=Sample_Method, args=(seeds, nodes), callback=result.append)
        async_result.append(res)

    while 1:
        time.sleep(0.5)
        if time.time()-start_time>time_limit-5:
            msg += 'break2\n'
            msg += str(len(async_result))+'\n'
            break
        if async_result[len(async_result)-1].ready() and async_result[len(async_result)-1].successful():
            msg += 'break3\n'
            msg += str(len(async_result))+'\n'
            break
    # pool.close()
    msg += str(pool)+'\n'
    pool.terminate()
    pool.join()

    for i in range(len(result)):
        summa = summa + result[i]
    if len(result) > 0:
        summa = summa/len(result)
    
    msg += str(len(result))+'\n'
    msg += str(time.time()-start_time)+'\n'
    msg = str(summa) + '\nthis is result\n' + msg
    print(msg)
    # summa = 0
    
    # if model == 'IC':
    #     Sample_Method = IC_Sample
    # else:
    #     Sample_Method = LT_Sample
        
    # for i in range(iteration):
    #     summa += Sample_Method(seeds.copy())
    #     if time.time() - start_time > time_limit - 5:
    #         iteration = i+1
    #         break
    # summa /= iteration
    
    # print(summa)
    
    '''
    程序结束后强制退出，跳过垃圾回收时间, 如果没有这个操作会额外需要几秒程序才能完全退出
    '''
    sys.stdout.flush()

