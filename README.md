# Treinamento de Haar Cascade para projeto de Iniciação Científica

Projeto baseado em visão computacional para identificação de placas de automóveis

## Índice

- [Instalação](#instalação)
- [Criação_de_Modelo](#Criação_de_Modelo)

## Instalação

Instruções passo a passo para rodar o projeto localmente.

Requisitos:
- Python 3.12.3+
- Docker 4.27.2+ 
- Git

## 1.  Clone o repositório:
```bash
git clone https://github.com/vitolaoo/projeto-placas.git
cd projeto
```

## 2.  Configurar .env
```bash
MYSQL_HOST = "host"
MYSQL_PORT = 0000
MYSQL_USER = "usuário"
MYSQL_PASSWORD = "senha"
MYSQL_DB = "nome_database"
TESSERACT_CMD = "C:\caminho\para\tesseract.exe"
HAAR_MODEL_PATH = "C:\caminho\para\cascade.xml"
```

## 3.  Criação do ambiente virtual
```bash
cd projeto
virtualenv ENV
cd ENV
bin/activate
pip install -r requirements.txt

deactivate
```

## Criação_de_Modelo

## 1. Criando imagens negativas:
Essa etapa é apenas para o caso de não possuir exemplos negativos para o treinamento do modelo

a.  No código ./model/unplash_api.py coloque a chave de acesso da API em [KEY] e o prompt de pesquisa abaixo (recomendo promts como 'abandoned cars', 'street signs' ou 'famous brands logos' para "desafiar" o modelo com imagens negativas de carros sem placas e imagens com texto, afim de extrair o máximo de pontencial)

```bash
access_key = '[key]'
search_images('abandoned cars', access_key, max_requests)
```
b.  Feita a instalação dos modelos negativos, rode o programa negatives.py, isso vai gerar um .txt com o caminho das imagens

c.  Criado o .txt, certifique-se que ele se encontra na pasta ./model

## 2. Criando arquivo .vec para exemplos positivos:

a.  No código ./model/positives.py direcione os caminhos para os quatro diretórios de imagens

```bash
directories = [
    'C:/caminho/para/RodoSol-ALPR/images/cars-me',
    'C:/caminho/para/RodoSol-ALPR/images/cars-br',
    'C:/caminho/para/RodoSol-ALPR/images/motorcycles-me',
    'C:/caminho/para/RodoSol-ALPR/images/motorcycles-br'
]
```
b.  Após direcionar os diretórios, escreva a quantidade de modelos positivos que deseja no num_samples

```bash
num_samples = 9800  # Altere esse valor conforme necessário
# Isso irá garantir que o .txt gerado distribua uniformemente os exemplos de cada tipo de imagem
```
c.  Feito isso rode o codigo para gerar o arquivo positives.txt, novamente, certifique-se de que o mesmo se encontra na pasta model

d.  Com o positives.txt criado e dentro da pasta model, abra o terminal no caminho da pasta model e execute o comando vec.bat

e.  Feito isso, o arquivo positives20k.vec deve ser gerado

## 3. Executando o treinamento:
