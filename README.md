# Treinamento de Haar Cascade para projeto de Iniciação Científica

Projeto baseado em visão computacional para identificação de placas de automóveis

## Índice

- [Instalação](#instalação)

## Instalação

Instruções passo a passo para rodar o projeto localmente.

Requisitos:
- Python 3.12.3+
- Docker 4.27.2+ 
- Git

1.  Clone o repositório:
```bash
git clone https://github.com/vitolaoo/projeto-placas.git
cd projeto
```

2.  Configurar .env
```bash
MYSQL_HOST = "host"
MYSQL_PORT = 0000
MYSQL_USER = "usuário"
MYSQL_PASSWORD = "senha"
MYSQL_DB = "nome_database"
TESSERACT_CMD = "C:\caminho\para\tesseract.exe"
HAAR_MODEL_PATH = "C:\caminho\para\cascade.xml"
```

3.  Criação do ambiente virtual
```bash
cd projeto
virtualenv ENV
cd ENV
bin/activate
pip install -r requirements.txt