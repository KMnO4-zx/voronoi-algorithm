#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   population_centroid.py
@Time    :   2023/09/25 21:04:35
@Author  :   不要葱姜蒜
@Version :   1.0
@Desc    :   None
'''

from population import get_population
import random, pprint, json
from collections import defaultdict
import numpy as np
from run import SphersVoronoi
from convert_la import convert_la, calculate_center, calculate_weighted_center


def cesium_paint(n, data, colors):
    # 此函数用于将data数据更改为cesium可用的格式，data为positive_reverse()函数的返回值
    res = []
    for i in range(len(data) - 1):
        for j in range(len(data[0]) - 1):
            left_top = convert_la(n, [i, j])
            right_top = convert_la(n, [i, j + 1])
            left_bottom = convert_la(n, [i + 1, j])
            right_bottom = convert_la(n, [i + 1, j + 1])
            res.append([left_top + right_top + right_bottom + left_bottom, colors[data[i][j]]])
    return res

def population_next_seed(n, voronoi_data):
    res = [] # 用于存储每个种子点的坐标
    voronoi_regin = defaultdict(list)  # 用于存储每个区域的坐标, 经纬度坐标
    for i in range(len(voronoi_data)):
        for j in range(len(voronoi_data[0])):
            if voronoi_data[i][j] != 0:
                voronoi_regin[voronoi_data[i][j]].append(convert_la(n, [i, j]))
    voronoi_keys = list(voronoi_regin.keys())
    for key in voronoi_keys:
        weights = [get_population(coord) for coord in voronoi_regin[key]]
        res.append(calculate_weighted_center(voronoi_regin[key], weights))
    return res
    
n = 9 # 层数
size = 2 ** n + 1 # 边长
seed_num = 1000 # 种子点数量
step = 64 # 质心迭代次数
colors = [[0, 0, 0]] + [[random.randrange(99, 206) for _ in range(3)] for _ in range(seed_num)] # 随机颜色列表
seed_list = [convert_la(n, [random.randrange(size), random.randrange(size)]) for _ in range(seed_num)] # 种子点列表

for i in range(step):
    print('第{}次迭代'.format(i+1))
    sv = SphersVoronoi(n, seed_list)
    sv.deal()
    data = sv.positive_reverse()
    # 保存可被Cesium使用的json文件
    with open(f'./data/population-{n}-{seed_num}-{i+1}.json', mode='w', encoding='utf-8') as f:
        f.write(str(json.dumps(cesium_paint(n, data, colors))))
    # 保存为png图片
    sv.paint(data, 'positive_reverse_sphere_population{}.png'.format(i+1), colors)
    seed_list = population_next_seed(n, data) 