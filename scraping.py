from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
import selenium
import os
import time

URL_TO_SCRAPE = 'http://www.snirh.gov.br/hidroweb/publico/medicoes_historicas_abas.jsf'

SHORT_TIMEOUT  = 5
LONG_TIMEOUT = 30
LOADING_ELEMENT_XPATH = '//div[@class="loading"]'

FILE_NAME = 'downloaded.txt'

ITENS_POR_PAGINA = 20

CHROMEDRIVER_PATH = os.environ.get('CHROMEDRIVER')

driver = webdriver.Chrome(CHROMEDRIVER_PATH)

def abrir_site():
    driver.get(URL_TO_SCRAPE)

def clicar_botao_consultar():
    obter_botao_consultar().click()

def obter_botao_consultar():
    return driver.find_element_by_id('form:fsListaEstacoes:bt')

def selecionar_quantidade_itens_por_pagina():
    select = Select(driver.find_element_by_id('form:fsListaEstacoes:fsListaEstacoesC:j_idt180:pageSizeSelect'))
    select.select_by_visible_text(str(ITENS_POR_PAGINA))
    driver.find_element_by_id('form:fsListaEstacoes:fsListaEstacoesC:j_idt180:pageSizeDefine').click()
    aguardar_loading()

def selecionar_estacoes():
    for i in range(0, ITENS_POR_PAGINA):
        selecionar_estacao(i)
        aguardar_loading()
        baixar_arquivo()

def selecionar_estacao(indice):
    driver.find_elements_by_css_selector('input[type="checkbox"]')[indice].send_keys(webdriver.common.keys.Keys.SPACE)

def exibir_pagina(numero_pagina):
    obter_link_pagina(numero_pagina).click()

def obter_link_pagina(numero_pagina):
    return driver.find_element_by_link_text(str(numero_pagina))

def baixar_arquivo():
    baixou = False
    while not baixou:
        try:
            driver.find_element_by_id('form:fsListaEstacoes:fsListaEstacoesC:btBaixar').click()
            baixou = True
        except selenium.common.exceptions.ElementClickInterceptedException:
            time.sleep(5)
            pass


def selecionar_tipo_arquivo_csv():
    driver.find_elements_by_css_selector('input[type="radio"]')[2].send_keys(webdriver.common.keys.Keys.SPACE)

def aguardar_loading():
    try:
        WebDriverWait(driver, SHORT_TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, LOADING_ELEMENT_XPATH)))
    except selenium.common.exceptions.TimeoutException:
        pass

    try:
        WebDriverWait(driver, LONG_TIMEOUT).until_not(EC.visibility_of_element_located((By.XPATH, LOADING_ELEMENT_XPATH)))
    except selenium.common.exceptions.TimeoutException:
        pass

def clicar_aba_dados_convencionais():
    driver.find_element_by_css_selector('a[href="#dadosConvencionais"]').click()

def processar_pagina(numero_pagina):
    selecionar_estacoes()
    gravar_ultima_pagina_processada(numero_pagina)
    exibir_pagina(numero_pagina + 1)

def verificar_ultima_pagina_processada():
    try:
        with open(FILE_NAME, 'r') as reader:
            line = int(reader.readline())
    except FileNotFoundError:
        line = 1
    return line

def gravar_ultima_pagina_processada(numero_pagina):
    with open(FILE_NAME, 'w') as writer:
        writer.write(str(numero_pagina))

def obter_indice_ultima_pagina():
    obter_botao_ultima_pagina().click()
    aguardar_loading()
    indice_ultima_pagina = int(driver.find_element_by_css_selector('ul.pagination li.active a').text)
    obter_botao_primeira_pagina().click()
    aguardar_loading()
    return indice_ultima_pagina

def obter_botao_primeira_pagina():
    return driver.find_element_by_css_selector('ul.pagination li:first-child a')

def obter_botao_ultima_pagina():
    return driver.find_element_by_css_selector('ul.pagination li:last-child a')

def ir_para_pagina(numero_pagina):
    achou = False
    while (not achou):
        try:
            link_pagina = obter_link_pagina(numero_pagina)
            achou = True
            link_pagina.click()
        except selenium.common.exceptions.NoSuchElementException:
            clicar_ultima_pagina_visivel()
            aguardar_loading()

def clicar_ultima_pagina_visivel():
    obter_ultima_pagina_visivel().click()

def obter_ultima_pagina_visivel():
    return driver.find_element_by_css_selector('ul.pagination li:nth-last-child(2) a')

def scrape():
    abrir_site()

    clicar_botao_consultar()

    aguardar_loading()

    clicar_aba_dados_convencionais()

    selecionar_quantidade_itens_por_pagina()

    selecionar_tipo_arquivo_csv()

    aguardar_loading()

    ultima_pagina_processada = verificar_ultima_pagina_processada()

    indice_ultima_pagina = obter_indice_ultima_pagina()

    if (ultima_pagina_processada > 1):
        ir_para_pagina(ultima_pagina_processada)

    for i in range(ultima_pagina_processada, indice_ultima_pagina + 1):
        processar_pagina(i)

scrape()