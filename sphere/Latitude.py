import math
from symmetry import Symmetry


# 纬度
class Latitude:
    def __init__(self, n):
        self.n = n
        self.size = 2 ** self.n + 1
        self.quadrant = [[-1, self.size // 2], [1, self.size //
                                                2], [-1, -(self.size // 2)], [1, -(self.size // 2)]]

    def have_0(self, coord):
        # x 或者 y 为 0
        if coord[0] == 0:
            return (1 - (abs(coord[1]) / (self.size // 2))) * 90
        elif coord[1] == 0:
            return (1 - (abs(coord[0]) / (self.size // 2))) * 90

    def get_node(self, coord):
        # 得到交点
        res = [0, 0]
        quadrant = Symmetry(self.n).get_quadrant(coord)  # 象限
        coefficient_ = self.quadrant[quadrant]
        res[0] = coefficient_[1] / ((coord[1] / coord[0]) - coefficient_[0])
        res[1] = coefficient_[0] * res[0] + coefficient_[1]
        return res

    def get_longitude(self, coord):
        # 如果为原点，或对称后为原点
        if coord == [0, 0]:
            return 90.0
        elif Symmetry(self.n).symmetry(coord) == [0, 0]:
            return -90.0
        # 判断点是否在北半球
        if Symmetry(self.n).inner(coord):  # 在北半球，返回正值
            if coord[0] == 0 or coord[1] == 0:
                return self.have_0(coord)
            node = self.get_node(coord)
            return (1 - self.distance(coord) / self.distance(node)) * 90.0
        else:  # 在南半球，返回负值
            coord_ = Symmetry(self.n).symmetry(coord)
            if coord_[0] == 0 or coord_[1] == 0:
                return -self.have_0(coord_)
            node = self.get_node(coord_)
            return -(1 - self.distance(coord_) / self.distance(node)) * 90.0

    @classmethod
    def distance(cls, coord):
        return math.sqrt(coord[0] ** 2 + coord[1] ** 2)


if __name__ == '__main__':
    l = Latitude(2)
    print(l.get_longitude([-2, -1]))
    print(l.get_longitude([-1, 0]))
