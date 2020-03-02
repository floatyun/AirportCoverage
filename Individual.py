'''
一个解集即一个个体

支持操作
凭借01矩阵产生初始解 over
#一个解集 to 一个染色体
#一个染色体 to 一个解集
两个个体 诞生 新个体（杂交） p_a
同时有一定几率交叉互换 p_b
同时有一个几率基因突变 p_c
'''
import matplotlib.pyplot as plt
import math
import random
import numpy as np
import global_var as gl
import Solution as SLT

mmp=None

def get_init(mp, grid_len):
    global mmp
    mmp = mp
    gl.row = mp.shape[0]
    gl.col = mp[0].shape[0]
    print(gl.row)
    print(gl.col)
    gl.radius /= grid_len
    gl.max_flight_radius /= grid_len
    gl.x_chro_point_len = int(math.ceil(math.log2(gl.col)))
    gl.y_chro_point_len = int(math.ceil(math.log2(gl.row)))


def init_random_one_individual():
    '''
    初始随机化一个个体的染色体chromosome
    :return:
    '''
    X = []
    cnt = gl.point_cnt*gl.x_chro_point_len
    for i in range(cnt):
        X.append(random.randint(0,1))
    Y = []
    cnt = gl.point_cnt * gl.y_chro_point_len
    for i in range(cnt):
        Y.append(random.randint(0,1))
    individual = (X, Y)
    return individual


def init_random_population(want_pop_size):
    global mmp
    population = list()
    for i in range(want_pop_size):
        while True:
            individual = init_random_one_individual()
            solution = individual_to_solution(individual)
            if True == SLT.is_valid(solution[0],solution[1],mmp):
                break
        population.append(individual)
    return population


def individual_to_solution(individual):
    '''
    :return:
    '''
    X = list()
    for i in range(gl.point_cnt):
        t = 0
        for j in range(i * gl.x_chro_point_len, (i + 1) * gl.x_chro_point_len):
            t = t * 2 + individual[0][j]
        X.append(t%317) # gl.col
    Y = list()
    for i in range(gl.point_cnt):
        t = 0
        for j in range(i * gl.y_chro_point_len, (i + 1) * gl.y_chro_point_len):
            t = t * 2 + individual[1][j]
        Y.append(t%392) #gl.row
    solution = (X, Y)
    return solution


def crossover(pplt):
    '''
    相邻个体以一定概率杂交
    :param pplt:这一代的种群
    :param [out]
    :return:
    '''
    sz = len(pplt)
    for i in range(sz):
        male = 0
        # 0-1的随机数落于[0,cross_p)即杂交概率为cross_p
        NX = []
        NX1 = []
        NY = []
        NY1 = []
        if (random.random() < gl.cross_p):
            # 与相邻的对象杂交
            male = (i + 1) % sz
            # 随机杂交点数目及杂交点分布
            cnt, cross = random_cross_solution(gl.min_cross_point_cnt, gl.max_cross_point_cnt, gl.col)
            NX,NX1 = produce_new_list(pplt[i][0], pplt[male][0], cnt, cross)
            cnt, cross = random_cross_solution(gl.min_cross_point_cnt, gl.max_cross_point_cnt, gl.row)
            NY,NY1 = produce_new_list(pplt[i][1], pplt[male][1], cnt, cross)
        pplt[i] = (NX,NY)
        pplt[male] = (NX1,NY1)

    '''for i in range(sz):
        t_cnt = random.randint(1,4)
        for k in range(t_cnt):
            male = random.randint(0,sz-1)
            if (random.random() < gl.cross_p):
                # 随机杂交点数目及杂交点分布
                cnt, cross = random_cross_solution(gl.min_cross_point_cnt, gl.max_cross_point_cnt, gl.col)
                NX = produce_new_list(pplt[i][0], pplt[male][0], cnt, cross)
                cnt, cross = random_cross_solution(gl.min_cross_point_cnt, gl.max_cross_point_cnt, gl.row)
                NY = produce_new_list(pplt[i][1], pplt[male][1], cnt, cross)
                next_generation.append((NX, NY))
    '''


def get_random_list_without_repetition(n, m):
    '''
    n个数里面随机选m个不重复的数
    :param n:
    :param m:
    :return:
    '''
    i = 0
    ans = []
    while i < n:
        if (random.randint(0, n - i - 1) < m):
            ans.append(i)
        i += 1
    return ans


def random_cross_solution(a, b, sz):
    # 随机产生要杂交断裂的断点数目
    cnt = random.randint(a, b)
    l = get_random_list_without_repetition(n=sz, m=cnt)
    # 把最后的点设置为断点
    cnt += 1
    l.append(sz)
    return cnt, l


def produce_new_list(dad, mom, cnt, cross):
    l = 0
    ans = []
    ans1 = []
    for i, r in enumerate(cross):
        if i%2 == 0:
            ans.extend(dad[l:r])
            ans1.extend(mom[l:r])
        else:
            ans.extend(mom[l:r])
            ans1.extend(dad[l:r])
    return ans,ans1

def mutation(next_generation):
    global mmp
    '''
    基因突变
    每个新生的个体，以一定概率基因突变（一个位产生变化）
    :return: 
    '''
    sz = len(next_generation)
    ans = []
    for i in range(sz):
        if (random.random() < gl.mutation_p):
            j = random.randint(0, gl.col-1)
            next_generation[i][0][j] ^= 1
            j = random.randint(0, gl.row - 1)
            next_generation[i][1][j] ^= 1
        solution = individual_to_solution(individual=next_generation[i])
        if True == SLT.is_valid(X=solution[0], Y=solution[1], mmp=mmp):
            ans.append(solution)
    return ans