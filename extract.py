from argparse import ArgumentParser
from pathlib import Path
import os
import zipfile

parser = ArgumentParser()
parser.add_argument('-i', '--input', help='Diretório onde se encontram os arquivos compactados', required=True)
parser.add_argument('-o1', '--first-output', help='Diretório de saída da primeira extração')
parser.add_argument('-o2', '--second-output', help='Diretório de saída da segunda extração')

args = parser.parse_args()

input_dir = args.input

home_folder = str(Path.home())
first_output = args.first_output if args.first_output else home_folder + '\\hidroweb\\primeira-extracao'
second_output = args.second_output if args.second_output else home_folder + '\\hidroweb\\segunda-extracao'

print('Lendo arquivos localizados em {}'.format(input_dir))

print('Iniciando primeira extração para {}...'.format(first_output))
for file in os.listdir(input_dir):
    print('\tExtraindo arquivo {}...'.format(file))
    with zipfile.ZipFile(input_dir + '\\' + file, 'r') as zip_ref:
        zip_ref.extractall(first_output)
print('Primeira extração concluída!')

print('Iniciando segunda extração para {}...'.format(second_output))
for file in os.listdir(first_output):
    print('\tExtraindo arquivo {}...'.format(file))
    with zipfile.ZipFile(first_output + '\\' + file, 'r') as zip_ref:
        zip_ref.extractall(second_output)
print('Segunda extração concluída!')
