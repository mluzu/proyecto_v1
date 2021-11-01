import os, sys
import fiona
from datetime import date
from sentinelsat import SentinelAPI, geojson_to_wkt

current_dir =  os.getcwd()
token = 'VKRcAW;pPkBnb88h*Wo{#K%09+~r5u/td1&qe&_o'
user = 'mluzu'
password = 'aufklarung'


shapefilePath = current_dir + "\\shapefile"
print(f'Reading shape file from {shapefilePath}...')
with fiona.open(shapefilePath, "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]

print('Querying products...')
geom = shapes[0]
save_path = current_dir + "\\products\\sentinel21c\\c_1819"
api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')
footprint = geojson_to_wkt(geom)
products = api.query(footprint,
                     date=(date(2018, 5, 1), date(2019, 4, 30)),
                     platformname='Sentinel-2',
                     cloudcoverpercentage=(0, 10),
                     producttype='S2MSI1C')

print(f'\n\nFound products:')
for k in products:
    print(products[k]['title'])

response = input("proceed to download yes, no?: ")

if response == "no":
    sys.exit()

print(f'Downloading products to {save_path}...')
d1, d2, d3 = api.download_all(products, directory_path=save_path)

print(f'Products succesfully downloaded\n')
for k in d1:
    print(d1[k])
print(f'Products not downloaded\n')
for k in d2:
    print(d2[k])
print(f'Products failed to download\n')
for k in d3:
    print(d3[k])

