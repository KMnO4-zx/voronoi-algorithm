from Longitude import Longitude
from Latitude import Latitude
import math
import random
import numpy as np
from PIL import Image
import copy
import pprint
from math import cos, sin, pi, acos
from tqdm import tqdm
from symmetry import Symmetry
import pprint


class Solution:
    def __init__(self, n, seed):
        self.n = n  # 层数
        self.size = 2 ** n + 1  # 边长
        self.seed = seed
        self.seed_list = self.create_seed()
        self.R = 6371  # 地球半径 6371km
        self.table = [[0] * self.size for _ in range(self.size)]
        self.color = self.colors()
        self.visited = [[False] * self.size for _ in range(self.size)]
        self.count = self.size * 4 - 4
        self.coordinate_table = self.coordinate_table()
        self.ori_table = self.ori_table()

    def coordinate_table(self):
        res = [[[]] * self.size for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                res[i][j] = self.get_la([i, j])
        return res

    def ori_table(self):
        res = [[[]] * self.size for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                res[i][j] = self.get_real([i, j])
        return res

    def colors(self):
        res = [[0, 0, 0]]  # 第一个颜色是种子点的颜色
        for _ in range(self.seed):
            res.append([random.randrange(99, 206) for _ in range(3)])
        return res

    def get_la_long(self, coord):
        # 输入为原点移动过后的坐标 纬度在纬度文件中以进行过处理 所以这里并不需要处理
        latitude = Latitude(self.n).get_longitude(coord)  # 纬度
        # 如果为南半球的点，则首先进行对称
        if not Symmetry(self.n).inner(coord):
            coord = Symmetry(self.n).symmetry(coord)
        longitude = Longitude(coord).get_degrees()  # 经度
        return [longitude, latitude]

    def get_real(self, coord):
        return [coord[0] - self.size // 2, coord[1] - self.size // 2]

    def create_seed(self):
        res = []
        for _ in range(self.seed):
            res.append(self.get_la_long(self.get_real(
                [random.randrange(self.size), random.randrange(self.size)])))
        return res

    @classmethod
    def degree_to_pi(cls, degree):
        return (degree / 180) * math.pi

    def arc_distance(self, coord1, coord2):
        # coordinate 为经纬度坐标 根据公式得出地球表面的大弧距离, coordinate[0]:经度； coordinate[1]纬度；
        coord1 = [self.degree_to_pi(coord1[0]), self.degree_to_pi(coord1[1])]
        coord2 = [self.degree_to_pi(coord2[0]), self.degree_to_pi(coord2[1])]
        return self.R * acos(
            self.degree_to_pi(
                cos(coord1[1]) * cos(coord2[1]) * cos(coord1[0] - coord2[0]) + sin(coord1[1]) * sin(coord2[1])))

    def attribution(self, coord):
        # 参数为经纬度坐标
        dic = float('inf')
        res = []
        for i in range(self.seed):
            tmp = self.arc_distance(coord, self.seed_list[i])
            if tmp < dic:
                res.append(i)
                dic = tmp
        return res[-1] + 1

    def get_la(self, coord):
        # 输入为 原始[i ,j]
        return self.get_la_long(self.get_real(coord))

    def deal(self):
        # top deal
        for j in range(self.size):
            self.table[0][j] = self.attribution(self.get_la([0, j]))
            self.visited[0][j] = True
        # bottom deal
        for j in range(self.size):
            self.table[self.size -
                       1][j] = self.attribution(self.get_la([self.size - 1, j]))
            self.visited[self.size - 1][j] = True
        # left deal
        for i in range(self.size):
            self.table[i][0] = self.attribution(self.get_la([i, 0]))
            self.visited[i][0] = True
        # right deal
        for i in range(self.size):
            self.table[i][self.size -
                          1] = self.attribution(self.get_la([i, self.size - 1]))
            self.visited[i][self.size - 1] = True

    def positive_search(self):
        copy_table = copy.deepcopy(self.table)
        for i in range(1, self.size - 1):
            for j in range(1, self.size - 1):
                if self.get_la([i, j]) not in self.seed_list:
                    if copy_table[i][j - 1] == copy_table[i - 1][j - 1] == copy_table[i - 1][j] == copy_table[i - 1][
                            j + 1]:
                        copy_table[i][j] = copy_table[i][j - 1]
                    else:
                        self.visited[i][j] = True
                        self.count += 1
                        copy_table[i][j] = self.attribution(
                            self.get_la([i, j]))
        return copy_table

    def positive_reverse(self):
        # 正向扫描
        copy_table = self.positive_search()
        # 逆向纠错
        for i in range(self.size - 2, 0, -1):
            for j in range(self.size - 2, 0, -1):
                if self.get_la([i, j]) not in self.seed_list:
                    if copy_table[i][j - 1] == copy_table[i - 1][j - 1] == copy_table[i - 1][j] == copy_table[i - 1][
                        j + 1] == copy_table[i][j + 1] == copy_table[i + 1][j + 1] == copy_table[i + 1][j] == \
                            copy_table[i + 1][j - 1]:
                        pass
                    else:
                        if not self.visited[i][j]:
                            copy_table[i][j] = self.attribution(
                                self.get_la([i, j]))
                            self.visited[i][j] = True
                            self.count += 1
        return copy_table

    def attribution_algorithm(self):
        copy_table = copy.deepcopy(self.table)
        for i in range(1, self.size - 1):
            for j in range(1, self.size - 1):
                if self.get_la([i, j]) not in self.seed_list:
                    copy_table[i][j] = self.attribution(self.get_la([i, j]))
        return copy_table

    @classmethod
    def paint(cls, data, name, colors):
        image = Image.new('RGB', (len(data), len(data[0])))
        put_pixel = image.putpixel
        for i in tqdm(range(len(data))):
            for j in range(len(data[0])):
                color = colors[data[i][j]]
                put_pixel((i, j), (color[0], color[1], color[2]))
        image.save(f'img/{name}.jpg')

    @classmethod
    def paint_visited(cls, data, name):
        image = Image.new('RGB', (len(data), len(data[0])))
        put_pixel = image.putpixel
        for i in tqdm(range(len(data))):
            for j in range(len(data[0])):
                if data[i][j]:
                    put_pixel((i, j), (255, 0, 0))
                else:
                    put_pixel((i, j), (255, 255, 255))
        image.save(f'img/{name}.jpg')


if __name__ == '__main__':
    s = Solution(3, 5)
    s.deal()
    print(s.seed_list)
    pprint.pprint(s.table)
    pprint.pprint(s.positive_reverse())
    # pprint.pp(s.color)
    # pprint.pp(s.coordinate_table)
    # positive_reverse = s.positive_reverse()
    # attribution_algorithm = s.attribution_algorithm()
    # s.paint(positive_reverse, 'positive_reverse', s.color)
    # s.paint(attribution_algorithm, 'attribution_algorithm', s.color)
    # s.paint_visited(s.visited, 'visited')
    # i, j = 5, 5
    # print(s.coordinate_table[i][j] + s.coordinate_table[i][j + 1] + s.coordinate_table[i + 1][j + 1] +
    #       s.coordinate_table[i + 1][
    #           j])
