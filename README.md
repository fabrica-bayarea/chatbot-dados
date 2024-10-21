# Chatbot de Dados 

Este projeto é responsável por carregar documentos de texto para o Supabase, criando a nossa base de dados vetorial para o chatbot.

## Descrição

O script principal (`index.py`) realiza as seguintes tarefas:

1. Carrega documentos de texto (.txt) de um diretório específico.
2. Divide os documentos em chunks menores.
3. Cria embeddings para esses chunks usando OpenAI.
4. Armazena os embeddings no Supabase para uso posterior em um chatbot.

## Pré-requisitos

- Python 3.x
- Conta no Supabase
- Chave de API do OpenAI

## Instalação

1. Clone o repositório:

```
git clone https://github.com/fabrica-bayarea/chatbot-dados.git
cd chatbot-dados
```

2. Configure o ambiente virtual Python:

```
python -m venv venv
```

3. Ative o ambiente virtual:

- No Windows:
  ```
  venv\Scripts\activate
  ```
- No macOS e Linux:
  ```
  source venv/bin/activate
  ```

4. Instale as dependências:

```
pip install -r requirements.txt
```

5. Configure as variáveis de ambiente:
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```
OPENAI_API_KEY=chave_da_api_do_openai
SUPABASE_PRIVATE_KEY=chave_privada_do_supabase
SUPABASE_URL=url_do_supabase
```

## Uso

1. Coloque seus documentos de texto (.txt) na pasta `src/data/`.

2. Execute o script:

```
python src/index.py
```

3. O script carregará os documentos, criará embeddings e os armazenará no Supabase.

## Estrutura do Projeto

```
chatbot-dados/
│
├── src/
│   ├── index.py
│   └── data/
│       ├── cursos.txt
│       ├── financeiro.txt
│       └── info.txt
│
├── requirements.txt
├── README.md
└── .env
```

## Dependências

- python-dotenv==1.0.1
- langchain==0.3.4
- langchain-community==0.3.3
- langchain-openai==0.2.3
- supabase==2.9.1
- openai==1.52.0