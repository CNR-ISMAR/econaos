---
layout: post
title:  "News from the database"
categories: products
lang: en
ref: dpp
---


Our database (marine, long term and ecological) is enriched by zooplankton data!
In fact, until now database was composed by abiotic and phytoplankton data only - with this update regarding the zooplankton, finally the database is complete.

With more than 100000 observations and 21 different parameters, the database has been initially corrected by replacing points falling on land (transcription errors), then the sampling station names have been harmonized creating a [GRASS GIS] [grass] + [Python] [py] routine which has been published on [CNR-ISMAR Github channel] [github] as Open Source code. This routine merges the high text mining capacity of some Python libraries and the performant spatial analysis capabilities of GRASS GIS in a unique solution. In the same folder of the code it is possible to find:

1. _a README that guides the user through a description of the code, requirements, installation and usage;
2. _the pseudocode in a flowchart;
3. _a 3D and 2D view of the whole database;
4. _a brief extract of the database for code testing purposes.


Contextually, the vector layer of historical sampling stations and a 3D layer the whole database observations have been created.


Then, for each parameter has ben reconstructed the variation of sampling and analysis methods in time. This operation required a special effort both from bibliographic point of view both from direct experience from the researchers cho collected data (depending on the age of data). This effert was although needed if we wanted to obtain a sufficiently rich metadatation and an exhaustive view of the historical evolution of the database.

At the present time, we are writing a datapaper which will be published on [Earth System Science Data] [ESSD] and it will resume all the metadata related tot he database at the best of our knowledge. Earth System Science Data journal is, in our opininon a well accreditated journal (this ensures an adequate visibility of the work), moreover it requires that data should be released under liberal license, that should be identified by a DOI and this identifier must be persistent in time. Moreover it has a special function for dynamic data called ["Living data process"] [LD]: this ensures datapaper to evolve with data. More details are soon to come!


![graticola]({{ site.baseurl }}/imgs/graticola.png)
![db]({{ site.baseurl }}/imgs/db.png)



[grass]: https://grass.osgeo.org/
[py]: https://www.python.org/
[github]: https://github.com/CNR-ISMAR/econaos/tree/master
[ESSD]: https://www.earth-system-science-data.net
[LD]: https://www.earth-system-science-data.net/living_data_process.html
