# -*- encoding: utf-8 -*-
#实验需要修改的参数 generate_city(,) choose_city(,,city) itermax
from __future__ import generator_stop
import numpy as np
import matplotlib.pyplot as plt
import pylab
import datetime
import random

city=[]#用于生产随机城市
result_city = []
result_list = []
output_list = []
coordinates = []
output1 = 999.999
draw_current_distance = []#某一次大循环中的当前和最优举例
draw_best_distance = []
result_current_distance = []#最优的一次中的当前和最优距离
result_best_distance = []

def initial(arr):
    global coordinates
    coordinates = np.array(arr)

def getdistmat(coordinates):
    num = coordinates.shape[0]
    distmat = np.zeros((len(coordinates), len(coordinates)))
    for i in range(num):
        for j in range(i, num):
            distmat[i][j] = distmat[j][i] = np.linalg.norm(coordinates[i] - coordinates[j])
    return distmat

def yiqun():
    global output1
    global result_list
    global draw_best_distance
    global draw_current_distance
    draw_current_distance = []
    draw_best_distance = []
    result_list = []
    distmat = getdistmat(coordinates)
    numant = 40  # 蚂蚁个数
    numcity = coordinates.shape[0]  # 城市个数
    alpha = 1  # 信息素重要程度因子
    beta = 1  # 启发函数重要程度因子
    rho = 0.1  # 信息素的挥发速度
    Q = 1
    iter = 0
    itermax = 100
    etatable = 1.0 / (distmat + np.diag([1e10] * numcity))  # 启发函数矩阵，表示蚂蚁从城市i转移到城市j的期望程度
    pheromonetable = np.ones((numcity, numcity))  # 信息素矩阵
    pathtable = np.zeros((numant, numcity)).astype(int)  # 路径记录表
    distmat = getdistmat(coordinates)  # 城市的距离矩阵
    lengthaver = np.zeros(itermax)  # 各代路径的平均长度
    lengthbest = np.zeros(itermax)  # 各代及其之前遇到的最佳路径长度
    pathbest = np.zeros((itermax, numcity))  # 各代及其之前遇到的最佳路径长度

    while iter < itermax:
        # 随机产生各个蚂蚁的起点城市
        if numant <= numcity:  # 城市数比蚂蚁数多
            pathtable[:, 0] = np.random.permutation(range(0, numcity))[:numant]
        else:  # 蚂蚁数比城市数多，需要补足
            pathtable[:numcity, 0] = np.random.permutation(range(0, numcity))[:]
            pathtable[numcity:, 0] = np.random.permutation(range(0, numcity))[:numant - numcity]
        length = np.zeros(numant)  # 计算各个蚂蚁的路径距离
        for i in range(numant):
            visiting = pathtable[i, 0]  # 当前所在的城市
            unvisited = set(range(numcity))  # 未访问的城市,以集合的形式存储{}
            unvisited.remove(visiting)  # 删除元素；利用集合的remove方法删除存储的数据内容
            for j in range(1, numcity):  # 循环numcity-1次，访问剩余的numcity-1个城市
                # 每次用轮盘法选择下一个要访问的城市
                listunvisited = list(unvisited)
                probtrans = np.zeros(len(listunvisited))
                for k in range(len(listunvisited)):
                    probtrans[k] = np.power(pheromonetable[visiting][listunvisited[k]], alpha) \
                                * np.power(etatable[visiting][listunvisited[k]], alpha)
                cumsumprobtrans = (probtrans / sum(probtrans)).cumsum()
                cumsumprobtrans -= np.random.rand()
                k = listunvisited[(np.where(cumsumprobtrans > 0)[0])[0]]  # python3中原代码运行bug，类型问题；鉴于此特找到其他方法
                # 通过where（）方法寻找矩阵大于0的元素的索引并返回ndarray类型，然后接着载使用[0]提取其中的元素，用作listunvisited列表中
                # 元素的提取（也就是下一轮选的城市）
                pathtable[i, j] = k  # 添加到路径表中（也就是蚂蚁走过的路径)
                unvisited.remove(k)  # 然后在为访问城市set中remove（）删除掉该城市
                length[i] += distmat[visiting][k]
                visiting = k
            length[i] += distmat[visiting][pathtable[i, 0]]  # 蚂蚁的路径距离包括最后一个城市和第一个城市的距离
            # 包含所有蚂蚁的一个迭代结束后，统计本次迭代的若干统计参数
        lengthaver[iter] = length.mean()
        if iter == 0:
            lengthbest[iter] = length.min()
            pathbest[iter] = pathtable[length.argmin()].copy()
        else:
            if length.min() > lengthbest[iter - 1]:
                lengthbest[iter] = lengthbest[iter - 1]
                pathbest[iter] = pathbest[iter - 1].copy()
            else:
                lengthbest[iter] = length.min()
                pathbest[iter] = pathtable[length.argmin()].copy()
        # 更新信息素
        changepheromonetable = np.zeros((numcity, numcity))
        for i in range(numant):
            for j in range(numcity - 1):
                changepheromonetable[pathtable[i, j]][pathtable[i, j + 1]] += Q / distmat[pathtable[i, j]][
                    pathtable[i, j + 1]]  # 计算信息素增量
            changepheromonetable[pathtable[i, j + 1]][pathtable[i, 0]] += Q / distmat[pathtable[i, j + 1]][pathtable[i, 0]]
        pheromonetable = (1 - rho) * pheromonetable + changepheromonetable  # 计算信息素公式
        iter += 1  # 迭代次数指示器+1
        #print("iter:", iter)
    draw_current_distance = lengthaver
    draw_best_distance = lengthbest

    # 做出平均路径长度和最优路径长度
    
    print(lengthbest[-1])
    output1 = lengthbest[-1]

    # 作出找到的最优路径图
    bestpath = pathbest[-1]
    
    for i in range(len(coordinates)):
        for j in range(len(coordinates)):
            if result_city[j][2] == bestpath[i]:
                result_list.append(result_city[j])


def generate_city(m,n):#m个城市，n个物品，三元组[x,y,物品编号]
    for i in range(m):
        if i<n:
            city.append([random.randint(0,100),random.randint(0,100),i])
        else:
            city.append([random.randint(0,100), random.randint(1, 100),random.randint(0,n-1)])
    print(city)

def choose_city(m,n,city):
    global result_city
    result_city = []
    for i in range(n):
        while True:
            random_city = city[random.randint(0,m-1)]
            if random_city[2] == i:
                result_city.append(random_city)
                break
    #print(result_city)
    return result_city

def choose():
    for i in range(10):
        choose_city(39,25,city)

def draw():
    x = []
    y = []
    for i in range(len(output_list)):
        x.append(output_list[i][0])
        y.append(output_list[i][1])
    x.append(output_list[0][0])
    y.append(output_list[0][1])
    plt.plot(x, y)
    plt.show()

    x = []
    y = []
    for i in range(len(result_current_distance)):
        y.append(result_current_distance[i])
        x.append(i)
    plt.plot(x,y)
    plt.show()

    x = []
    y = []
    for i in range(len(result_best_distance)):
        y.append(result_best_distance[i])
        x.append(i)
    plt.plot(x,y)
    plt.show() 

if __name__ == "__main__":
    generate_city(39,25)
    output2 = 999.999
    starttime = datetime.datetime.now()
    for i in range(100):
        choose_city(39,25,city)
        initial(result_city)
        yiqun()
        if output1 < output2:
            output2 = output1
            output_list = result_list
            result_current_distance = draw_current_distance
            result_best_distance = draw_best_distance
    
    print(output2)
    print(output_list)
    endtime = datetime.datetime.now()
    print(endtime-starttime)
    draw()


    