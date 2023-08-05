from 坐标转换算法.run import Solution
import json
import pprint

# data = [
#     [32, 21],
#     [12, 89],
#     [12, 78],
#     [1, 1]
# ]
#
# data_ = json.dumps(data)
# with open('D:\日常文件\ceium学习\src\Voronoi/test.json', mode='w', encoding='utf-8') as f:
#     f.write(data_)
#
# with open('D:\日常文件\ceium学习\src\Voronoi/test.json', mode='r', encoding='utf-8') as f:
#     data__ = json.load(f)


if __name__ == '__main__':
    json_data = []
    s = Solution(6, 50)
    s.deal()
    for i in range(s.size - 1):
        for j in range(s.size - 1):
            json_data.append(
                s.coordinate_table[i][j] + s.coordinate_table[i][j + 1] + s.coordinate_table[i + 1][j + 1] +
                s.coordinate_table[i + 1][j])
    data_ = json.dumps(json_data)
    with open('D:\日常文件\ceium学习\src\Voronoi/6-50.json', mode='w', encoding='utf-8') as f:
        f.write(data_)