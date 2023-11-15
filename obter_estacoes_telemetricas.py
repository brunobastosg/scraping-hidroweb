import simplejson as json
import zeep

WSDL = 'https://telemetriaws1.ana.gov.br/ServiceANA.asmx?wsdl'

client = zeep.Client(wsdl=WSDL)
result = client.service.ListaEstacoesTelemetricas(statusEstacoes='', origem='')

estacoes = []

for item in result._value_1._value_1:
  estacao = {}
  for key in item['Table']:
     estacao[key] = item['Table'][key]
  estacoes.append(estacao)

with open('ids_estacoes_telemetricas.txt', 'a') as ids_file:
  for estacao in estacoes:
    ids_file.write(str(estacao['CodEstacao']) + '\n')
