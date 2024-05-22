# app.py

from fastapi import FastAPI, UploadFile, File
import fitz  
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain_community.llms import OpenAI
from dotenv import load_dotenv
from model import QueryRequest  # Import the QueryRequest class from model.py

app = FastAPI()

load_dotenv()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    content = await file.read()
    pdf_document = fitz.open(stream=content, filetype="pdf")
    pdf_text = ""

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pdf_text += page.get_text()

    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    chunks = text_splitter.split_text(pdf_text)

    return {"filename": file.filename, "content": chunks}

@app.post("/query/")
async def query_pdf(query_request: QueryRequest):
    content = query_request.content
    query = query_request.query

    embeddings = OpenAIEmbeddings()    
    knowledge_base = FAISS.from_texts(content, embeddings)

    docs = knowledge_base.similarity_search(query=query, k=3)

    llm = OpenAI()
    chain = load_qa_chain(llm, chain_type="stuff")
    response = chain.run(input_documents=docs, question=query)

    return {"answer": response}

if __name__ == '__main__':
    load_dotenv()
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
