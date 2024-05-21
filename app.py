from fastapi import FastAPI, UploadFile, File
import fitz  

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    if not file:
        return {"message": "No upload file sent"}
    
    content = await file.read()
    
     
    pdf_document = fitz.open(stream=content, filetype="pdf")
    pdf_text = ""
    
   
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pdf_text += page.get_text()
    
    return {"filename": file.filename, "content": pdf_text}

@app.post("/uploadFile/")
async def create_upload_file(file: UploadFile = File(...)):
    if not file:
        return {"message": "No upload file sent"}
    
    content = await file.read()
    
    return {"filename": file.filename, "content": content.hex()}
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
