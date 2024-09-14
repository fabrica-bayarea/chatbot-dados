# Web Scraping e Resumo de Cursos

Este projeto consiste em um script Python para extrair informações sobre cursos de um site, formatar URLs e gerar resumos usando a API do OpenAI.

## Requisitos

- Python 3.7+
- pip (gerenciador de pacotes do Python)

## Instalação

1. Clone este repositório ou baixe o arquivo para sua máquina local.

2. Instale as dependências necessárias executando o seguinte comando no terminal:

- `pip install playwright beautifulsoup4 requests python-dotenv openai`

3. Instale os navegadores necessários para o Playwright:

- `playwright install`

4. Crie um arquivo `.env` na raiz do projeto e adicione sua chave de API do OpenAI:

- `OPENAI_API_KEY=sua_api_key_aqui`

## Uso

### 1. Extrair Cursos (extrair_cursos.py)

Este script extrai os links dos cursos do site.

Para executar: `python extrair_cursos.py`

Resultado: Gera um arquivo `links.txt` com os URLs dos cursos.

### 2. Formatar URLs (formatar_urls.py)

Este script formata as URLs extraídas.

Para executar: `python formatar_urls.py`

Resultado: Lê o arquivo `links.txt` e gera um arquivo `formatted_urls.txt` com as URLs formatadas.

### 3. Resumir Cursos (resumir_cursos.py)

Este script acessa as URLs dos cursos, extrai informações e gera resumos usando a API do OpenAI.

Para executar: `python resumir_cursos.py`

Resultado: Os resumos são salvos no arquivo `resumos.txt`.

## Notas

- Certifique-se de ter uma conexão estável com a internet ao executar os scripts.
- O script `resumir_cursos.py` requer uma chave de API válida do OpenAI.
- Os scripts podem levar algum tempo para serem executados, dependendo da quantidade de dados a serem processados.

## Problemas Conhecidos

- O script `extrair_cursos.py` pode falhar se o site alterar sua estrutura HTML.
- O script `resumir_cursos.py` pode atingir limites de taxa da API do OpenAI se executado muitas vezes em um curto período.

## Personalização

- Em `extrair_cursos.py`, você pode modificar a URL inicial se necessário.
- Em `resumir_cursos.py`, você pode ajustar a lista `directories` para incluir diferentes URLs de cursos.