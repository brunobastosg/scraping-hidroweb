import json
import requests

TAMANHO_PAGINA = 100
URL = 'http://www.snirh.gov.br/hidroweb/rest/api/estacaotelemetrica'

pagina_atual = 0

total_paginas = None

dados = []

response = requests.get(URL + '?size={}&page={}'.format(TAMANHO_PAGINA, pagina_atual))

if response.status_code == 200:
    retorno = json.loads(response.content.decode('utf-8'))
    total_paginas = retorno['totalPages']
else:
    raise Exception('Erro ao obter total de páginas dos dados de estações telemétricas')

with open('ids_estacoes_telemetricas.txt', 'a') as ids_file:
    while pagina_atual <= total_paginas:
        print('Obtendo página {} de {}...'.format(pagina_atual, total_paginas))
        response = requests.get(URL + '?size={}&page={}'.format(TAMANHO_PAGINA, pagina_atual))
        if response.status_code == 200:
            retorno = json.loads(response.content.decode('utf-8'))
            dados += retorno['content']
            for estacao in retorno['content']:
                ids_file.write(str(estacao['id']) + '\n')
            pagina_atual = pagina_atual + 1
        else:
            raise Exception('Erro ao obter a página {} dos dados de estações telemétricas'.format(pagina_atual))

with open('estacoes_telemetricas.json', 'w') as json_file:
     json.dump(dados, json_file)
