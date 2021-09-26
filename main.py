import os
#os.environ['USE_PATH_FOR_GDAL_PYTHON']='YES'
os.environ['PROJ_LIB'] = 'C:\\Users\\Mariano\\anaconda3\\envs\\geoconda\\Library\\share\\proj'
os.environ['GDAL_DATA'] = 'C:\\Users\\Mariano\\anaconda3\\envs\\geoconda\\Library\\share\\gdal'

from osgeo import ogr
#import geojson


# Cargo el shapefile. Un shapefile es el formato de almacenamiento
# desarrollado por ESRI para vector data. Es en realidad una coleccion
# de archivos

shapefiles_path = 'shapefile'
shapefile = ogr.Open(shapefiles_path)

# OGR model se compone de Data Sources, Layers y Features. 
# Features tiene attributes y Geometry
# Vector data model https://gdal.org/user/vector_data_model.html

# miro layers
numLayers = shapefile.GetLayerCount()
print(f'Shapefiles contains {numLayers} layers')
layer = shapefile.GetLayer(0)

# extraigo informacion geoespacial del layer
spatialRef = layer.GetSpatialRef().ExportToProj4()
numFeatures = layer.GetFeatureCount()
print(f'Layer has spatial reference {spatialRef} layers')
print(f'Layer has {numFeatures} reference {spatialRef} layers')

# miro metadata (features)
feature = layer.GetFeature(0)
featureItems = feature.items()
for key, value in featureItems.items():
    print(f'{key} {value}')

# miro la geometria
def analyzeGeometry(geometry, indent=0):
    s = []
    s.append(" " * indent)
    s.append(geometry.GetGeometryName())
    if geometry.GetPointCount() > 0:
        s.append(" with %d data points" % geometry.GetPointCount())
    if geometry.GetGeometryCount() > 0:
        s.append(" containing:")
    print("".join(s))
    for i in range(geometry.GetGeometryCount()):
        analyzeGeometry(geometry.GetGeometryRef(i), indent+1)

geom = feature.GetGeometryRef()
analyzeGeometry(geom, 3)

#-----descarga de imagines con google earth engine------#

import ee
import time
import json
from ee import geometry

# conda install -c conda-forge fiona
# https://fiona.readthedocs.io/en/latest/manual.html
# import fiona


ee.Authenticate()
ee.Initialize()

gj = feature.GetGeometryRef().ExportToJson()
gjObject = json.loads(gj)

#  en EE un Feature esta definido por un GeoJSON que contiene una geometria 
# y propiedades almacenadas en un diccionario
# GeoJSON (RFC7946) https://geojson.org/
geometry = ee.Geometry(gjObject)

# selecciono el catalogo de copernicus sentinel2
image_collection = ee.ImageCollection('COPERNICUS/S2')

# defino filtro geometria
glopez_area = ee.Feature(geometry)

# defino filtro temporal
# Cada camapaña va desde mayo a abril de cada año. 
#Campaña 18/19
camp_1819 = ['2018-05-01', '2019-05-01']
#Campaña 19/20
camp_1920 = ['2019-05-01','2020-05-01']

# filtro el catalogo por geometria, tiempo nubosidad y bandas
camp1819_imagenes = image_collection \
    .filterBounds(geometry) \
    .filterDate(camp_1819[0], camp_1819[1]) \
    .filterMetadata('CLOUDY_PIXEL_PERCENTAGE','less_than', 10)\
    .select(['B1','B2','B3','B4','B5','B6','B7','B8','B8A','B9', 'B11','B12'])

camp1920_imagenes = image_collection \
    .filterBounds(geometry) \
    .filterDate(camp_1920[0], camp_1920[1]) \
    .filterMetadata('CLOUDY_PIXEL_PERCENTAGE','less_than', 10)\
    .select(['B1','B2','B3','B4','B5','B6','B7','B8','B8A','B9', 'B11','B12'])

count = camp1819_imagenes.size();
print(f'Cantidad de imagenes:{count}');

count = camp1920_imagenes.size();
print(f'Cantidad de imagenes:{count}');

# batch permite usar el sistema de ee para ejecutar tareas
# de este modo podemos usar la funcionalidad de la case Export
# para almacenar las imagenes en batches
def export(collection, description):
    params = {
        'description': description,
        'folder':'images',
        'scale': 30,
        'fileFormat': 'GeoTIFF',
    }
    task = ee.batch.Export.image.toDrive(collection, **params)
    task.start()
    while task.active():
            time.sleep(30)
            print(task.status())

export(camp1819_imagenes, 'campania_1819')
export(camp1920_imagenes, 'campania_1920')

