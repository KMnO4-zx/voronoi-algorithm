import math
from PIL import Image
from tqdm import tqdm
import random
import numpy as np
import concurrent.futures
from scipy.spatial import KDTree

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

def calculate_voronoi_segment(height, width, seed_list, row_start, row_end, progress_bar):
    segment = np.zeros((row_end - row_start, width))
    tree = KDTree(seed_list)  # 使用KD树优化搜索

    for row in range(row_start, row_end):
        for col in range(width):
            point = index_to_lat_lon_scaled(row, col, height, width)
            _, nearest_index = tree.query(point)  # 查找最近的种子点
            segment[row - row_start, col] = nearest_index + 1

        progress_bar.update(1)  # 更新进度条

    return segment

def voronoi_data_parallel(width, height, seed_list):
    data = np.zeros((height, width))
    num_threads = 4  # 或者根据您的系统情况调整
    segment_height = height // num_threads

    progress_bars = [tqdm(total=segment_height, position=i, desc=f"Thread {i+1}") for i in range(num_threads)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(calculate_voronoi_segment, height, width, seed_list, i * segment_height, (i + 1) * segment_height, progress_bars[i]) for i in range(num_threads)]

        for i, future in enumerate(futures):
            data[i * segment_height:(i + 1) * segment_height, :] = future.result()
            progress_bars[i].close()

    return data


# 示例：假设矩阵尺寸为 90x180，转换几个矩阵索引
scaled_height = 90*30
scaled_width = 180*30
scaled_example_indices = [(0, 0), (scaled_height-1, scaled_width-1), (scaled_height//2, scaled_width//2), [32, 90]]
scaled_lat_lon_examples = [index_to_lat_lon_scaled(row, col, scaled_height, scaled_width) for row, col in scaled_example_indices]
print(scaled_lat_lon_examples)

# 测试函数 - 计算从巴黎到伦敦的距离
distance_paris_london = haversine_distance([2.3522, 48.8566], [-0.1278, 51.5074])
print(distance_paris_london)

seeds = [[-40.891272606653786, 69.62248179646832],
 [158.2437635508901, 84.6616154936666],
 [-6.974626582920479, -89.3772213640066],
 [7.674911824158016, 2.217542454332502],
 [27.378055560049262, 84.51470656586065],
 [18.800193947689024, 89.16975451693608],
 [9.540933101952021, 64.99396519075691],
 [108.54274776611874, 77.05157138597946],
 [156.68514286458407, -70.73050104822089],
 [-163.97445221521363, -27.96264162068627]]

v_data = voronoi_data(scaled_width, scaled_height, seeds)
paint_map(v_data, 'test', [[0, 0, 0]] + [[random.randrange(99, 206) for _ in range(3)] for _ in range(10)])