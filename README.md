# Scraping dos dados do Portal HidroWeb

O Portal HidroWeb é uma ferramenta integrante do Sistema Nacional de Informações sobre Recursos Hídricos (SNIRH) e oferece o acesso ao banco de dados que contém todas as informações coletadas pela Rede Hidrometeorológica Nacional (RHN), reunindo dados de níveis fluviais, vazões, chuvas, climatologia, qualidade da água e sedimentos. Trata-se de uma importante ferramenta para a sociedade e instituições públicas e privadas, pois os dados coletados pelas estações hidrometeorológicas são imprescindíveis para a gestão dos recursos hídricos e diversos setores econômicos, como geração de energia, irrigação, navegação e indústria, além do projeto, manutenção e operação de infraestrutura hidráulica de pequeno e grande porte, como barragens, drenagem pluvial urbana e mesmo bueiros e telhados. Os dados disponíveis no Portal HidroWeb se referem à coleta convencional de dados hidrometeorológicos, ou seja, registros diários feitos pelos observadores e medições feitas em campo pelos técnicos em hidrologia e engenheiros hidrólogos.

## Funcionamento

O objetivo deste script é efetuar o download das séries históricas de todas as estações convencionais, tanto pluviométricas quanto fluviométricas.

> OBS: A construção do script está em andamento e ele pode não funcionar corretamente.

## Requisitos

* Python 3 (obrigatório)
* [pip](https://pypi.org/project/pip/) (desejável)
* [virtualenv](https://virtualenv.pypa.io/en/latest/) (desejável)

## Configuração

1. Clone o repositório;
2. Na pasta do repositório, execute `virtualenv --python=/path/to/python3 .` (substituir `/path/to/python3` pelo caminho de sua instalação do Python 3);
3. Em seguida, execute `bin/pip install -r requirements.txt`.

## Execução

É necessário definir a variável de ambiente `CHROMEDRIVER`, com a localização do [ChromeDriver](https://chromedriver.chromium.org/downloads), ao executar o script.

Na pasta do projeto, digite `CHROMEDRIVER=/path/to/chromedriver bin/python scraping.py` e aguarde (vai demorar algumas horas).
