import json
import random
import requests

with open('user-agents.txt', 'r') as user_agents_file:
    user_agents = [line.strip() for line in user_agents_file]

random_user_agent = random.choice(user_agents)
headers = {
    'User-Agent': random_user_agent
}

TAMANHO_PAGINA = 100
URL = 'http://www.snirh.gov.br/hidroweb/rest/api/dadosHistoricos'

pagina_atual = 0

total_paginas = None

dados = []

response = requests.get(f'{URL}?size={TAMANHO_PAGINA}&page={pagina_atual}', headers=headers)

if response.status_code == 200:
    retorno = json.loads(response.content.decode('utf-8'))
    total_paginas = retorno['totalPages']
else:
    raise Exception('Erro ao obter total de páginas dos dados de estações convencionais')

with open('ids_estacoes_convencionais.txt', 'a') as ids_file:
    while pagina_atual <= total_paginas:
        print(f'Obtendo página {pagina_atual} de {total_paginas}...')
        response = requests.get(f'{URL}?size={TAMANHO_PAGINA}&page={pagina_atual}', headers=headers)
        if response.status_code == 200:
            retorno = json.loads(response.content.decode('utf-8'))
            dados += retorno['content']
            for estacao in retorno['content']:
                ids_file.write(str(estacao['id']) + '\n')
            pagina_atual = pagina_atual + 1
        else:
            raise Exception(f'Erro ao obter a página {pagina_atual} dos dados de estações convencionais')

with open('estacoes_convencionais.json', 'w') as json_file:
    json.dump(dados, json_file)
