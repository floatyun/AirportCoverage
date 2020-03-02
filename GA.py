import Individual as IDV
import global_var as gl
import Solution as SLT
import lisiqi as lsq
import random
import os


def work(mp,grid_len):
    IDV.get_init(mp,grid_len)
    pop = IDV.init_random_population(gl.want_init_population_size)
    result = []
    next_generation = []
    process = [] # 中间结果
    t_best_individual = ()
    t_best_fit = 0

    for i in range(gl.iter_count):
        print("i = ", i, "total iteration = ", gl.iter_count )
        obj_value = calc_obj_value(pop)
        print("finish cal obj values")
        fit_value = calc_fit_value(obj_value)
        print("finish cal fit values")
        t_best_individual, t_best_fit = find_best(pop, fit_value)
        print("finish find")
        selection(pop, fit_value)
        print("finish selection")
        IDV.crossover(pop)
        print("finish crossover")
        IDV.mutation(pop)
        print("finish mutation")
        #nxt_obj_value = calc_obj_value(next_generation)
        #nxt_fit_value = calc_fit_value(nxt_obj_value)

        if (i%10 == 0):
            process.append((t_best_individual, t_best_fit))

    best_individual = t_best_individual
    best_fit = t_best_fit
    solution = IDV.individual_to_solution(best_individual)
    X = solution[0]
    Y = solution[1]
    lsq.finial(xList=Y,yList=X)


def selection(pop, fit_value):
    p_fit_value = []
    # 适应度总和
    total_fit = sum(fit_value)
    # 归一化，使概率总和为1
    for i in range(len(fit_value)):
        p_fit_value.append(fit_value[i] / total_fit)
    # 概率求和排序
    cum_sum(p_fit_value)
    pop_len = len(pop)
    # 类似搞一个转盘吧下面这个的意思
    ms = sorted([random.random() for i in range(pop_len)])
    fitin = 0
    newin = 0
    newpop = pop[:]
    # 转轮盘选择法
    while newin < pop_len:
        # 如果这个概率大于随机出来的那个概率，就选这个
        if (ms[newin] < p_fit_value[fitin]):
            newpop[newin] = pop[fitin]
            newin = newin + 1
        else:
            fitin = fitin + 1
    # 这里注意一下，因为random.random()不会大于1，所以保证这里的newpop规格会和以前的一样
    # 而且这个pop里面会有不少重复的个体，保证种群数量一样

    # 之前是看另一个人的程序，感觉他这里有点bug，要适当修改
    pop = newpop[:]

# 计算累计概率
def cum_sum(fit_value):
    for i in range(1,len(fit_value)):
        fit_value[i] += fit_value[i-1];

def calc_obj_value(pop):
    obj_value = []
    for individual in pop:
        solution = IDV.individual_to_solution(individual)
        X = solution[0]
        Y = solution[1]
        obj_value.append(lsq.calc_area(Y,X));
    return obj_value

def calc_fit_value(obj_value):
    fit_value = []
    #
    # 比如c_min设大一些可以加快收敛
    # 但是如果设置过大，有可能影响了全局最优的搜索
    c_min = gl.row*gl.col*0.2
    for value in obj_value:
        if value > c_min:
            temp = value
        else:
            temp = 0.
        fit_value.append(temp)
    # fit_value保存的是活下来的值
    return fit_value

def find_best(pop, fit_value):
    n = len(fit_value)
    best_id = 0
    for i in range(n):
        if fit_value[i] > fit_value[best_id]:
            best_id = i
    return pop[best_id], fit_value[best_id]


lsq.ReadFile()
work(lsq.IM,lsq.disB)