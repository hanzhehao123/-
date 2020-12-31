import random
import math
import copy
import time
import datetime
from matplotlib import pyplot as plt

city = []  # 城市
thing = []  # 物品
seq = []  # 临时城市排列
last_seq = []
T_start = time.time()
draw_best_distance = []
result_best_distance = []
k = 0.5  # Metroplis准则系数
sec=10#执行秒数

m = 17
n = 11

u = []
v = []

starttime = datetime.datetime.now()

def generate_city(m, n):  # m个城市，n个物品，三元组[x,y,物品编号]
    for i in range(m):
        if i < n:
            city.append([random.randint(0, 100), random.randint(0, 100), i])
        else:
            city.append([random.randint(0, 100), random.randint(0, 100), random.randint(0, n - 1)])


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def calc_seq_sum(seq):
    sum = 0
    for i in range(len(seq) - 1):
        sum += distance(seq[i], seq[i + 1])
    sum += distance(seq[len(seq) - 1], seq[0])
    return sum


def move(seq):
    if random.random() >= 0.5:  # 物品组内交换城市
        for i in range(n):
            tmp_n = []  # 物品号为n的城市集合
            for j in range(m):
                if city[j][2] == i:
                    tmp_n.append(city[j])
            x = random.randint(0, len(tmp_n) - 1)
            seq[i] = copy.deepcopy(tmp_n[x])
    else:  # 交换物品顺序
        for i in range(n):
            x = random.randint(0, n - 1)
            y = random.randint(0, n - 1)
            tmp = copy.deepcopy(seq[x])
            seq[x] = copy.deepcopy(seq[y])
            seq[y] = copy.deepcopy(tmp)


generate_city(m, n)
for i in range(n):  # 初始化排列
    for j in range(m):
        if city[j][2] == i:
            seq.append(city[j])
            break

count = 0  # 画迭代图的计数器
while 1:
    T_now = time.time()
    detaT = T_now - T_start
    if detaT < sec:  # 执行时间
        last_seq = copy.deepcopy(seq)
        move(seq)
        a = calc_seq_sum(seq)
        b = calc_seq_sum(last_seq)
        p = 2.718281828459 ** (-1 * (a - b) / k / (sec - (time.time() - T_start) + 0.5))
        if a <= b:
            last_seq = copy.deepcopy(seq)
        elif p > random.random():
            last_seq = copy.deepcopy(seq)
        else:
            seq = copy.deepcopy(last_seq)
        if a > b:
            print(b, p)
            v.append(b)
            count += 1
            u.append(count)
        else:
            print(a)
            v.append(a)
            count += 1
            u.append(count)
    else:
        break
print(seq)
result = calc_seq_sum(seq)
print(result)
endtime = datetime.datetime.now()
print(endtime-starttime)
print(city)

# 作图部分
x = []
y = []
for i in range(len(seq)):
    x.append(seq[i][0])
    y.append(seq[i][1])
x.append(seq[0][0])
y.append(seq[0][1])
plt.plot(x, y)
plt.show()

uu=[]
vv=[]
for i in range(len(u)):
    if i%100==1:
        uu.append(u[i])
for i in range(len(v)):
    if i%100==1:
        vv.append(v[i])
plt.plot(uu, vv)
#plt.plot(u,v)
plt.show()
