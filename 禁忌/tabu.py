#!/usr/bin/python
#_*_ coding:utf-8 _*_  
#实验需要修改的参数 n generate_city(,) choose_city(,,city) tabu_limit temp
import math
import random
import numpy as np 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
from numpy.core.records import array
from numpy.lib.function_base import append
from numpy.matlib import rand
#from matplotlib.mlab import dist
from matplotlib.artist import getp
import copy
#from test.test__locale import candidate_locales
from cProfile import run

from typing_extensions import runtime
import datetime

#城市、物品数量
n = 25

city=[]#用于生产随机城市
result_city = []
output1 = 0.0

city_x = []
city_y = []
distance = []
draw_current_distance = []#某一次大循环中的当前和最优举例
draw_best_distance = []
result_current_distance = []#最优的一次中的当前和最优距离
result_best_distance = []
#初始城市坐标
def initialization(arr):
    input_array = arr
    
    for i in range(n):
        city_x.append(input_array[i][0])
        city_y.append(input_array[i][1])

distance = [[0 for col in range(n)] for raw in range(n)]



#禁忌表
tabu_list = []
tabu_time = []
#当前禁忌对象数量
current_tabu_num = 0
#禁忌长度，即禁忌期限
tabu_limit = 200
#候选集
candidate = [[0 for col in range(n)] for raw in range(200)]
candidate_distance = [0 for col in range(200)]
#最佳路径以及最佳距离
best_route = []
best_distance = sys.maxsize
current_route = []
current_distance = 0.0

def greedy():
    #通过贪心算法确定  
    sum = 0.0
    #必须实例化一个一个赋值，不然只是把地址赋值，牵一发而动全身
    dis = [[0 for col in range(n)] for raw in range(n)]
    for i in range(n):
        for j in range(n):
            dis[i][j] = distance[i][j]
                
    visited = []
        #进行贪心选择——每次都选择距离最近的
    id = 0
    for i in range(n):
        for j in range(n):
            dis[j][id] = sys.maxsize
        minvalue = min(dis[id])
        if i != 29:
            sum += minvalue
        visited.append(id)
        id = dis[id].index(minvalue)
    sum += distance[0][visited[n-1]]
    return visited


#构建初始参考距离矩阵
def getdistance():
    for i in range(n):
        for j in range(n):
            x = pow(city_x[i] - city_x[j], 2)
            y = pow(city_y[i] - city_y[j], 2)
            distance[i][j] = pow(x + y, 0.5)
    for i in range(n):
        for j in range(n):
            if distance[i][j] == 0:
                distance[i][j] = sys.maxsize
                
#计算总距离
def cacl_best(rou):
    sumdis = 0.0
    for i in range(n-1):
        sumdis += distance[rou[i]][rou[i+1]]
    sumdis += distance[rou[n-1]][rou[0]]     
    return sumdis

#初始设置
def setup():
    global best_route
    global best_distance
    global tabu_time
    global current_tabu_num
    global current_distance
    global current_route
    global tabu_list
    #得到初始解以及初始距离
    #current_route = random.sample(range(0, n), n) 
    current_route = greedy()
    best_route = copy.copy(current_route)
    #函数内部修改全局变量的值
    current_distance = cacl_best(current_route)
    best_distance = sys.maxsize
    
    #置禁忌表为空
    tabu_list.clear()
    tabu_time.clear()
    current_tabu_num = 0

#交换数组两个元素
def exchange(index1, index2, arr):
    current_list = copy.copy(arr)
    current = current_list[index1]
    current_list[index1] = current_list[index2]
    current_list[index2] = current
    return current_list
    
    
#得到邻域 候选解
def get_candidate():
    global best_route
    global best_distance
    global current_tabu_num
    global current_distance
    global current_route
    global tabu_list
    #存储两个交换的位置
    exchange_position = []
    temp = 0
    #随机选取邻域
    while True:
        current = random.sample(range(0, n), 2)
        #print(current)
        if current not in exchange_position:
            exchange_position.append(current)
            candidate[temp] = exchange(current[0], current[1], current_route)
            if candidate[temp] not in tabu_list:
                candidate_distance[temp] = cacl_best(candidate[temp])
                temp += 1
            if temp >= 200:
                break
            
    
    #得到候选解中的最优解
    candidate_best = min(candidate_distance)
    best_index = candidate_distance.index(candidate_best)
    
    
    current_distance = candidate_best
    current_route = copy.copy(candidate[best_index])
    #与当前最优解进行比较 
    
    if current_distance < best_distance:
        best_distance = current_distance
        best_route = copy.copy(current_route)
    
    #加入禁忌表
    tabu_list.append(candidate[best_index])
    tabu_time.append(tabu_limit)
    current_tabu_num += 1    

    #存储路径长度
    draw_current_distance.append(current_distance)
    draw_best_distance.append(best_distance)
    
#更新禁忌表以及禁忌期限
def update_tabu():
    global current_tabu_num
    global tabu_time
    global tabu_list
    
    del_num = 0
    temp = [0 for col in range(n)]
    #更新步长
    tabu_time = [x-1 for x in tabu_time]
    #如果达到期限，释放
    for i in range(current_tabu_num):
        if tabu_time[i] == 0:
            del_num += 1
            tabu_list[i] = temp
           
    current_tabu_num -= del_num        
    while 0 in tabu_time:
        tabu_time.remove(0)
    
    while temp in tabu_list:
        tabu_list.remove(temp)
    
    
    
def draw():
    result_x = [0 for col in range(n+1)]
    result_y = [0 for col in range(n+1)]
    
    for i in range(n):
        result_x[i] = city_x[best_route[i]]
        result_y[i] = city_y[best_route[i]]
    result_x[n] = result_x[0]
    result_y[n] = result_y[0]
    #print(result_x)
    #print(result_y)
    plt.xlim(0, 100)  # 限定横轴的范围
    plt.ylim(0, 100)  # 限定纵轴的范围
    plt.plot(result_x, result_y)
    plt.xlabel(u"x") #X轴标签
    plt.ylabel(u"y") #Y轴标签
    
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
    
    #print(result_current_distance)
    #print(result_best_distance)
                
def solve():
    global draw_current_distance
    global draw_best_distance
    global result_current_distance
    global result_best_distance

    output2 = 999.999
    generate_city(39,25)
    for i in range(100):
        draw_current_distance = []
        draw_best_distance = []
        choose_city(39,25,city)
        initialization(result_city)
        getdistance()
        runtime = 500
        # 迭代次数
        setup()
        for rt in range(runtime):
            get_candidate()
            update_tabu()
        if best_distance < output2:
            output2 = best_distance
            result_best_distance = draw_best_distance
            result_current_distance = draw_current_distance
    
    print("当前距离：")
    print(current_distance)
    print(current_route)
    print("最优距离：")    
    print(best_route)
    print(best_distance)
    draw()    

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

    
if __name__=="__main__":    
    starttime = datetime.datetime.now()
    solve()
    endtime = datetime.datetime.now()
    print(endtime-starttime)
    
