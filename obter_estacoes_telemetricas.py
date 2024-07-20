import json
import requests

TAMANHO_PAGINA = 100
URL = 'http://www.snirh.gov.br/hidroweb/rest/api/estacaotelemetrica'

pagina_atual = 0

total_paginas = None

dados = []

response = requests.get(f'{URL}?size={TAMANHO_PAGINA}&page={pagina_atual}')

if response.status_code == 200:
    retorno = json.loads(response.content.decode('utf-8'))
    total_paginas = retorno['totalPages']
else:
    raise Exception('Erro ao obter total de páginas dos dados de estações telemétricas')

with open('ids_estacoes_telemetricas.txt', 'a') as ids_file:
    while pagina_atual <= total_paginas:
        print(f'Obtendo página {pagina_atual} de {total_paginas}...')
        response = requests.get(f'{URL}?size={TAMANHO_PAGINA}&page={pagina_atual}')
        if response.status_code == 200:
            retorno = json.loads(response.content.decode('utf-8'))
            dados += retorno['content']
            for estacao in retorno['content']:
                ids_file.write(str(estacao['id']) + '\n')
            pagina_atual = pagina_atual + 1
        else:
            raise Exception(f'Erro ao obter a página {pagina_atual} dos dados de estações telemétricas')

with open('estacoes_telemetricas.json', 'w') as json_file:
     json.dump(dados, json_file)
