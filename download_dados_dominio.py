import pandas as pd
import pyodbc
import requests
import tempfile
import zipfile

URL = 'https://www.snirh.gov.br/hidroweb/rest/api/documento?page=0&size=5'
OUTPUT_FOLDER = 'dominio'
DOMINIOS = ['bacia', 'entidade', 'estacao', 'estado', 'municipio', 'rio', 'subbacia']
COLUNAS_IGNORADAS_TODOS = ['RegistroID', 'Importado', 'Temporario', 'Removido', 'ImportadoRepetido', 'DataIns', 'DataAlt', 'RespAlt']
COLUNAS_IGNORADAS_POR_DOMINIO = {
    # estou ignorando essas colunas pois possuem conteúdo não estruturado, com quebras de linha, e bagunçavam o csv no final
    'estacao': ['Descricao', 'Historico']
}

def obter_url_download():
    response = requests.get(URL)
    conteudo = response.json()
    id = None
    for item in conteudo['content']:
        if item['nome'] == 'Inventario.zip':
            id = item['id']
            break
    if id is None:
        raise Exception('URL para download do Inventario.zip não encontrada')
    return f'https://www.snirh.gov.br/hidroweb/rest/api/documento/download?documentos={id}'

def obter_driver():
    driver = [x for x in pyodbc.drivers() if x.startswith('Microsoft Access Driver')]
    if driver:
        return driver[0]
    else:
        raise Exception('Driver MS Access não encontrado')

def efetuar_download():
    url_download = obter_url_download()
    response = requests.get(url_download)
    tmp = tempfile.TemporaryFile()
    tmp.write(response.content)
    return tmp

def obter_banco_access():
    with efetuar_download() as tmp:
        access_db = None
        with zipfile.ZipFile(tmp, 'r') as zip:
            access_db = zip.namelist()[0]
            zip.extractall(OUTPUT_FOLDER)
    return access_db

def transformar_access_em_csv(banco_access):
    driver = obter_driver()
    conn = pyodbc.connect('DRIVER={};DBQ={}/{}'.format(driver, OUTPUT_FOLDER, banco_access))
    cur = conn.cursor()

    for dominio in DOMINIOS:
        colunas_ignoradas_dominio = COLUNAS_IGNORADAS_POR_DOMINIO.get(dominio, [])
        sql = pd.read_sql_query('SELECT * FROM {}'.format(dominio), conn)
        df = pd.DataFrame(sql).drop(COLUNAS_IGNORADAS_TODOS + colunas_ignoradas_dominio, axis=1)
        df.to_csv('dominio/{}.csv'.format(dominio), sep=';', index=False, encoding='utf-8-sig')

    cur.close()
    conn.close()

def main():
    banco_access = obter_banco_access()
    transformar_access_em_csv(banco_access)

if __name__ == "__main__":
    main()
