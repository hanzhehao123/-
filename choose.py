import random

city=[]
result_city = []
def generate_city(m,n):#m个城市，n个物品，三元组[x,y,物品编号]
    for i in range(m):
        if i<n:
            city.append([random.randint(0,100),random.randint(0,100),i])
        else:
            city.append([random.randint(0,100), random.randint(1, 100),random.randint(0,n-1)])
    print(city)

def choose_city(m,n,city):#选出刚好可以买到n个物品的n个城市
    result_city = []
    for i in range(n):
        while True:
            random_city = city[random.randint(0,m-1)]
            if random_city[2] == i:
                result_city.append(random_city)
                break
    print(result_city)
    return result_city

def choose():
    for i in range(10):
        choose_city(39,25,city)

generate_city(39,25)
choose_city(39,25,city)
#choose()
