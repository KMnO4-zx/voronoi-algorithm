#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   centroid_run.py
@Time    :   2023/09/24 10:19:05
@Author  :   不要葱姜蒜
@Version :   1.0
@Desc    :   None
'''

import random, pprint, json, pprint
from collections import defaultdict
import numpy as np
from run import SphersVoronoi
from convert_la import convert_la, calculate_center
import math
from tqdm import tqdm
from PIL import Image

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

def haversine_distance(coordinates1, coordinates2):
    """
    使用哈弗辛公式计算两个经纬度坐标之间的距离。

    :param coordinates1: 第一个坐标的经纬度，格式为 [经度, 纬度]
    :param coordinates2: 第二个坐标的经纬度，格式为 [经度, 纬度]
    :return: 两点之间的距离（千米）
    """
    lon1, lat1 = coordinates1
    lon2, lat2 = coordinates2

    # 将经纬度转换为弧度
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # 计算经纬度差值
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # 应用哈弗辛公式
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # 地球平均半径（千米）
    R = 6371

    # 计算总距离
    distance = R * c
    return distance

def index_to_lat_lon_scaled(row_index, col_index, height, width):
    """
    将缩放后的矩阵索引转换为经纬度坐标。

    :param row_index: 矩阵的行索引
    :param col_index: 矩阵的列索引
    :param height: 矩阵的总行数
    :param width: 矩阵的总列数
    :return: 对应的经度和纬度
    """
    # 根据矩阵尺寸调整经纬度的计算
    longitude = (col_index * 360 / width) - 180
    latitude = 90 - (row_index * 180 / height)
    return [longitude, latitude]


def voronoi_data(width, height, seed_list):
    """
    使用种子点列表计算 Voronoi 图。

    :param width: 矩阵的宽度
    :param height: 矩阵的高度
    :param seed_list: 种子点列表，格式为 [[经度, 纬度], ...]
    :return: 二维数组，表示每个像素点所属的种子点
    """
    # 创建一个空的矩阵
    data = [[0] * width for _ in range(height)]

    # 计算每个像素点的种子点
    print("******计算地图图像数据******")
    for row in tqdm(range(height)):
        for col in range(width):
            # 计算当前像素点到每个种子点的距离
            distances = [haversine_distance(index_to_lat_lon_scaled(row, col, height, width), seed) for seed in seed_list]

            # 找到最近的种子点
            closest_seed = min(distances)

            # 将当前像素点分配给最近的种子点
            seed_index = distances.index(closest_seed)
            data[row][col] = seed_index + 1

    return data

def paint_map(data, filename, colors):
    width = len(data[0])
    height = len(data)
    image = Image.new('RGB', (width, height))
    put_pixel  = image.putpixel
    print("******绘制图像******")
    for row in tqdm(range(height)):
        for col in range(width):
            color = colors[data[row][col]]
            put_pixel((col, row), (color[0], color[1], color[2]))
    image.save(f"{filename}.jpg")


if __name__== "__main__":
    n = 8 # 层数
    size = 2 ** n + 1 # 边长
    seed_num = 100 # 种子点数量
    step = 3 # 质心迭代次数
    # 假设矩阵尺寸为 90x180，转换几个矩阵索引
    scaled_height = 90*30
    scaled_width = 180*30
    # 颜色
    colors = [[0, 0, 0]] + [[random.randrange(99, 206) for _ in range(3)] for _ in range(seed_num)] # 随机颜色列表
    seed_list = [convert_la(n, [random.randrange(size), random.randrange(size)]) for _ in range(seed_num)] # 种子点列表

    for i in range(step):
        print('第{}次迭代'.format(i+1))
        sv = SphersVoronoi(n, seed_list)
        sv.deal()
        data = sv.positive_reverse()
        # 保存可被Cesium使用的json文件
        # with open(f'./data/{n}-{seed_num}-{i+1}.json', mode='w', encoding='utf-8') as f:
        #     f.write(str(json.dumps(cesium_paint(n, data, colors))))
        # 保存为png图片
        # sv.paint(data, 'positive_reverse_sphere_{}.png'.format(i+1), colors)
        seed_list = next_seeds(n, data)
    
    v_data = voronoi_data(scaled_width, scaled_height, seed_list)
    paint_map(v_data, f'./img/voronoi_sphere-{scaled_height}-{scaled_width}-{seed_num}', colors)
