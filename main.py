from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from starlette import status
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

# pdf
from utils.pdf_text import extract_text_from_pdf, send_text_to_langchain, query_langchain, query_langchain_text

# text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", status_code=status.HTTP_200_OK)
def read_root(): 
    return {"Hello": "World"}   

@app.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload(
    file_type: str = Form(...),
    prompt: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    if file_type == "text":
        if prompt is None:
            raise HTTPException(status_code=400, detail="Prompt is required for text upload")
        text = query_langchain_text(prompt)
        
        return {"message": "Text upload received", "query_result": text}
    elif file_type == "pdf":
        # file is required here
        if file is None:
            raise HTTPException(status_code=400, detail="File is required for PDF upload")
        text =  extract_text_from_pdf(file.file)  # Add await if extract_text_from_pdf is async
        send_text_to_langchain(text)
        query_result = query_langchain(prompt)
        
        return {"message": "PDF upload received", "query_result": query_result}
    else:
        raise HTTPException(status_code=400, detail="Invalid file type")
