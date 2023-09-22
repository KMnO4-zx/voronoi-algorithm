# An algorithm using edge attribution and bilateral scanning to generate spherical raster Voronoi diagrams

## Catalogue

```
|--Latitude.py
|--Longitude.py
|--symmetry.py
|--run.py
|--requirements.txt
|--readme.md
```

## Introduction

- `Latitude.py`: The latitude value is obtained by converting the plane Cartesian coordinates to latitude and longitude coordinates.
- `Longitude.py`: The longitude value is obtained by converting the plane Cartesian coordinates to latitude and longitude coordinates.
- `symmetry.py`: The coordinates of the southern Hemisphere are symmetrically aligned to the northern Hemisphere.
- `run.py`: The core algorithm to generate the spherical Voronoi diagram, running this python file will get a two-dimensional array, this array stores the Voronoi area belonging information of all the dots.

## QuickStart

- Clone repository

`git clone https://github.com/KMnO4-zx/voronoi-algorithm.git`

- Enter the repository directory

`cd voronoi-algorithm`

- Install dependency packages

`pip install -r requirements.txt`

- Running code

`python run.py`