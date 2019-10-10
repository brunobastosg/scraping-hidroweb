from selenium import webdriver
import os
import time

URL_TO_SCRAPE = 'http://www.snirh.gov.br/hidroweb/publico/medicoes_historicas_abas.jsf'

chromedriver_path = os.environ.get('CHROMEDRIVER')
driver = webdriver.Chrome(chromedriver_path)

def clicar_botao_consultar():
    obter_botao_consultar().click()

def obter_botao_consultar():
    return driver.find_element_by_id('form:fsListaEstacoes:bt')

def selecionar_checkboxes():
    for j in range(0, 5):
        checkbox = driver.find_elements_by_css_selector('input[type="checkbox"]')[j]
        checkbox.send_keys(webdriver.common.keys.Keys.SPACE)
        time.sleep(2)
        driver.find_elements_by_css_selector('input[type="radio"]')[2].send_keys(webdriver.common.keys.Keys.SPACE)
        time.sleep(2)
        driver.find_element_by_id('form:fsListaEstacoes:fsListaEstacoesC:btBaixar').click()
        time.sleep(2)

def exibir_pagina(numeroPagina):
    driver.find_element_by_link_text(str(numeroPagina)).click()

def scrape():
    driver.get(URL_TO_SCRAPE)

    clicar_botao_consultar()

    time.sleep(5)

    driver.find_element_by_css_selector('a[href="#dadosConvencionais"]').click()

    ultima_pagina = 7238
    i = 2

    selecionar_checkboxes()
    exibir_pagina(i)
    i = i + 1

    while i < ultima_pagina:
        selecionar_checkboxes()
        exibir_pagina(i)
        i = i + 1

scrape()