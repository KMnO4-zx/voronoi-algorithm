# An algorithm using edge attribution and bilateral scanning to generate spherical raster Voronoi diagrams

&emsp;&emsp;球面Voronoi图是计算几何领域中的一个重要研究方向，其生成算法是该领域的关键技术。现有的球面栅格算法多是由平面算法扩展而来，确定归属算法符合计算机的离散特征，是精度最优的球面栅格Voronoi算法之一，但该算法在海量数据处理时效率不高。针对这一问题，以正八面体剖分格网作为基础，提出一种结合边缘归属与双向扫描的球面Voronoi图生成算法。在深入探究确定归属算法精度优异和效率较低问题的基础上，首先建立球面经纬度坐标与平面坐标的转换关系，优先确定边缘栅格归属，建立3×3邻域扫描模板，进行正向扫描；然后在剖析正向扫描结果的基础上，通过逆向纠错确保所有栅格归属正确；最后利用不同层次的数据进行实验对比。结果表明，本文算法具有与确定归属算法相同的精度，但却省去80%以上的计算量，效率提高四倍以上，且划分的格网数量越多，算法优势越明显。

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

