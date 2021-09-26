
def convert_to_geojson(gdal_feature):
    gj_geom = {}
    geometry = gdal_feature.GetGeometryRef()
    geom_name = geometry.GetGeometryName()
    coordinates = []
    exterior_lring = []
    for i in range(geometry.GetGeometryCount()):
        point = geometry.GetPoint(i)
        exterior_lring.append(point)
    coordinates.append(exterior_lring)
    gj_geom.update({"type": geom_name.lower().capitalize()})
    gj_geom.update({"coordinates": coordinates})
    return gj_geom