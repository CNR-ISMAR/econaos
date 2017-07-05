#!/usr/bin/env python
#
##############################################################################
#
#!/usr/bin/env python
#
##############################################################################
#
# MODULE:       preprocEconaos.py
#
# AUTHOR(S):    annalisa minelli
#
# PURPOSE:      Preprocessing of marine ecological data.
#
# DATE:         Thu Feb  9 15:14:32 2017
#
##############################################################################

#%module
#% description: Preprocessing of marine ecological data.
#%end
#%option
#% key: llmset
#% type: string
#% label: path to the latlong mapset where data are stored
#% description: for exampe '/home/annalisa/DATAGRASS/LL_WGS84/ismar72'
#% required: yes
#%end
#%option G_OPT_F_INPUT
#% key: matrix
#% type: string
#% label: path to the csv matrix containing data
#% description: for exampe '/home/annalisa/Documenti/Venezia/datiMauroFabrizio/dataset_adriatico/versioniMatrice/matrice3D.csv'
#% required: yes
#%end
#%option G_OPT_F_INPUT
#% key: stations
#% type: string
#% label: path to the csv with coordinates and names of the stations
#% description: for exampe '/home/annalisa/Documenti/Venezia/datiMauroFabrizio/dataset_adriatico/stationsAll.csv'
#% required: yes
#%end
#%option G_OPT_F_OUTPUT
#% key: matclean
#% type: string
#% label: path to the csv cleaned matrix
#% description: for exampe '/home/annalisa/Documenti/Venezia/datiMauroFabrizio/dataset_adriatico/matrixCleaned.csv'
#% required: yes
#%end
#%option G_OPT_V_OUTPUT
#% key: mattot
#% type: string
#% label: name of the shapefile of the total matrix in output
#% description: for exampe '/home/annalisa/Documenti/Venezia/datiMauroFabrizio/dataset_adriatico/matrixTot.shp'
#% required: yes
#%end
#%option G_OPT_V_OUTPUT
#% key: matmatching
#% type: string
#% label: name of the shapefile of points matching with stations in output
#% description: for exampe '/home/annalisa/Documenti/Venezia/datiMauroFabrizio/dataset_adriatico/matrixMatching.shp'
#% required: yes
#%end
#%option G_OPT_V_OUTPUT
#% key: matinteger
#% type: string
#% label: name of the shapefile of points with an integer as station name in output
#% description: for exampe '/home/annalisa/Documenti/Venezia/datiMauroFabrizio/dataset_adriatico/matrixInteger.shp'
#% required: yes
#%end

import sys,os,re
import grass.script as grass

from grass.script import parser
#from difflib import SequenceMatcher as sm
#from subprocess import call

def cleanup():
    pass

def main():
    #mapset latlong - tutto il path locale
    llmset=options['llmset']
    #matricione in csv
    matrix=options['matrix']
    #rete delle stazioni in csv
    stations=options['stations']
    #
    matclean=options['matclean']
    #
    mattot=options['mattot']
    #
    matmatching=options['matmatching']
    #
    matinteger=options['matinteger']
    
    #llMset= '/home/annalisa/DATAGRASS/LL_WGS84/ismar72'
    #matrix= '/home/annalisa/Documenti/Venezia/datiMauroFabrizio/dataset_adriatico/versioniMatrice/matrice3D.csv'
    #stations= '/home/annalisa/Documenti/Venezia/datiMauroFabrizio/dataset_adriatico/stationsAll.csv'
    
    grass.run_command('g.gisenv', set='"OVERWRITE=1"')
    
    #importiamo la matrice come punti 3D
    
    os.system("grass72 "+llMset+" --exec v.in.ascii --overwrite input="+stations+" output=stationsAll_2 skip=1")
    os.system("grass72 "+llMset+" --exec v.in.ascii -z --overwrite input="+matrix+" output=matrice_3D skip=2 z=3")
    
    grass.run_command('v.proj', location=llMset.split('/')[-2], mapset=llMset.split('/')[-1], input='matrice_3D')
    grass.run_command('v.proj', location=llMset.split('/')[-2], mapset=llMset.split('/')[-1], input='stationsAll_2')
    
    #aggiorno le coordinate nel sistema metrico UTM
    grass.run_command('v.to.db', map='matrice_3D', option='coor', columns='dbl_1,dbl_2,dbl_3')
    grass.run_command('v.to.db', map='stationsAll_2', option='coor', columns='dbl_1,dbl_2')
    
    #faccio una copia del file vettoriale dei dati importato in UTM
    grass.run_command('g.copy', vector='matrice_3D,matrice_3D_copyOld')
    
    #grass.run_command('g.copy', vector='matrice_3D_copyOld,matrice_3D')
    
    #spostamento geografico dei punti su terra
    grass.run_command('g.region', raster='italy_cleaned2', res='100')
    
    #facciamo un buffer negativo di 10km per evitare i campionamenti in zone costiere (o estuarine)
    #verifico prima che io non abbia gia il buf neg da precedenti elaborazioni (operazione time consuming!)
    r=str(grass.list_strings(type='raster'))
    if re.search('italy_cleaned3',r):
	    pass;
    else:
	    grass.run_command('r.grow', input='italy_cleaned2', output='italy_cleaned3', radius='-100', new='1')
    
    a=grass.read_command('v.what.rast', flags='p', map='matrice_3D', raster='italy_cleaned3').split('\n')[:-1]
    cats=[]
    for i in a:
        if i.split('|')[1]=='1':
            cats.append(int(i.split('|')[0]))
    
    #se ci sono punti su terra, segue una procedura di spostamento dei punti
    if len(cats) != 0:
        from_coords=(grass.read_command('v.to.db', flags='p', map='matrice_3D', option='coor', units='meters')[:-1]).split('\n')[1:]
        for i in cats:
            print 'moving category nr. '+str(i)
            station=grass.read_command('v.db.select', flags='c', map='matrice_3D', columns='str_3', where='cat='+str(i))[:-1]
        
            #coordinate di partenza
            for g in from_coords:
                if g.startswith(str(i)+'|'):
                    east_from,north_from,z_from=g.split('|')[1],g.split('|')[2],g.split('|')[3]
        
            #coordinate di arrivo
            grass.run_command('v.db.addcolumn', map='stationsAll_2', columns="east double precision, north double precision")
            grass.run_command('v.to.db', map='stationsAll_2', type='point', option='coor', columns='east,north', units='meters')
            east_to,north_to,z_to=grass.read_command('v.db.select', flags='c', map='stationsAll_2', columns='east,north', where='str_1 LIKE "%'+str(station)+'%"')[:-1].split('|')[0],grass.read_command('v.db.select', flags='c', map='stationsAll_2', columns='east,north', where='str_1 LIKE "%'+str(station)+'%"')[:-1].split('|')[1],z_from
        
            #sposto i punti piazzati male
            grass.run_command('v.edit', tool='move', map='matrice_3D', cat=i, move=str(float(east_to)-float(east_from))+','+str(float(north_to)-float(north_from))+',0')
            grass.run_command('v.to.db', map='matrice_3D', option='coor', columns='dbl_1,dbl_2,dbl_3')

    
    
    #creazione dei voronoi e matching della stazione indicata coi voronoi
    
    #mi metto intorno alle stazioni e allargo la bbox di 30km per prendere piu punti possibile
    grass.run_command('g.region', vector='stationsAll_2', n='n+30000', s='s-30000', e='e+30000', w='w-30000')
    grass.run_command('v.voronoi', input='stationsAll_2', output='stationsAllVoronoi_2')
    grass.run_command('v.db.addcolumn',map='matrice_3D',column='voronoiStat char(30)')
    grass.run_command('v.what.vect',map='matrice_3D',column='voronoiStat',query_map='stationsAllVoronoi_2',query_column='str_1')
    a=grass.read_command('db.select',table='matrice_3D').split('\n')[1:-1]
    
    #individuo i punti con le stazioni scritte bene a meno di un carattere separatore
    cats_matching=[]
    cats_integer=[]
    matching=open('matching.csv','w')
    integer=open('integer.csv','w')

    for i in a:
        if len(i.split('|')[6])>6 :
    		    #correggi la tabella del vettoriale in caso di stazione+data
    		    i=i.replace('_'+i.split('|')[8],'',1)
        try:
            #provo a trasformare i nomi delle stazioni in interi, se questo non avviene, avvio il matching
            #per evitare che ad es. 183 finisca nella stazione 1/3
            int(i.split('|')[6])
        except ValueError:
            #non considero i punti che non ricadono in nessun voronoi
            if len(i.split('|')[-1])==0:
			    continue;
			#caso in cui la stazione abbia due nomi (cambio nome nel tempo)
    	    if len(i.split('|')[-1])>5:
    		    for g in i.split('|')[-1].split(','):
    			    if (len(i.split('|')[6])<6 and i.split('|')[6].startswith(g.split('/')[0]) and i.split('|')[6].endswith(g.split('/')[-1])):
    			        #correggi la tabella del vettoriale in caso di stazione scritta male
    			        i=i.replace(i.split('|')[6],g,1)
    			        matching.writelines(i)
    			        matching.writelines('\n')
    			        cats_matching.append(int(i.split('|')[0]))
            else:
                #caso in cui la stazione ha un solo nome
                if (len(i.split('|')[6])<6 and i.split('|')[6].startswith(i.split('|')[-1].split('/')[0]) and i.split('|')[6].endswith(i.split('|')[-1].split('/')[-1])):
                    #correggi la tabella del vettoriale in caso di stazione scritta male
                    i=i.replace(i.split('|')[6],i.split('|')[-1],1)
                    matching.writelines(i)
                    matching.writelines('\n')
                    cats_matching.append(int(i.split('|')[0]))
        else:
            #caso in cui al posto del nome della stazione ci sia un numero intero
    		cats_integer.append(int(i.split('|')[0]))
    		integer.writelines(i)
    		integer.writelines('\n')
           
    matching.close()
    integer.close()

    #faccio una copia di sicurezza prima di modificare i dati di partenza
    grass.run_command('g.copy', vector='matrice_3D,matrice_3D_copy')

    #carico i nuovi vettoriali di matching e integer con matrice corretta
    grass.run_command('v.in.ascii', flags='z', input='matching.csv', output='matrice_3D_matching', x='2', y='3', z='4', cat='1')
    grass.run_command('v.in.ascii', flags='z', input='integer.csv', output='matrice_3D_integer', x='2', y='3', z='4', cat='1')
    #salvo i risultati, una tabella dei dati totali e tre shapes dei vettoriali totale, matching e integer
    grass.run_command('v.out.ogr', input='matrice_3D', output=matclean format='CSV')
    grass.run_command('v.out.ogr', flags='e', input='matrice_3D', output=mattot)
    grass.run_command('v.out.ogr', flags='e', input='matrice_3D_integer', output=matinteger)
    grass.run_command('v.out.ogr', flags='e', input='matrice_3D_matching', output=matmatching)
#   grass.run_command('v.edit', map='matrice_3D', type='point', tool='delete', cats=str(cats_integer)[1:-1]+','+str(cats_matching)[1:-1])

    print "The End";

if __name__ == "__main__":
    options, flags = parser()
#   atexit.register(cleanup)
    sys.exit(main())
