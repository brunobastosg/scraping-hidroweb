# Scraping dos dados do Portal HidroWeb

O Portal HidroWeb é uma ferramenta integrante do Sistema Nacional de Informações sobre Recursos Hídricos (SNIRH) e oferece o acesso ao banco de dados que contém todas as informações coletadas pela Rede Hidrometeorológica Nacional (RHN), reunindo dados de níveis fluviais, vazões, chuvas, climatologia, qualidade da água e sedimentos. Trata-se de uma importante ferramenta para a sociedade e instituições públicas e privadas, pois os dados coletados pelas estações hidrometeorológicas são imprescindíveis para a gestão dos recursos hídricos e diversos setores econômicos, como geração de energia, irrigação, navegação e indústria, além do projeto, manutenção e operação de infraestrutura hidráulica de pequeno e grande porte, como barragens, drenagem pluvial urbana e mesmo bueiros e telhados. Os dados disponíveis no Portal HidroWeb se referem à coleta convencional de dados hidrometeorológicos, ou seja, registros diários feitos pelos observadores e medições feitas em campo pelos técnicos em hidrologia e engenheiros hidrólogos.

## Funcionamento

O objetivo deste script é efetuar o download das séries históricas de todas as estações convencionais, tanto pluviométricas quanto fluviométricas.

## Requisitos

* Python 3 (obrigatório)
* [pip](https://pypi.org/project/pip/) (desejável)
* Driver do MS Access (https://www.microsoft.com/en-US/download/details.aspx?id=13255)

## Configuração

1. Clone o repositório;
2. Na pasta do repositório, execute `python -m venv .venv`;
3. Em seguida, execute `.venv/bin/pip install -r requirements.txt` (se estiver no Linux ou Mac) ou `.venv/Scripts/pip install -r requirements` (se estiver no Windows).

## Execução

Falta fazer.