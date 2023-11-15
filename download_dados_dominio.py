from functools import partial
from pathlib import Path

import pandas as pd
import zeep

WSDL = 'https://telemetriaws1.ana.gov.br/ServiceANA.asmx?wsdl'

OUTPUT_FOLDER = Path('dominio')
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

client = zeep.Client(wsdl=WSDL)

DOMINIOS = {
  'baciaSubBacia': partial(client.service.HidroBaciaSubBacia, codBacia='', codSubBacia=''),
  'rio': partial(client.service.HidroRio, codRio=''),
  'estado': partial(client.service.HidroEstado, codUf=''),
  'municipio': partial(client.service.HidroMunicipio, codMunicipio=''),
  'entidade': partial(client.service.HidroEntidades, codEntidade=''),
  'estacao': partial(client.service.ListaEstacoesTelemetricas, statusEstacoes='', origem='')
}

def separar_bacias_de_subbacias(bacias_subbacias):
  cod_bacias = set()
  bacias = []
  subbacias = []
  for bacia_subbacia in bacias_subbacias:
    if bacia_subbacia['codBacia'] not in cod_bacias:
      bacias.append({
        'codBacia': bacia_subbacia['codBacia'],
        'nmBacia': bacia_subbacia['nmBacia']
      })
      cod_bacias.add(bacia_subbacia['codBacia'])

    subbacias.append({
      'codBacia': bacia_subbacia['codBacia'],
      'codSubBacia': bacia_subbacia['codSubBacia'],
      'nmSubBacia': bacia_subbacia['nmSubBacia']
    })
  
  return {
    'bacia': bacias,
    'subbacia': subbacias
  }

POS_PROCESSAMENTO = {
  'baciaSubBacia': separar_bacias_de_subbacias
}

def transformar_para_csv(dados, nome_arquivo):
  df = pd.DataFrame(dados)
  df.to_csv(OUTPUT_FOLDER / f'{nome_arquivo}.csv', sep=';', index=False, encoding='utf-8-sig')

def main():
  for dominio in DOMINIOS:
    dados = []
    res = DOMINIOS[dominio]()
    for item in res._value_1._value_1:
      dado = {}
      for key in item['Table']:
        dado[key] = item['Table'][key]
      dados.append(dado)

    if dominio in POS_PROCESSAMENTO:
      dados_pos_processados = POS_PROCESSAMENTO[dominio](dados)
      for nome in dados_pos_processados:
        transformar_para_csv(dados_pos_processados[nome], nome)
    else:
      transformar_para_csv(dados, dominio)

if __name__ == '__main__':
    main()
