#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   population.py
@Time    :   2023/09/25 16:33:00
@Author  :   不要葱姜蒜
@Version :   1.0
@Desc    :   None
'''


from osgeo import gdal


# 打开.tif文件
dataset = gdal.Open('./landscan-global-2021-colorized.tif')

# 读取波段数据
data = dataset.ReadAsArray()


# 文件代码还没有测试极端情况，比如在经纬度为-90，180的情况，不知道会不会溢出

def get_population(coord):
    # 密度表
    density = {
        "0,0,0,0": 0,
        "255,255,190,255": 1,
        "255,255,115,255": 2,
        "255,255,0,255": 3,
        "255,170,0,255": 4,
        "255,102,0,255": 5,
        "255,0,0,255": 16,
        "204,0,0,255": 21,
        "115,0,0,255": 32,
    }
    # coord：经纬度,经度在前。
    height, width = -1, -1
    # 纬度
    if coord[1] >= 0:  # 北半球
        height = int((90 - coord[1]) * 120)
    elif coord[1] == -90:  # 南极点
        height = 0
    else:  # 南半球
        height = int((abs(coord[1]) + 90) * 120)
    # 经度
    width = int((180 + coord[0]) * 120)
    color = data.transpose(1, 2, 0)[height][width]
    color = ','.join(map(str, color))
    return density[color] 



dataset = None

# # 关闭数据集
# dataset = None
if __name__ == '__main__':
    coords = [[0, -90.0], [-90.0, -67.5], [-90.0, -45.0], [-90.0, -22.5], [-90.0, -22.5], [-90.0, -45.0], [-90.0, -67.5], [0.0, -90.0], [-116.56505117707799, -22.5], [-63.43494882292201, -22.5], [-45.00000000000001, -45.0], [-0.0, -67.5], [-0.0, -67.5], [0.0, -90.0], [0.0, -90.0]]
    for coord in coords:
        print(get_population(coord))