import errno
import os

import requests
from bs4 import BeautifulSoup

RESULTS_DIR = 'results'
LIDAR_FILES_DIR = 'lidar_files'
LIDAR_IDS_DOC = 'lidar_ids_doc.txt'


def fetch_doc_list(state_cod, whole_spain='N', lidar_ids_file=LIDAR_IDS_DOC):
 

    url = 'http://centrodedescargas.cnig.es/CentroDescargas/resultadosArchivos'
    next_page = 1
    doc_list = []
    while next_page:
        print('Leyendo documentos de la página {}'.format(next_page))
        data = {
            'numPagina': next_page,
            'codSerie': 'LIDA2',
            'series': 'LIDA2',
            'codProvAv': state_cod,
            'todaEsp': whole_spain,
            'tipoBusqueda': 'AV',
        }
        response = requests.post(url, data=data)
        if response.status_code != 200:
            print('>>>>> Error. No se pudo recuperar el listado de documentos')
            print(response.text)
            return
        data = response.text
        soup = BeautifulSoup(data, 'lxml')
        f =  open('myfile.txt', 'w')
        for s in data:
        	f.write(s)
        print(soup)
        next_page = None
        """soup = BeautifulSoup(data, 'lxml')
        next_link = soup.find('a', {'title': 'Siguiente'})
        next_page = next_page + 1 if next_link else None
        file_list_div = soup.find('div', {'id': 'blqListaArchivos'})
        file_list_tb = file_list_div.find('table').find('tbody')
        trs = file_list_tb.find_all('tr')
        for tr in trs:
            ihidden = tr.find_all('input', {'type': 'hidden'})
            file_link_id = None
            for input in ihidden:
                if input['id'].startswith('secGeo_'):
                    file_link_id = input['value']
            file_name = tr.find('td', {'data-th': 'Nombre'}).text
            doc_list.append((file_name, file_link_id))
    print('Número de docs: {}'.format(len(doc_list)))

    lidar_doc_file_path = os.path.join(RESULTS_DIR, lidar_ids_file)
    with open(lidar_doc_file_path, 'w') as lidar_docs_file:
        for doc in doc_list:
            lidar_docs_file.write('{},{}\n'.format(doc[0], doc[1]))"""

if __name__ == '__main__':
    if not os.path.exists(RESULTS_DIR):
        try:
            os.makedirs(RESULTS_DIR)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    # El código de la provincia de Murcia es el 30
    fetch_doc_list('45')
