import errno
import os
import requests

URL = 'http://www.snirh.gov.br/hidroweb/rest/api/documento/convencionais'
TIPO = 3
NUMERO_LINHAS = 50

pasta_atual = os.path.dirname(__file__)
pasta_destino = os.path.join(pasta_atual, 'downloads')

ids_documentos = None

if not os.path.exists(os.path.dirname(pasta_destino)):
    try:
        os.makedir(os.path.dirname(pasta_destino))
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise

with open('ids_estacoes_convencionais.txt', 'r') as ids_file:
    ids_documentos = ids_file.readlines()

inicio_bloco = 0
fim_bloco = inicio_bloco + NUMERO_LINHAS
tamanho = len(ids_documentos)
index = 0

while fim_bloco < tamanho:
    print('Processando bloco {} a {} de {}...'.format(inicio_bloco, fim_bloco, tamanho))
    bloco_ids = ids_documentos[inicio_bloco:fim_bloco]
    documentos = ','.join(bloco_ids).replace('\n', '')
    response = requests.get(URL + '?tipo={}&documentos={}'.format(TIPO, documentos))
    if response.status_code == 200:
        open(os.path.join(pasta_destino, 'medicoes_convencionais{}.zip'.format(index)), 'wb').write(response.content)
    else:
        print('Erro {} ao baixar lista de documentos: {}'.format(response.status_code, documentos))
    index = index + 1
    inicio_bloco = fim_bloco
    fim_bloco = tamanho - 1 if fim_bloco + NUMERO_LINHAS >= tamanho else fim_bloco + NUMERO_LINHAS

