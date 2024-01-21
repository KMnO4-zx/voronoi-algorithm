#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   voronoi_21.py
@Time    :   2024/01/21 10:50:34
@Author  :   不要葱姜蒜
@Version :   1.0
@Desc    :   None
'''
import math, json, pprint, random
from tqdm import tqdm
import copy
from PIL import Image

from convert_la import convert_la, calculate_center, calculate_weighted_center

"""
    改进Voronoi算法 使用更高效扫描流程。

"""

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
    # 计算种子点归属
    def attribute(coordinates, seed_list):
        # coordinates: 当前像素点的经纬度
        # 计算种子点距离
        distances = [haversine_distance(coordinates, seed) for seed in seed_list]
        # 找到最近的种子点
        nearest_seed = distances.index(min(distances))
        return nearest_seed + 1

    # 处理边缘归属
    def deal(data):
        data = data.copy()
        # top 
        print('******处理边缘点 top******')
        for j in tqdm(range(width)):
            data[0][j] = attribute(index_to_lat_lon_scaled(0, j, height, width), seed_list)
        # bottom
        print('******处理边缘点 bottom******')
        for j in tqdm(range(width)):
            data[height - 1][j] = attribute(index_to_lat_lon_scaled(height - 1, j, height, width), seed_list)
        # left
        print('******处理边缘点 left******')
        for i in tqdm(range(1, height-1)):
            data[i][0] = attribute(index_to_lat_lon_scaled(i, 0, height, width), seed_list)
        # right
        print('******处理边缘点 right******')
        for i in tqdm(range(1, height-1)):
            data[i][width - 1] = attribute(index_to_lat_lon_scaled(i, width - 1, height, width), seed_list)
        return data

    # 正向扫描
    def positive_search(data):
        copy_data = copy.deepcopy(data)
        for i in tqdm(range(1, height - 1)):
            for j in range(1, width - 1):
                if copy_data[i][j - 1] == copy_data[i - 1][j - 1] == copy_data[i - 1][j] == copy_data[i - 1][j + 1]:
                    copy_data[i][j] = copy_data[i][j - 1]
                else:
                    if not visit[i][j]:
                        copy_data[i][j] = attribute(index_to_lat_lon_scaled(i, j, height, width), seed_list)
                        visit[i][j] = 1
                    else:
                        pass
        return copy_data
    
    # 逆向纠错
    def positive_reverse(data):
        data = data.copy()
        # 正向扫描
        print("******正向扫描开始******")
        data = positive_search(data)
        # 逆向纠错
        print("******纠错扫描开始******")
        for i in tqdm(range(height - 2, 0, -1)):
            for j in range(width - 2, 0, -1):
                if data[i][j + 1] == data[i + 1][j + 1] == data[i + 1][j] == data[i + 1][j - 1] == data[i][j - 1] == data[i - 1][j - 1] == data[i - 1][j] == data[i - 1][j + 1]:
                    pass
                else:
                    if not visit[i][j]:
                        data[i][j] = attribute(index_to_lat_lon_scaled(i, j, height, width), seed_list)
                        visit[i][j] = 1
                    else:
                        pass
        return data


    # 创建一个空的矩阵
    data = [[0] * width for _ in range(height)]

    # 创建一个访问数组，被计算过的点会被标记为 1
    visit = [[0] * width for _ in range(height)]
    
    # 计算边缘点的Voronoi归属
    data = deal(data)

    # voronoi data
    v_data = positive_reverse(data)

    return v_data

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

if __name__=='__main__':
    n = 9 # 层数
    size = 2 ** n + 1 # 边长
    seed_num = 2000 # 种子点数量
    step = 32 # 质心迭代次数
    scaled_height = 90*90
    scaled_width = 180*90
    colors = [[0, 0, 0]] + [[random.randrange(99, 206) for _ in range(3)] for _ in range(seed_num)] # 随机颜色列表
    # seed_list = [convert_la(n, [random.randrange(size), random.randrange(size)]) for _ in range(seed_num)] # 种子点列表
    with open('./data/population-seed-9-2000-32.json', mode='r', encoding="utf-8") as f:
        seed_list = json.load(f)
    # print(len(seed_list), seed_list[0])
    vor_data = voronoi_data(scaled_width, scaled_height, seed_list)
    paint_map(vor_data, 'test_90', colors)