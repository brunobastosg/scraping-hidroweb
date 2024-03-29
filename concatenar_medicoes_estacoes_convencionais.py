import glob
import pandas as pd

from argparse import ArgumentParser
from pathlib import Path

parser = ArgumentParser()
parser.add_argument('-i', '--input', help='Diretório onde se encontram os arquivos CSV', required=True)
args = parser.parse_args()
input_dir = args.input

extension = 'csv'

output_folder = 'medicoes-estacoes-convencionais-concatenadas'

arquivos_com_erro_nao_tratados = []

# alguns arquivos estão mal-formados, pois usam o caracter ; no meio do valor de uma célula, sem envolver o valor entre aspas, então o pandas acha que é um separador
map_correcoes_arquivos = {
    'ResumoDescarga_C_15564000.csv': 'eyck; fabio; robson',
    'ResumoDescarga_C_40784000.csv': 'Sidney; Grace; Michele',
    'ResumoDescarga_C_14845000.csv': 'Rodolfo Oliveira; Guilherme Costa'
}

def concatenar_arquivos_csv(nome, prefixo, skiprows, usecols=None, date_columns=None, sort_columns=None, output_filename=None, engine='c'):
    print(nome)
    print(f'\tLendo...')
    files = [i for i in glob.glob(f'{input_dir}/{prefixo}*.{extension}')]
    
    if len(files) > 0:
        print('\tConcatenando...')
        dfs = []
        for f in files:
            try:
                df = pd.read_csv(f, sep=';', skiprows=skiprows, index_col=False, dayfirst=True, parse_dates=date_columns, decimal=',', usecols=usecols, encoding='iso-8859-1', engine=engine)
                dfs.append(df)
            except Exception as e:
                print(f'\t\tErro ao ler CSV {f}: {e}')
                nome_arquivo_sem_pasta = f.split('/')[1]
                if map_correcoes_arquivos[nome_arquivo_sem_pasta]:
                    print('\t\tTentando tratar o problema...')
                    with open(f, 'r', encoding='iso-8859-1') as csv_problematico:
                        conteudo = csv_problematico.read()
                        conteudo = conteudo.replace(map_correcoes_arquivos[nome_arquivo_sem_pasta], map_correcoes_arquivos[nome_arquivo_sem_pasta].replace(';', ','))
                    with open(f, 'w', encoding='iso-8859-1') as csv_consertado:
                        csv_consertado.write(conteudo)
                    df = pd.read_csv(f, sep=';', skiprows=skiprows, index_col=False, dayfirst=True, parse_dates=date_columns, decimal=',', usecols=usecols, encoding='iso-8859-1', engine=engine)
                    dfs.append(df)
                else:
                    arquivos_com_erro_nao_tratados.append(f)

        concatenated_df = pd.concat(dfs)
        
        print('\tOrdenando...')
        concatenated_df = concatenated_df.sort_values(by=sort_columns)
        
        print('\tGerando CSV...')
        output_subfolder = Path(output_folder, prefixo.lower())
        output_subfolder.mkdir(parents=True, exist_ok=True)
        concatenated_df.to_csv(output_subfolder / f'{output_filename}.csv', index=False, encoding='utf-8-sig')
    else:
        print(f'\tNenhum CSV de {nome} encontrado.')

print('INICIANDO...')

concatenar_arquivos_csv(nome='CHUVA', prefixo='chuvas', skiprows=12, date_columns=[2], sort_columns=['EstacaoCodigo', 'Data'], output_filename='chuvas')
concatenar_arquivos_csv(nome='CLIMA', prefixo='clima', skiprows=38, date_columns=[2, 3], sort_columns=['EstacaoCodigo', 'Data', 'Hora'], output_filename='clima')
concatenar_arquivos_csv(nome='COTAS', prefixo='cotas', skiprows=13, date_columns=[2, 3], sort_columns=['EstacaoCodigo', 'Data', 'Hora'], output_filename='cotas')
concatenar_arquivos_csv(nome='CURVA DESCARGA', prefixo='curvadescarga', skiprows=12, usecols=range(0, 17), engine='python', sort_columns=['EstacaoCodigo', 'NivelConsistencia', 'PeriodoValidadeInicio', 'PeriodoValidadeFim'], output_filename='curvadescarga')
concatenar_arquivos_csv(nome='PERFIL TRANSVERSAL', prefixo='PerfilTransversal', skiprows=11, date_columns=[2, 3], usecols=range(0, 15), engine='python', sort_columns=['EstacaoCodigo', 'Data', 'Hora'], output_filename='perfiltransversal')
concatenar_arquivos_csv(nome='QUALIDADE DA ÁGUA', prefixo='qualagua', skiprows=14, date_columns=[2, 3], usecols=range(0, 302), sort_columns=['EstacaoCodigo', 'Data', 'Hora'], output_filename='qualagua')
concatenar_arquivos_csv(nome='RESUMO DESCARGA', prefixo='ResumoDescarga', skiprows=10, date_columns=[2, 3], sort_columns=['EstacaoCodigo', 'Data', 'Hora'], output_filename='resumodescarga')
concatenar_arquivos_csv(nome='SEDIMENTOS', prefixo='sedimentos', skiprows=10, date_columns=[2, 3, 5, 6], sort_columns=['EstacaoCodigo', 'Data', 'Hora', 'NumMedicao', 'DataLiq', 'HoraLiq', 'NumMedicaoLiq'], output_filename='sedimentos')
concatenar_arquivos_csv(nome='VAZÕES', prefixo='vazoes', skiprows=13, date_columns=[2, 3], sort_columns=['EstacaoCodigo', 'Data', 'Hora'], output_filename='vazoes')

print('CONCLUÍDO!')

print()

print(f'Arquivos com erro: {print(*arquivos_com_erro_nao_tratados, sep=", ")}')
