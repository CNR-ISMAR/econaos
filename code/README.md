# econaos
marine ecological data management following Open Science principles.

#preprocEconaos.py
The preprocEconaos.py module is written with the purpose to harmonise at structural level the sampling station's names for the LTER marine ecological data belonging to CNR-ISMAR (Venezia). It is written for GRASS GIS 7.2 and it requires some input data:
* a CSV file of the station coordinates with correct name and period of use (of that specific name for the station) - a sample is provided
* the matrix file (specific for our dataset) - a sample is provided
* since normally the data coming from sensors is in Lat Long it is required to provide the Lat Long GRASS mapset where the data will be imported. The data is then reprojected because we have to do some distance-based considerations and the metric system (UTM WGS84 Z33 N) is more suitable than Lat Long for this purpose.
it returns:
* the matrix with stations' names properly cleaned
* the shapefile of the whole matrix (with database cleaned)
* the shapefile of records spatially matching the stations
* the shapefile of records which have, as station name, an integer number
