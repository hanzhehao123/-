# -*- encoding: utf-8 -*-
#实验需要修改的参数 generate_city(,) choose_city(,,city) tsp.run()

import random
import math
from matplotlib import pyplot as plt
import datetime
from GA import GA

city = []
result_city = []
result_list = []
output_list = []
output1 = 999.999
draw_current_distance = []#某一次大循环中的当前和最优举例
draw_best_distance = []
result_current_distance = []#最优的一次中的当前和最优距离
result_best_distance = []

class TSP(object):
      def __init__(self, aLifeCount = 100,):
            self.initCitys(arr)
            self.lifeCount = aLifeCount
            self.ga = GA(aCrossRate = 0.7, 
                  aMutationRage = 0.02, 
                  aLifeCount = self.lifeCount, 
                  aGeneLenght = len(self.citys), 
                  aMatchFun = self.matchFun())


      def initCitys(self,arr):
            self.citys = []
          
            input_array = arr
            for i in range(len(input_array)):
                  self.citys.append(input_array[i])
            

            
      def distance(self, order):
            global result_list
            result_list = []
            distance = 0.0
            for i in range(-1, len(self.citys) - 1):
                  index1, index2 = order[i], order[i + 1]
                  city1, city2 = self.citys[index1], self.citys[index2]
                  distance += math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

                  result_list.append(city1)#保存当前解
            return distance


      def matchFun(self):
            return lambda life: 1.0 / self.distance(life.gene)


      def run(self, n = 0):
            global output1
            global draw_best_distance
            global draw_current_distance
            output1 = 999.999
            draw_current_distance = []
            draw_best_distance = []
            while n > 0:
                  self.ga.next()
                  distance = self.distance(self.ga.best.gene)
                  if n % 1000 == 1:
                        print (("%d : %f") % (self.ga.generation, distance))
                  n -= 1
                  if distance < output1:
                        output1 = distance
                  draw_current_distance.append(distance)
                  draw_best_distance.append(output1)


def main(arr):
      tsp = TSP()
      tsp.initCitys(arr)
      tsp.run(1000)

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

if __name__ == '__main__':
      generate_city(39,25)
      output2 = 999.999 #最优解的路经长
      starttime = datetime.datetime.now()
      for i in range(100):
            choose_city(39,25,city)
            arr = result_city
            main(arr)
            if output1 < output2:
                  output2 = output1
                  output_list = result_list
                  result_current_distance = draw_current_distance
                  result_best_distance = draw_best_distance
      
      print(output2)
      print(output_list)#输出最优解
      endtime = datetime.datetime.now()
      print(endtime-starttime)
      draw()
