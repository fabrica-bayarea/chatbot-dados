from typing import Optional
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores.supabase import SupabaseVectorStore
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from supabase.client import Client, create_client

class DocumentProcessor:
    def __init__(
        self,
        data_dir: str = './data',
        chunk_size: int = 1600,
        chunk_overlap: int = 160
    ):
        self.data_dir = Path(data_dir)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self._ensure_data_directory()
        
    def _ensure_data_directory(self) -> None:
        """Garante que o diretório de dados existe."""
        if not self.data_dir.exists():
            print(f"Diretório '{self.data_dir}' não encontrado. Criando...")
            self.data_dir.mkdir(parents=True, exist_ok=True)
            print(f"Diretório '{self.data_dir}' criado.")

    def load_documents(self) -> list[Document]:
        """Carrega documentos do diretório especificado."""
        loader = DirectoryLoader(
            str(self.data_dir),
            glob="**/*.txt",
            loader_cls=lambda path: TextLoader(path, encoding='utf-8')
        )
        
        docs = loader.load()
        if not docs:
            raise ValueError(f"Nenhum documento encontrado em '{self.data_dir}'. Verifique se existem arquivos .txt neste diretório.")
        
        print(f"Carregados {len(docs)} documentos.")
        return docs

    def split_documents(self, docs: list[Document]) -> list[Document]:
        """Divide os documentos em chunks menores."""
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            is_separator_regex=False,
            separators=["\n\n", "\n"],
        )
        
        doc_chunks = splitter.split_documents(docs)
        print(f"Documentos divididos em {len(doc_chunks)} chunks.")
        return doc_chunks

class SupabaseVectorStoreManager:
    def __init__(self):
        load_dotenv()
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_PRIVATE_KEY')
        self._validate_credentials()
        
    def _validate_credentials(self) -> None:
        """Valida as credenciais do Supabase."""
        if not self.supabase_url or not self.supabase_key:
            raise ValueError(
                "As variáveis de ambiente SUPABASE_URL e SUPABASE_PRIVATE_KEY devem ser definidas."
            )

    def get_client(self) -> Client:
        """Retorna um cliente Supabase configurado."""
        return create_client(self.supabase_url, self.supabase_key)

    def create_vector_store(
        self,
        documents: list[Document],
        table_name: str = 'documents',
        query_name: str = 'match_documents'
    ) -> SupabaseVectorStore:
        """Cria um vector store no Supabase com os documentos fornecidos."""
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small"
        )
        
        return SupabaseVectorStore.from_documents(
            documents=documents,
            embedding=embeddings,
            client=self.get_client(),
            table_name=table_name,
            query_name=query_name
        )

def main():
    try:
        # Inicializa o processador de documentos
        processor = DocumentProcessor()
        
        # Carrega e processa os documentos
        docs = processor.load_documents()
        doc_chunks = processor.split_documents(docs)
        
        # Inicializa o gerenciador do Supabase e cria o vector store
        supabase_manager = SupabaseVectorStoreManager()
        vector_store = supabase_manager.create_vector_store(doc_chunks)
        
        print('Processo concluído com sucesso!')
        
    except Exception as error:
        print(f"Ocorreu um erro: {error}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main()