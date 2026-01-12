import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")
DATABASE_URL = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME", "pdf_embeddings")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
GOOGLE_EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001")


def ingest_pdf():
    """
    Faz a ingestão de um PDF no banco de dados PostgreSQL com pgVector.

    Passos:
    1. Carrega o PDF
    2. Divide em chunks de 1000 caracteres com overlap de 150
    3. Gera embeddings para cada chunk
    4. Armazena no banco de dados vetorial
    """
    print("=" * 80)
    print("INICIANDO INGESTÃO DO PDF")
    print("=" * 80)

    # Validações
    if not PDF_PATH:
        raise ValueError("PDF_PATH não está configurado no arquivo .env")

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL não está configurado no arquivo .env")

    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(f"PDF não encontrado no caminho: {PDF_PATH}")

    # Escolher qual embeddings usar (prioriza OpenAI se ambas estiverem configuradas)
    if OPENAI_API_KEY:
        print(f"✓ Usando OpenAI Embeddings: {OPENAI_EMBEDDING_MODEL}")
        embeddings = OpenAIEmbeddings(
            model=OPENAI_EMBEDDING_MODEL,
            openai_api_key=OPENAI_API_KEY
        )
    elif GOOGLE_API_KEY:
        print(f"✓ Usando Google Gemini Embeddings: {GOOGLE_EMBEDDING_MODEL}")
        embeddings = GoogleGenerativeAIEmbeddings(
            model=GOOGLE_EMBEDDING_MODEL,
            google_api_key=GOOGLE_API_KEY
        )
    else:
        raise ValueError("Nenhuma API key configurada. Configure OPENAI_API_KEY ou GOOGLE_API_KEY no arquivo .env")

    # 1. Carregar o PDF
    print(f"\n1. Carregando PDF: {PDF_PATH}")
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    print(f"   ✓ {len(documents)} página(s) carregada(s)")

    # 2. Dividir em chunks
    print("\n2. Dividindo documento em chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"   ✓ {len(chunks)} chunks criados")

    # 3. Criar e popular o banco vetorial
    print("\n3. Gerando embeddings e armazenando no PostgreSQL...")
    print(f"   Database: {DATABASE_URL}")
    print(f"   Collection: {COLLECTION_NAME}")

    # Remover collection existente e criar nova
    vectorstore = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=DATABASE_URL,
        use_jsonb=True,
    )

    # Deletar collection existente
    try:
        vectorstore.delete_collection()
        print(f"   ✓ Collection '{COLLECTION_NAME}' existente removida")
    except Exception:
        print(f"   ℹ Collection '{COLLECTION_NAME}' não existia anteriormente")

    # Criar nova collection e adicionar documentos
    vectorstore = PGVector.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        connection=DATABASE_URL,
        use_jsonb=True,
    )

    print(f"   ✓ {len(chunks)} embeddings criados e armazenados com sucesso!")

    print("\n" + "=" * 80)
    print("INGESTÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 80)
    print("\nAgora você pode executar o chat.py para fazer perguntas sobre o documento.")


if __name__ == "__main__":
    try:
        ingest_pdf()
    except Exception as e:
        print(f"\n❌ ERRO durante a ingestão: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
