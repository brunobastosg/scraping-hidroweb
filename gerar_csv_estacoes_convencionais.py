import pandas as pd

df = pd.read_json('estacoes_convencionais.json')

df.to_csv('estacoes_convencionais.csv', sep=';', index=False, encoding='utf-8-sig')