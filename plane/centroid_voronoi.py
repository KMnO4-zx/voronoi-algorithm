#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   centroid_voronoi.py
@Time    :   2023/09/21 20:00:45
@Author  :   不要葱姜蒜
@Version :   1.0
@Desc    :   None
'''

import random, pprint
from collections import defaultdict
from pane_voronoi import PaneVoronoi
import numpy as np

def next_seeds(voronoi_data):
    # voronoi_data: 二维数组，上一次迭代的结果
    res = [] # 用于存储每个种子点的坐标
    voronoi_regin = defaultdict(list)
    for i in range(len(voronoi_data)):
        for j in range(len(voronoi_data[0])):
            if voronoi_data[i][j] != 0:
                voronoi_regin[voronoi_data[i][j]].append([i, j])
    for key, value in voronoi_regin.items():
        tmp_x, tmp_y = [], []
        for x, y in value:
            tmp_x.append(x)
            tmp_y.append(y)
        res.append([np.mean(tmp_x), np.mean(tmp_y)])
    return res

n = 800 # 边长
step = 25 # 质心迭代次数
seed_num = 32 # 种子点个数

seed_init = [[random.randrange(n), random.randrange(n)] for _ in range(seed_num)] # 种子点列表
colors = [[0, 0, 0]] + [[random.randrange(99, 206) for _ in range(3)] for _ in range(seed_num)] # 随机颜色列表

for i in range(step):
    print('第{}次迭代'.format(i+1))
    pv = PaneVoronoi(seed=seed_num, seed_list=seed_init, n=n)
    pv.deal()
    data = pv.positive_reverse()
    pv.paint(data, 'positive_reverse_{}.png'.format(i+1), colors)
    seed_init = next_seeds(data)
    # pprint.pprint(data) 
    # print(seed_init)


