#importing libraries
from typing import List

from langchain.schema import Document
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter #for chunking
from langchain.embeddings import HuggingFaceEmbeddings


#Extract data from PDF files
def load_pdf_file(data):
    loader = DirectoryLoader(data, glob="*.pdf",loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents


# filter important data from the extracted document
def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    """
    Given a list of Document objects, return a new list of Document objects 
    containing only 'source' in metdata and the original page_content.
    """
    
    minimal_docs : List[Document] = []
    for doc in docs:
        src = doc.metadata.get("source")
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source":src}

            )
        )
    return minimal_docs


#Split the data into text chunks
def text_split(minimal_docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20, #for understanding the context
    )
    texts = text_splitter.split_documents(minimal_docs)
    return texts



#Download emebedings from Huggingface 
def download_hugging_face_embeddings():
    """
    Downaload  and return the Huggingface embeddings models.
    """
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name
        )
    return embeddings

embedding = download_hugging_face_embeddings()