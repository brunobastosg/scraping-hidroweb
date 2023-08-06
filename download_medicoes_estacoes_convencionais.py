import random
import requests

from pathlib import Path

with open('user-agents.txt', 'r') as user_agents_file:
    user_agents = [line.strip() for line in user_agents_file]

random_user_agent = random.choice(user_agents)
headers = {
    'User-Agent': random_user_agent
}

URL = 'http://www.snirh.gov.br/hidroweb/rest/api/documento/convencionais'
TIPO = 3
NUMERO_LINHAS = 50

pasta_destino = Path('downloads')

ids_documentos = None

if not pasta_destino.is_dir():
    pasta_destino.mkdir()

with open('ids_estacoes_convencionais.txt', 'r') as ids_file:
    ids_documentos = [line.strip() for line in ids_file.readlines()]

inicio_bloco = 0
fim_bloco = inicio_bloco + NUMERO_LINHAS
tamanho = len(ids_documentos)
index = 0

while fim_bloco < tamanho - 1:
    print(f'Processando bloco {inicio_bloco} a {fim_bloco} de {tamanho}...')
    bloco_ids = ids_documentos[inicio_bloco:fim_bloco]
    documentos = ','.join(bloco_ids)
    response = requests.get(f'{URL}?tipo={TIPO}&documentos={documentos}', headers=headers)
    if response.status_code == 200:
        if (len(response.content) == 0):
            print('Response vazio. Ignorando...')
        else:
            open(Path(pasta_destino, f'medicoes_convencionais{index}.zip'), 'wb').write(response.content)
    else:
        print(f'Erro {response.status_code} ao baixar lista de documentos: {documentos}')
    index = index + 1
    inicio_bloco = fim_bloco
    fim_bloco = tamanho - 1 if fim_bloco + NUMERO_LINHAS >= tamanho else fim_bloco + NUMERO_LINHAS
