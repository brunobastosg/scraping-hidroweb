from tempfile import TemporaryFile
import pandas as pd
import pyodbc
import requests
import tempfile
import zipfile

URL = 'http://www.snirh.gov.br/hidroweb/rest/api/documento/download?documentos=76'
OUTPUT_FOLDER = 'dominio'
DOMINIOS = ['bacia', 'entidade', 'estacao', 'estado', 'municipio', 'rio', 'subbacia']
COLUNAS_IGNORADAS = ['RegistroID', 'Importado', 'Temporario', 'Removido', 'ImportadoRepetido', 'DataIns', 'DataAlt', 'RespAlt']

def obter_driver():
    driver = [x for x in pyodbc.drivers() if x.startswith('Microsoft Access Driver')]
    if driver:
        return driver[0]
    else:
        raise Exception('Driver MS Access não encontrado')

def efetuar_download():
    response = requests.get(URL)
    tmp = tempfile.TemporaryFile()
    tmp.write(response.content)
    return tmp

def obter_banco_access():
    with efetuar_download() as tmp:
        access_db = None
        with zipfile.ZipFile(tmp, 'r') as zip1:
            arquivo1 = zip1.namelist()[0]
            zip1.extractall(OUTPUT_FOLDER)

            with zipfile.ZipFile('{}/{}'.format(OUTPUT_FOLDER, arquivo1), 'r') as zip2:
                access_db = zip2.namelist()[0]
                zip2.extractall(OUTPUT_FOLDER)
    
    return access_db

def transformar_access_em_csv(banco_access):
    driver = obter_driver()
    conn = pyodbc.connect('DRIVER={};DBQ={}/{}'.format(driver, OUTPUT_FOLDER, banco_access))
    cur = conn.cursor()

    for dominio in DOMINIOS:
        sql = pd.read_sql_query('SELECT * FROM {}'.format(dominio), conn)
        df = pd.DataFrame(sql).drop(COLUNAS_IGNORADAS, axis=1)
        df.to_csv('{}.csv'.format(dominio), sep=';', index=False, encoding='utf-8-sig')

    cur.close()
    conn.close()

def main():
    banco_access = obter_banco_access()
    transformar_access_em_csv(banco_access)

if __name__ == "__main__":
    main()
