"""
Autor = Alberto Álvarez Vales
Fecha = 22/03/2019
email = alberto.alvarez@fundacionmatrix.es

Descripción:
Crea archivos TIF de pendiente a partir de los datos del DEM.

Argumentos:
@srcFolder = Carpeta origen con archivos TIF con información del DEM
@dstFolder = Carpeta destino donde se generan los archivos TIF con información de la pendiente en radianes


La documentación de la libería richdem se puede encontrar en la siguiente
dirección: https://richdem.readthedocs.io/en/latest/

Metodología
Horn, B.K.P., 1981. Hill shading and the reflectance map. Proceedings of the IEEE 69, 14–47. doi:10.1109/PROC.1981.11918 Horn (1981) 
calculates the slope of a focal cell by using a central difference estimation of a surface fitted to the focal cell and its neighbours. 
The slope chosen is the maximum of this surface and can be returned in several formats.

"""


import os
import richdem 


def pendiente(srcFolder="./", dstFolder="./"):
    for archivo in os.listdir(srcFolder):
        if archivo.endswith(".tif"):           
            if srcFolder.endswith("/"): 
                ruta=srcFolder+archivo
            else:
                ruta=srcFolder+"/"+archivo
            dem = richdem.LoadGDAL(ruta) 
            slope = richdem.TerrainAttribute(dem, attrib='slope_radians') 
            archivo="pendiente_"+archivo
            if not os.path.exists(dstFolder):
                os.mkdir(dstFolder)
            if srcFolder.endswith("/"): 
                dstRuta=dstFolder+archivo
            else:
                dstRuta=dstFolder+"/"+archivo
            richdem.SaveGDAL(dstRuta,slope) 
    
    
pendiente("mdts/","pendiente/")