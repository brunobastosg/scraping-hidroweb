from argparse import ArgumentParser
import os
import glob
import pandas as pd

parser = ArgumentParser()
parser.add_argument('-i', '--input', help='Diretório onde se encontram os arquivos CSV', required=True)

args = parser.parse_args()

input_dir = args.input

os.chdir(input_dir)

extension = 'csv'

print('INICIANDO...')

print('CHUVA')
print('\tLendo...')
chuvas = [i for i in glob.glob('chuvas*.{}'.format(extension))]
print('\tConcatenando...')
chuvas_csv = pd.concat([pd.read_csv(f, sep=';', skiprows=12, index_col=False, dayfirst=True, parse_dates=[2], decimal=',') for f in chuvas]).sort_values(by=['EstacaoCodigo', 'Data'])
print('\tGerando CSV...')
chuvas_csv.to_csv('chuvas.csv', index=False, encoding='utf-8-sig')

print('CLIMA')
print('\tLendo...')
clima = [i for i in glob.glob('clima*.{}'.format(extension))]
print('\tConcatenando...')
clima_csv = pd.concat([pd.read_csv(f, sep=';', skiprows=38, index_col=False, dayfirst=True, parse_dates=[2, 3], decimal=',') for f in clima]).sort_values(by=['EstacaoCodigo', 'Data', 'Hora'])
print('\tGerando CSV...')
clima_csv.to_csv('clima.csv', index=False, encoding='utf-8-sig')

print('COTAS')
print('\tLendo...')
cotas = [i for i in glob.glob('cotas*.{}'.format(extension))]
print('\tConcatenando...')
cotas_csv = pd.concat([pd.read_csv(f, sep=';', skiprows=13, index_col=False, dayfirst=True, parse_dates=[2, 3], decimal=',') for f in cotas]).sort_values(by=['EstacaoCodigo', 'Data', 'Hora'])
print('\tGerando CSV...')
cotas_csv.to_csv('cotas.csv', index=False, encoding='utf-8-sig')

print('CURVA DESCARGA')
print('\tLendo...')
curvadescarga = [i for i in glob.glob('curvadescarga*.{}'.format(extension))]
print('\tConcatenando...')
curvadescarga_csv = pd.concat([pd.read_csv(f, sep=';', skiprows=12, index_col=False, decimal=',', usecols=range(0, 17), engine='python') for f in curvadescarga]).sort_values(by=['EstacaoCodigo', 'NivelConsistencia', 'PeriodoValidadeInicio', 'PeriodoValidadeFim'])
print('\tGerando CSV...')
curvadescarga_csv.to_csv('curvadescarga.csv', index=False, encoding='utf-8-sig')

print('PERFIL TRANSVERSAL')
print('\tLendo...')
perfiltransversal = [i for i in glob.glob('PerfilTransversal*.{}'.format(extension))]
print('\tConcatenando...')
perfiltransversal_csv = pd.concat([pd.read_csv(f, sep=';', skiprows=11, index_col=False, dayfirst=True, parse_dates=[2, 3], decimal=',', usecols=range(0, 15), engine='python') for f in perfiltransversal]).sort_values(by=['EstacaoCodigo', 'Data', 'Hora'])
print('\tGerando CSV...')
perfiltransversal_csv.to_csv('perfiltransversal.csv', index=False, encoding='utf-8-sig')

print('QUALIDADE DA ÁGUA')
print('\tLendo...')
qualagua = [i for i in glob.glob('qualagua*.{}'.format(extension))]
print('\tConcatenando...')
qualagua_csv = pd.concat([pd.read_csv(f, sep=';', skiprows=14, index_col=False, dayfirst=True, parse_dates=[2, 3], decimal=',', usecols=range(0, 302)) for f in qualagua]).sort_values(by=['EstacaoCodigo', 'Data', 'Hora'])
print('\tGerando CSV...')
qualagua_csv.to_csv('qualagua.csv', index=False, encoding='utf-8-sig')

print('RESUMO DESCARGA')
print('\tLendo...')
resumodescarga = [i for i in glob.glob('ResumoDescarga*.{}'.format(extension))]
print('\tConcatenando...')
resumodescarga_csv = pd.concat([pd.read_csv(f, sep=';', skiprows=10, index_col=False, dayfirst=True, parse_dates=[2, 3], decimal=',', encoding='iso-8859-1') for f in resumodescarga]).sort_values(by=['EstacaoCodigo', 'Data', 'Hora'])
print('\tGerando CSV...')
resumodescarga_csv.to_csv('resumodescarga.csv', index=False, encoding='utf-8-sig')

print('SEDIMENTOS')
print('\tLendo...')
sedimentos = [i for i in glob.glob('sedimentos*.{}'.format(extension))]
print('\tConcatenando...')
sedimentos_csv = pd.concat([pd.read_csv(f, sep=';', skiprows=10, index_col=False, dayfirst=True, parse_dates=[2, 3, 5, 6], decimal=',') for f in sedimentos]).sort_values(by=['EstacaoCodigo', 'Data', 'Hora', 'NumMedicao', 'DataLiq', 'HoraLiq', 'NumMedicaoLiq'])
print('\tGerando CSV...')
sedimentos_csv.to_csv('sedimentos.csv', index=False, encoding='utf-8-sig')

print('VAZÕES')
print('\tLendo...')
vazoes = [i for i in glob.glob('vazoes*.{}'.format(extension))]
print('\tConcatenando...')
vazoes_csv = pd.concat([pd.read_csv(f, sep=';', skiprows=13, index_col=False, dayfirst=True, parse_dates=[2, 3], decimal=',') for f in vazoes]).sort_values(by=['EstacaoCodigo', 'Data', 'Hora'])
print('\tGerando CSV...')
vazoes_csv.to_csv('vazoes.csv', index=False, encoding='utf-8-sig')

print('CONCLUÍDO!')
