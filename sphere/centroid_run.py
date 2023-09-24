#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   centroid_run.py
@Time    :   2023/09/24 10:19:05
@Author  :   不要葱姜蒜
@Version :   1.0
@Desc    :   None
'''

import random, pprint
from collections import defaultdict
import numpy as np
from run import SphersVoronoi
from convert_la import convert_la, calculate_center


def next_seeds(n, voronoi_data):
    # voronoi_data: 二维数组，上一次迭代的结果
    res = [] # 用于存储每个种子点的坐标
    voronoi_regin = defaultdict(list)
    for i in range(len(voronoi_data)):
        for j in range(len(voronoi_data[0])):
            if voronoi_data[i][j] != 0:
                voronoi_regin[voronoi_data[i][j]].append(convert_la(n, [i, j]))
    for key, value in voronoi_regin.items():
        res.append(calculate_center(value))
    return res

n = 10 # 层数
size = 2 ** n + 1 # 边长
seed_num = 12 # 种子点数量
step = 25 # 质心迭代次数
colors = [[0, 0, 0]] + [[random.randrange(99, 206) for _ in range(3)] for _ in range(seed_num)] # 随机颜色列表
seed_list = [convert_la(n, [random.randrange(size), random.randrange(size)]) for _ in range(seed_num)] # 种子点列表

for i in range(step):
    print('第{}次迭代'.format(i+1))
    sv = SphersVoronoi(n, seed_list)
    sv.deal()
    data = sv.positive_reverse()
    sv.paint(data, 'positive_reverse_sphere_{}.png'.format(i+1), colors)
    seed_list = next_seeds(n, data)

