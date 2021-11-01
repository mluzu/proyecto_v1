import os
#os.environ['USE_PATH_FOR_GDAL_PYTHON']='YES'
os.environ['PROJ_LIB'] = 'C:\\Users\\Mariano\\anaconda3\\envs\\geoconda\\Library\\share\\proj'
os.environ['GDAL_DATA'] = 'C:\\Users\\Mariano\\anaconda3\\envs\\geoconda\\Library\\share\\gdal'

from osgeo import ogr


# Cargo el shapefile. Un shapefile es el formato de almacenamiento
# desarrollado por ESRI para vector data. Es en realidad una coleccion
# de archivos
# OGR model se compone de Data Sources, Layers y Features. 
# Features tiene attributes y Geometry
# Vector data model https://gdal.org/user/vector_data_model.html

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


def getRectangleFromGeometry(geometry):
    results = {'N': None, 'S': None, 'W': None, 'E': None}
    def findPoints(geometry, results):
        for i in range(geometry.GetPointCount()):
            x, y, _ = geometry.GetPoint(i)
            if results['N'] == None or results['N'][1] < y:
                results['N'] = (x,y)
            if results['S'] == None or results['S'][1] > y:
                results['S'] = (x,y)
            if results['W'] == None or results['W'][0] < x:
                results['W'] = (x,y)
            if results['E'] == None or results['E'][0] > x:
                results['E'] = (x,y)
        return results
    for i in range(geometry.GetGeometryCount()):
        findPoints(geometry.GetGeometryRef(i), results)
    return results

rectangle = getRectangleFromGeometry(feature.GetGeometryRef())
n, s, w, e = rectangle.values()
print('The area under observation is delimited by the rectangle',
    f'{n}, {s}, {w}, {e}')
