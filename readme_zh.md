# An algorithm using edge attribution and bilateral scanning to generate spherical raster Voronoi diagrams

## 目录

```
|--Latitude.py
|--Longitude.py
|--symmetry.py
|--run.py
|--requirements.txt
|--readme.md
```

## 介绍


- `latitude .py`:将平面笛卡尔坐标转换为经纬度坐标得到纬度值。
- `longitude .py`:将平面笛卡尔坐标转换为经纬度坐标得到经度值。
- `symmetry.py`:南半球的坐标与北半球对称排列。
- `run.py`:生成球形`Voronoi`图的核心算法，运行这个`python`文件会得到一个二维数组，这个数组存储了`Voronoi`区域中所有点的归属信息。

## Todo

- [x] 平面Voronoi图生成
- [x] 平面质心Voronoi图生成
- [ ] 球面Voronoi图生成
- [ ] 利用Cesium展示球面Voronoi图


## 快速开始

- 克隆仓库

`git clone https://github.com/KMnO4-zx/voronoi-algorithm.git`

- 切换工作目录

`cd voronoi-algorithm`

- 安装依赖

`pip install -r requirements.txt`

- 运行代码

`python run.py`