import math


def haversine(lat1, long1, lat2, long2):
    """

    The haversine formula determines the 
    great-circle distance between two points 
    on a sphere given their longitudes and latitudes.

    Parameters:
    lat1 (Number): Latitude of the first point
    lonng1 (Number): Longitud of the first point
    lat2 (Number): Latitude of the second point
    lonng2 (Number): Longitud of the second point

    Returns:
    distance: The distance between tow point in the earth surface

    """
    rLat1 = math.radians(lat1)
    rLong1 = math.radians(long1)
   
    rLat2 = math.radians(lat2)
    rLong2 = math.radians(long2)
    
    dLat = rLat2 - rLat1
    dLong = rLong2 - rLong1

    # haversine formula using the earth radius
    a = math.sin(dLat/2)**2 + math.cos(rLat1) * math.cos(rLat2) \
        * math.sin(dLong/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = 6371 * c

    return distance

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