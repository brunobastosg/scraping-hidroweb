from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium
import os
import time

URL_TO_SCRAPE = 'http://www.snirh.gov.br/hidroweb/publico/medicoes_historicas_abas.jsf'

SHORT_TIMEOUT  = 5
LONG_TIMEOUT = 30
LOADING_ELEMENT_XPATH = '//div[@class="loading"]'

ITENS_POR_PAGINA = 5
ULTIMA_PAGINA = 7238

CHROMEDRIVER_PATH = os.environ.get('CHROMEDRIVER')

driver = webdriver.Chrome(CHROMEDRIVER_PATH)

def abrir_site():
    driver.get(URL_TO_SCRAPE)

def clicar_botao_consultar():
    obter_botao_consultar().click()

def obter_botao_consultar():
    return driver.find_element_by_id('form:fsListaEstacoes:bt')

def selecionar_estacoes():
    for i in range(0, ITENS_POR_PAGINA):
        selecionar_estacao(i)
        aguardar_loading()
        baixar_arquivo()

def selecionar_estacao(indice):
    driver.find_elements_by_css_selector('input[type="checkbox"]')[indice].send_keys(webdriver.common.keys.Keys.SPACE)

def exibir_pagina(numeroPagina):
    driver.find_element_by_link_text(str(numeroPagina)).click()

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

def processar_pagina(indice_proxima_pagina):
    selecionar_estacoes()
    exibir_pagina(indice_proxima_pagina)
    return indice_proxima_pagina + 1

def scrape():
    abrir_site()

    clicar_botao_consultar()

    aguardar_loading()

    clicar_aba_dados_convencionais()

    selecionar_tipo_arquivo_csv()

    aguardar_loading()

    i = processar_pagina(2)

    while i < ULTIMA_PAGINA:
        i = processar_pagina(i)

scrape()