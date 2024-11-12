# Projeto Spectra DB

O `spectra_db` é uma aplicação para processamento e análise de dados de espectrometria, desenvolvida para converter arquivos MGF em formato CSV, armazená-los em um banco de dados PostgreSQL e permitir a visualização e manipulação desses dados. Este projeto facilita o processamento de grandes quantidades de dados espectrométricos de forma estruturada e eficiente.

## Pré-requisitos

- **Python 3.12 ou superior**
- **PostgreSQL 16**: É essencial que o PostgreSQL 16 esteja instalado e configurado, pois o projeto utiliza recursos compatíveis com esta versão para melhor desempenho e compatibilidade.
- Dependências adicionais estão listadas em `requirements.txt`.

### Instalação das Dependências

Para instalar as dependências Python necessárias, execute o seguinte comando:

```bash
pip install -r requirements.txt 

## Estrutura do projeto
.
├── insert_your_new_mgf_data       # Diretório para adicionar novos arquivos MGF para processamento
│   ├── UNPD_mgf_01.mgf
│   └── UNPD_mgf_02.mgf
├── Readme.md                      # Arquivo de documentação do projeto
├── requirements.txt               # Arquivo de dependências do projeto
├── run_program.bat                # Script de execução para Windows
├── run_program.sh                 # Script de execução para Linux/Mac
├── scripts                        # Diretório contendo scripts principais
│   ├── converting_mgf_to_csv.py   # Script para converter arquivos MGF para formato CSV
│   ├── initial_screen.py          # Tela inicial do programa para iniciar a conversão e visualização dos dados
│   ├── main.py                    # Script principal para controle do fluxo do programa
│   ├── models.py                  # Modelos do banco de dados e funções para manipulação dos dados
│   └── __pycache__                # Diretório de cache gerado automaticamente pelo Python
│       ├── models.cpython-312.pyc
│       └── models_teste.cpython-312.pyc
├── source                         # Diretório contendo arquivos de saída e dados processados
│   └── mgf_output.csv             # Arquivo CSV gerado a partir dos arquivos MGF
└── unpd_mgf_data                  # Diretório contendo o arquivo Parquet gerado
    └── mgf_output.parquet


## Como Executar o Projeto

1. Certifique-se de que o **PostgreSQL 16** está instalado e em execução.
2. Coloque os arquivos MGF que deseja processar no diretório `insert_your_new_mgf_data`.
3. Execute o programa:
   - **No Windows**: execute `run_program.bat`
   - **No Linux/Mac**: execute `run_program.sh`

Esses scripts iniciarão a aplicação, realizando a conversão dos arquivos MGF em CSV (salvos no diretório `source`) e gerando o arquivo Parquet correspondente em `unpd_mgf_data`.

## Scripts Principais

- **converting_mgf_to_csv.py**: Converte arquivos MGF para o formato CSV.

- **initial_screen.py**: Tela inicial do programa, onde o usuário pode iniciar o processo de conversão e visualizar os dados.

- **main.py**: Controla o fluxo principal do programa.

- **models.py**: Define os modelos de dados e as operações de banco de dados para armazenar e manipular os dados convertidos.

## Dados Processados

- **source/mgf_output.csv**: Contém os dados convertidos dos arquivos MGF no formato CSV.
- **unpd_mgf_data/mgf_output.parquet**: Arquivo Parquet contendo os dados em um formato otimizado para análise e armazenamento.
