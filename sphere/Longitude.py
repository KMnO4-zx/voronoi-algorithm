# 已知三个坐标，得到三个点的夹角
# 用向量计算
import math


# 经度
class Longitude:
    def __init__(self, coordinate):
        self.coordinate = coordinate  # 改正后坐标
        self.a = [0, 1]  # 标准向量，0°方向

    @classmethod
    def mor(cls, coord):
        # 向量的模长
        return math.sqrt(coord[0] ** 2 + coord[1] ** 2)

    def inner_product(self):
        # 内积
        return self.a[0] * self.coordinate[0] + self.a[1] * self.coordinate[1]

    def cos_val(self):
        # cos的值
        return self.inner_product() / (self.mor(self.a) * self.mor(self.coordinate))

    def get_degrees(self):
        if self.coordinate == [0, 0]:
            return 0.0
        if self.coordinate[0] > 0:
            return math.degrees(math.acos(self.cos_val()))
        else:
            return -math.degrees(math.acos(self.cos_val()))


if __name__ == '__main__':
    li = [[0, 0], [0, 1], [1, 0], [-1, 0], [0, -1], [3, 3], [-3, 3], [-3, -3], [3, -3], [3, 0], [2, 2]]
    for li in li:
        s = Longitude(li)
        print(s.get_degrees())
