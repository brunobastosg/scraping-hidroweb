# Scraping dos dados do Portal HidroWeb

O Portal HidroWeb é uma ferramenta integrante do Sistema Nacional de Informações sobre Recursos Hídricos (SNIRH) e oferece o acesso ao banco de dados que contém todas as informações coletadas pela Rede Hidrometeorológica Nacional (RHN), reunindo dados de níveis fluviais, vazões, chuvas, climatologia, qualidade da água e sedimentos. Trata-se de uma importante ferramenta para a sociedade e instituições públicas e privadas, pois os dados coletados pelas estações hidrometeorológicas são imprescindíveis para a gestão dos recursos hídricos e diversos setores econômicos, como geração de energia, irrigação, navegação e indústria, além do projeto, manutenção e operação de infraestrutura hidráulica de pequeno e grande porte, como barragens, drenagem pluvial urbana e mesmo bueiros e telhados. Os dados disponíveis no Portal HidroWeb se referem à coleta convencional de dados hidrometeorológicos, ou seja, registros diários feitos pelos observadores e medições feitas em campo pelos técnicos em hidrologia e engenheiros hidrólogos.

## Funcionamento

O objetivo deste script é efetuar o download das séries históricas de todas as estações convencionais, tanto pluviométricas quanto fluviométricas, e enviar o resultado para o Kaggle utilizando GitHub Actions.

## Requisitos

* Python 3.9 (obrigatório)
* [pip](https://pypi.org/project/pip/) (desejável)
* Driver do MS Access (https://www.microsoft.com/en-US/download/details.aspx?id=13255)
   + No Linux ou MacOS, instalar o [mdbtools](https://github.com/mdbtools/mdbtools)

## Configuração

1. Clone o repositório;
1. Na pasta do repositório, execute `python -m venv .venv`;
1. Em seguida, execute `.venv/bin/pip install -r requirements.txt` (se estiver no Linux ou Mac) ou `.venv/Scripts/pip install -r requirements` (se estiver no Windows).

## Execução

Execute os scripts nessa ordem:

1. `python download_dados_dominio.py`
   * Os dados de domínio serão salvos na pasta `dominio`
   * Esse é o único script que precisa ler de um banco MS Access, portanto certifique-se de instalar o driver do MS Access no Windows ou o [mdbtools](https://github.com/mdbtools/mdbtools) no Linux ou MacOS
1. `python obter_estacoes_convencionais.py`
   * Este script obterá um arquivo chamado `ids_estacoes_convencionais.txt`, na raiz do projeto, o qual é necessário para o próximo script
1. `python download_medicoes_estacoes_convencionais.py`
   * Este script salva todas as medições de todas as estações, em formato ZIP, na pasta `downloads` (demora bastante de executar, pois são muitos dados)
1. `python extrair_medicoes_estacoes_convencionais.py -i downloads -o1 primeira-extracao -o2 segunda-extracao`
   * Este script extrai os dados das medições e coloca os CSV's resultantes na pasta `segunda-extracao`
1. `python concatenar_medicoes_estacoes_convencionais.py -i segunda-extracao`
   * Este script concatena os CSV's por assunto e coloca os CSV's resultantes na pasta `csvs-concatenados`

> OBS: os scripts [gerar_csv_estacoes_convencionais.py](./gerar_csv_estacoes_convencionais.py) e [obter_estacoes_telemetricas.py](./obter_estacoes_telemetricas.py) ainda não estão sendo utilizados
