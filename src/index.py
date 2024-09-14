import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from supabase import create_client

load_dotenv()

try:
    # Verifique se o diretório 'data' existe no diretório atual
    data_dir = './data'
    if not os.path.exists(data_dir):
        print(f"Diretório '{data_dir}' não encontrado. Criando...")
        os.makedirs(data_dir)
        print(f"Diretório '{data_dir}' criado.")

    # Carregamento de documentos
    loader = DirectoryLoader(data_dir, glob="**/*.txt", loader_cls=lambda path: TextLoader(path, encoding='utf-8'))

    docs = loader.load()

    if not docs:
        print(f"Nenhum documento encontrado em '{data_dir}'. Verifique se existem arquivos .txt neste diretório.")
        exit()

    print(f"Carregados {len(docs)} documentos.")

    # Configuração do splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", "?", "!", " ", ""]
    )

    doc_output = splitter.split_documents(docs)
    print(f"Documentos divididos em {len(doc_output)} chunks.")

    # Configuração do cliente Supabase
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_PRIVATE_KEY')
    
    if not supabase_url or not supabase_key:
        raise ValueError("As variáveis de ambiente SUPABASE_URL e SUPABASE_PRIVATE_KEY devem ser definidas.")

    client = create_client(supabase_url, supabase_key)

    # Criação do vetor store
    embeddings = OpenAIEmbeddings()

    vector_store = SupabaseVectorStore.from_documents(
        doc_output,
        embeddings,
        client=client,
        table_name='documents',
        query_name='match_documents'
    )

    print('Sucesso!')
except Exception as error:
    print(f"Ocorreu um erro: {error}")
    import traceback
    print(traceback.format_exc())