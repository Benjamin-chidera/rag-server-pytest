import os
from dotenv import load_dotenv
load_dotenv()

import pdfplumber
from io import BytesIO

from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_ollama import OllamaEmbeddings
# from langchain_chroma import Chroma
# from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# create embeddings
embedding = OllamaEmbeddings(model="llama3.1")

OLLAMA_ENABLED = os.getenv("OLLAMA_ENABLED", "false").lower() == "true"

print(f"OLLAMA_ENABLED: {OLLAMA_ENABLED}")

# Function to extract text from a PDF file
def extract_text_from_pdf(file_object) -> str:
    """Extract text from PDF file object without saving to disk"""
    # Read the file content
    file_content = file_object.read()

    # Create a BytesIO object from the content
    pdf_file = BytesIO(file_content)

    # Open with pdfplumber and extract text
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

    
    return text

# langchain function
def send_text_to_langchain(text: str):
    
    # chunking the text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        # separators=["\n\n", "\n", " ", ""]
    )
    texts = text_splitter.split_text(text)
    
    vector_store = Chroma(
    embedding_function=embedding,
    persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
)
    # store in vector db    
    vector_store.add_texts(texts)

def query_langchain(query: str):
    print("Query received:", query)
    
    vector_store = Chroma(
    embedding_function=embedding,
    persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
)
    
    docs = vector_store.similarity_search(query, k=3)
    
    
    llm = ChatOllama(model="llama3.1", temperature=0, num_predict=512)
    output_parser = StrOutputParser()
    
    messages = [
    ("system", """You are a helpful assistant that provides concise answers based on the provided context.
    
    Note: If the context does not contain relevant information, respond with "I don't know".
    
    Context:
    {context}
    """),
    ("human", "{query}")
    ]

    
    chat = ChatPromptTemplate.from_messages(messages)
    
    chain = chat | llm | output_parser
    return chain.invoke({
        "query": query,
        "context": "\n".join([doc.page_content for doc in docs])
    })
    
    

def query_langchain_text(query: str):
    print("Query received:", query)
    
    if not OLLAMA_ENABLED:
        return "LLM disabled (CI mode)"
    
    
    llm = ChatOllama(model="llama3.1", temperature=0, num_predict=512)
    output_parser = StrOutputParser()
    
    messages = [
    ("system", """You are a helpful assistant that provides concise answers based on the provided context.
          
     Note: make it short and concise.
    """),
    ("human", "{query}")
    ]

    
    chat = ChatPromptTemplate.from_messages(messages)
    
    chain = chat | llm | output_parser
    return chain.invoke({
        "query": query    })
    