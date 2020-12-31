import random
city=[]
def generate_city(m,n):#m个城市，n个物品，三元组[x,y,物品编号]
    for i in range(m):
        if i<n:
            city.append([random.randint(0,100),random.randint(0,100),i])
        else:
            city.append([random.randint(0,100), random.randint(1, 100),random.randint(0,n-1)])
    print(city)

generate_city(31,16)