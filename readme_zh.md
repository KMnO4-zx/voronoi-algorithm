# An algorithm using edge attribution and bilateral scanning to generate spherical raster Voronoi diagrams

## 目录

```
|--pnae
	|--img
	|--centroid_voronoi.py
	|--pane_voronoi.py
|--Latitude.py
|--Longitude.py
|--symmetry.py
|--run.py
|--requirements.txt
|--readme.md
```

## 介绍

- `pane`：这个目录下存放平面质心`Voronoi`图的生成算法，如果不想生成质心`Voronoi`图，那只需要把迭代次数设置为`1`即可。


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

## 引用

如果您觉得我的工作对您有帮助，请考虑引用下列论文~

```
@article{{0},
 author = {Wang Lei, Song Zhixue, Yin Nan &amp; Cheng Gang},
 title = {A Raster Voronoi Diagram Generating Algorithm Using Edge Attribution and Bilateral Scanning},
 journal = {Geomatics and Information Science of Wuhan University},
 volume = {},
 number = {},
 year = {},
 issn = {1671-8860},
 doi ={10.13203/j.whugis20220110}
 }
```

