import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_postgres import PGVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME", "pdf_embeddings")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
GOOGLE_EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001")

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""


def get_embeddings():
    """Retorna o modelo de embeddings configurado."""
    if OPENAI_API_KEY:
        return OpenAIEmbeddings(
            model=OPENAI_EMBEDDING_MODEL,
            openai_api_key=OPENAI_API_KEY
        )
    elif GOOGLE_API_KEY:
        return GoogleGenerativeAIEmbeddings(
            model=GOOGLE_EMBEDDING_MODEL,
            google_api_key=GOOGLE_API_KEY
        )
    else:
        raise ValueError("Nenhuma API key configurada. Configure OPENAI_API_KEY ou GOOGLE_API_KEY no arquivo .env")


def get_llm():
    """Retorna o modelo de LLM configurado."""
    if OPENAI_API_KEY:
        # Usando gpt-4o-mini como alternativa ao gpt-5-nano que não existe ainda
        return ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            openai_api_key=OPENAI_API_KEY
        )
    elif GOOGLE_API_KEY:
        # Usando gemini-2.0-flash-exp como alternativa ao gemini-2.5-flash-lite
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            temperature=0,
            google_api_key=GOOGLE_API_KEY
        )
    else:
        raise ValueError("Nenhuma API key configurada. Configure OPENAI_API_KEY ou GOOGLE_API_KEY no arquivo .env")


def format_docs(docs):
    """Formata os documentos recuperados para inserir no contexto."""
    return "\n\n".join([doc.page_content for doc in docs])


def search_prompt(question=None):
    """
    Cria e retorna uma chain de busca RAG (Retrieval-Augmented Generation).

    Se uma pergunta for fornecida, executa a busca e retorna a resposta.
    Caso contrário, retorna a chain para uso posterior.

    Args:
        question: Pergunta do usuário (opcional)

    Returns:
        Se question for None: retorna a chain
        Se question for fornecida: retorna a resposta como string
    """
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL não está configurado no arquivo .env")

    # Obter embeddings e LLM
    embeddings = get_embeddings()
    llm = get_llm()

    # Conectar ao vectorstore
    vectorstore = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=DATABASE_URL,
        use_jsonb=True,
    )

    # Criar retriever com k=10
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 10}
    )

    # Criar o prompt template
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    # Criar a chain RAG
    chain = (
        {
            "contexto": retriever | format_docs,
            "pergunta": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    # Se uma pergunta foi fornecida, executa a busca
    if question:
        return chain.invoke(question)

    # Caso contrário, retorna a chain para uso posterior
    return chain
