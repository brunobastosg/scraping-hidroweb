import os
import pandas as pd
import pyodbc
import sqlalchemy as sa
import time
import winreg
import zipfile

from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = 'https://www.snirh.gov.br/hidroweb/download'
NOME_ARQUIVO_INVENTARIO = 'Inventario.zip'
OUTPUT_FOLDER = 'dominio'
DOMINIOS = ['bacia', 'entidade', 'estacao', 'estado', 'municipio', 'rio', 'subbacia']
COLUNAS_IGNORADAS_TODOS = ['RegistroID', 'Importado', 'Temporario', 'Removido', 'ImportadoRepetido', 'DataIns', 'DataAlt', 'RespAlt']
COLUNAS_IGNORADAS_POR_DOMINIO = {
    # estou ignorando essas colunas pois possuem conteúdo não estruturado, com quebras de linha, e bagunçavam o csv no final
    'estacao': ['Descricao', 'Historico']
}

def aguardar_download(diretorio, timeout, numero_arquivos=None):
    segundos = 0
    aguardar = True
    while aguardar and segundos < timeout:
        time.sleep(1)
        aguardar = False
        arquivos = os.listdir(diretorio)
        if numero_arquivos and len(arquivos) != numero_arquivos:
            aguardar = True

        for nome_arquivo in arquivos:
            if nome_arquivo.endswith('.crdownload'):
                aguardar = True

        segundos += 1
        print(f'\tAguardando download do inventário... ({segundos}s)')
    print(f'Download concluído em {segundos} segundos')
    return segundos

def obter_driver():
    driver = [x for x in pyodbc.drivers() if x.startswith('Microsoft Access Driver')]
    if driver:
        return driver[0]
    else:
        raise Exception('Driver MS Access não encontrado')

def efetuar_download():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    browser = webdriver.Chrome(options=options)
    browser.get(URL)
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.cdk-column-acaoDownload')))
    botao_download_inventario = browser.find_element(by=By.XPATH, value=f'//tr[td[contains(text(),"{NOME_ARQUIVO_INVENTARIO}")]]/td[contains(@class, "cdk-column-acaoDownload")]/button')
    botao_download_inventario.click()
    pasta_download = obter_pasta_download()
    qtd_arquivos_pasta_download = obter_quantidade_arquivos(pasta_download)
    aguardar_download(pasta_download, 60, qtd_arquivos_pasta_download + 1)
    browser.close()
    return open(str(Path(pasta_download) / NOME_ARQUIVO_INVENTARIO), 'b+r')

def obter_pasta_download():
    sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
    downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
        location = winreg.QueryValueEx(key, downloads_guid)[0]
    return location

def obter_quantidade_arquivos(pasta):
    return sum(1 for _ in Path(pasta).glob('*'))

def obter_banco_access():
    with efetuar_download() as tmp:
        access_db = None
        with zipfile.ZipFile(tmp, 'r') as zip_file:
            access_db = zip_file.namelist()[0]
            zip_file.extractall(OUTPUT_FOLDER)
    return access_db

def transformar_access_em_csv(banco_access):
    driver = obter_driver()
    connection_url = sa.engine.URL.create(
        'access+pyodbc',
        query={'odbc_connect': f'DRIVER={driver};DBQ={OUTPUT_FOLDER}/{banco_access}'}
    )
    engine = sa.create_engine(connection_url)

    for dominio in DOMINIOS:
        colunas_ignoradas_dominio = COLUNAS_IGNORADAS_POR_DOMINIO.get(dominio, [])
        sql = pd.read_sql_query(f'SELECT * FROM {dominio}', engine)
        df = pd.DataFrame(sql).drop(COLUNAS_IGNORADAS_TODOS + colunas_ignoradas_dominio, axis=1)
        df.to_csv(f'dominio/{dominio}.csv', sep=';', index=False, encoding='utf-8-sig')

def main():
    banco_access = obter_banco_access()
    transformar_access_em_csv(banco_access)

if __name__ == '__main__':
    main()
