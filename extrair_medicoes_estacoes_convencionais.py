import zipfile

from argparse import ArgumentParser
from pathlib import Path

def extrair_arquivos(input_dir, output_dir):
    for file in input_dir.iterdir():
        print(f'\tExtraindo arquivo {file.name}...')
        try:
            with zipfile.ZipFile(file, 'r') as zip_ref:
                zip_ref.extractall(output_dir)
        except:
            print(f'\t\tErro ao extrair arquivo {file.name}. Ignorando.')

def main():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', help='Diretório onde se encontram os arquivos compactados', required=True)
    parser.add_argument('-o1', '--first-output', help='Diretório de saída da primeira extração')
    parser.add_argument('-o2', '--second-output', help='Diretório de saída da segunda extração')
    args = parser.parse_args()

    input_dir = Path(args.input)
    home_folder = str(Path.home())
    first_output = Path(args.first_output) if args.first_output else Path(home_folder, 'hidroweb', 'primeira-extracao')
    second_output = Path(args.second_output) if args.second_output else Path(home_folder, 'hidroweb', 'segunda-extracao')

    print(f'Lendo arquivos localizados em {input_dir}')

    print(f'Iniciando primeira extração para {first_output}...')
    extrair_arquivos(input_dir, first_output)
    print('Primeira extração concluída!')

    print(f'Iniciando segunda extração para {second_output}...')
    extrair_arquivos(first_output, second_output)
    print('Segunda extração concluída!')

if __name__ == "__main__":
    main()
