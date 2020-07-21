"""
Autor = Juanma Cintas
Fecha = 07/03/2019
email = juanmanuel.cintas@fundacionmatrix.es

Descripción:
Tile using filters.splitter.  ERROR: It can create las files iteratively.

La documentación de la libería pdal se puede encontrar en la siguiente
dirección: https://pdal.io/index.html


"""

import json
import pdal


def tile_lidar(folder_with_las, spacing, output_folder, buffer_distance):
        creating_json = {
                "pipeline": [
                        {
                                "type": "readers.las",
                                "filename": f"{folder_with_las}/*",
                                "spatialreference": "EPSG:25830"
                        },
                        {
                                "type": "filters.splitter",
                                "length": f"{spacing}",
                                "buffer": f"{buffer_distance}"
                        },
                        {
                                "type": "writer.las",
                                "srs": "EPSG:25830",
                                "filename": f"{output_folder}"
                        }
                ]
        
        }
        
        consulta = json.dumps(creating_json, indent = 4)
        print(consulta)

        pipeline = pdal.Pipeline(consulta)
        pipeline.validate()  # Check if json options are good
        pipeline.loglevel = 8
        count = pipeline.execute()
        print(count)
        
if __name__=="__main__":
        folder_with_las  = "data"
        spacing = 10000
        buffer_distance = 2500
        output_folder = "tiles"
        tile_lidar(folder_with_las = folder_with_las, spacing = spacing, output_folder = output_folder, buffer_distance = buffer_distance)
