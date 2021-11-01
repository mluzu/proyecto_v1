## Configuracion del entorno de desarrollo
- conda create -n <envname> --python=3.9.6
- conda activate <envname>
- conda install --file requirements.txt

Hay que apuntas las variables de entorno PROJ_LIB a la carpeta proj que se encuentra dentro del entorno virtual (se crea tras instalar las librerias de gdal); la variable de entorno GDAL_DATA debe apuntar a las carpetas donde se encuentran los escripts de gdal. El path termina siempre con "envs\\geoconda\\Library\\share\\proj" y "envs\\geoconda\\Library\\share\\gdal" respectivamente, donde envs es el directorio donde se encuentras los entornos creados con conda. 


## Alternativas para descargar imagenes
- Copernicus Open Hub
https://sentinelsat.readthedocs.io/en/master/api_overview.html
https://docs.sentinel-hub.com/api/latest/

- Google Earth Engine
https://developers.google.com/earth-engine