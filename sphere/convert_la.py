#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   convert_la.py
@Time    :   2023/09/23 21:05:57
@Author  :   不要葱姜蒜
@Version :   1.0
@Desc    :   None
'''
import math
from Longitude import Longitude
from Latitude import Latitude
from symmetry import Symmetry


# 平面坐标转为经纬度坐标
def convert_la(n, coord):
    # n: 层数
    # coord: 平面坐标
    size = 2 ** n + 1  # 边长
    coord = [coord[0] - size // 2, coord[1] - size // 2]
    # 输入为原点移动过后的坐标 纬度在纬度文件中以进行过处理 所以这里并不需要处理
    latitude = Latitude(n).get_longitude(coord)  # 纬度
    # 如果为南半球的点，则首先进行对称
    if not Symmetry(n).inner(coord):
        coord = Symmetry(n).symmetry(coord)
    longitude = Longitude(coord).get_degrees()  # 经度
    return [longitude, latitude]

def calculate_center(coordinates):
    num_coords = len(coordinates)
    x = 0.0
    y = 0.0
    z = 0.0

    # 计算三维坐标的累加和
    for lon, lat in coordinates:
        lat_rad = math.radians(lat)
        lon_rad = math.radians(lon)

        x += math.cos(lat_rad) * math.cos(lon_rad)
        y += math.cos(lat_rad) * math.sin(lon_rad)
        z += math.sin(lat_rad)

    # 计算平均值
    x /= num_coords
    y /= num_coords
    z /= num_coords

    # 将三维坐标转换为经纬度坐标
    center_lon = math.atan2(y, x)
    center_lat = math.atan2(z, math.sqrt(x * x + y * y))

    # 将弧度转换为度数
    center_lon = math.degrees(center_lon)
    center_lat = math.degrees(center_lat)

    return [center_lon, center_lat]


