import random
from math import atan2

# 生成随机经纬度坐标点


def generate_random_coordinates(num_points):
    coordinates = []
    for _ in range(num_points):
        # 生成随机的经度和纬度（在一定范围内）
        longitude = random.uniform(-180, 180)
        latitude = random.uniform(-90, 90)
        coordinates.append((longitude, latitude))
    return coordinates

# 计算点的极角


def calculate_polar_angle(point, center):
    x_diff = point[0] - center[0]
    y_diff = point[1] - center[1]
    return atan2(y_diff, x_diff)

# 按顺时针排序坐标点


def sort_coordinates_clockwise(coordinates):
    # 找到最小的纬度作为起始点（最南边的点）
    start_point = min(coordinates, key=lambda point: point[1])

    # 将起始点移至列表首位
    coordinates.remove(start_point)
    coordinates.insert(0, start_point)

    # 使用起始点作为中心点，根据极角排序其余点
    sorted_points = sorted(
        coordinates, key=lambda point: calculate_polar_angle(point, start_point))

    return sorted_points


if __name__=='__main__':

    # 生成5个随机经纬度坐标点
    coors = [[101.78445, 36.62338], [102.85245, 24.87400], [106.55843, 29.56900], [114.31158, 30.59847], [118.80242, 32.06465]]

    # 按顺时针排序这些坐标点
    sorted_coordinates = sort_coordinates_clockwise(coors)
    res = []
    for item in sorted_coordinates:
        res += [item[0], item[1]]
    # 输出排序后的坐标点
    print("随机生成的经纬度坐标点：", coors)
    print("按顺时针排序后的坐标点：", res)
