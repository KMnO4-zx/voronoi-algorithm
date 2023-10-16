import math


class Symmetry:
    """
        对称过程中没有考虑坐标点是否在北半球，直接对称
    """
    def __init__(self, n):
        self.size = 2 ** n + 1
        # 四象限系数矩阵
        self.quadrant = [[-1, self.size // 2], [1, self.size // 2], [-1, -(self.size // 2)], [1, -(self.size // 2)]]

    @classmethod
    def get_quadrant(cls, coord):
        # 得到坐标点所属的象限
        if coord[0] > 0 and coord[1] >= 0:
            return 0
        elif coord[0] <= 0 and coord[1] > 0:
            return 1
        elif coord[0] < 0 and coord[1] <= 0:
            return 2
        elif coord[0] >= 0 and coord[1] < 0:
            return 3

    def inner(self, coord):
        if coord == [0, 0]: # 原点
            return True
        coefficient = self.quadrant[self.get_quadrant(coord)]
        if self.get_quadrant(coord) < 2:
            if coord[1] <= coefficient[0] * coord[0] + coefficient[1]:
                return True
            else:
                return False
        else:
            if coord[1] >= coefficient[0] * coord[0] + coefficient[1]:
                return True
            else:
                return False

    def symmetry(self, coord):
        coefficient = self.quadrant[self.get_quadrant(coord)]
        A, B, C = coefficient[0], -1, coefficient[1]
        x = coord[0] - 2 * A * ((A * coord[0] + B * coord[1] + C) / (A ** 2 + B ** 2))
        y = coord[1] - 2 * B * ((A * coord[0] + B * coord[1] + C) / (A ** 2 + B ** 2))
        return [x, y]


if __name__ == '__main__':
    s = Symmetry(3)
    li = [0, 1]
    print(s.get_quadrant(li) + 1)
    print(s.inner(li))
    print(s.symmetry(li))
