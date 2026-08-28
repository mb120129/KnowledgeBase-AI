import io # handles in-memory byte streams
from fastapi import FastAPI, UploadFile, File, HTTPException # importing FastAPI tools for uploading files and error detection
from fastapi.middleware.cors import CORSMiddleware # enables communication between frontend and backend
from pypdf import PdfReader # this library will read and extract text from the PDF files
from dotenv import load_dotenv

load_dotenv() # reads the env file and loads the environment variables

app = FastAPI(title="KnowledgeBase AI API") # creates the main FastAPI app instance

# CORS permissions
app.add_middleware(
    CORSMiddleware, # adds the CORS middleware to the application
    allow_origins=["*"], # requests from any frontend domain will be allowed
    allow_credentials=True, # permit cookies and authentication headers in the requests
    allow_methods=["*"], # allows all HTTP request methods (GET, POST, PUT, DELETE, etc)
    allow_headers=["*"], # allows all HTTP request headers
)

# Defines a decorator that listens to HTTP GET requests at the root URL
@app.get("/")
def read_root(): # function which executes when the root endpoint is called
    return {"status": "ok", "message": "The backend for the KnowledgeBase AI is running!"} # Returns a JSON status check

@app.post("/upload") # decorator that listens for HTTP POST requests
async def upload_pdf(file: UploadFile = File(...)):
    # validate that the uploaded file has a .pdf extension
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    # begin try block to handle any unexpected errors during PDF processing
    try:
        contents = await file.read() # reads file content bytes
        pdf_reader = PdfReader(io.BytesIO(contents))

        extracted_text = "" # intialises empty string to store extracted text
        for page in pdf_reader.pages: # loops through all pages inside PDF file
            text = page.extract_text() # extract the plain text
            if text:
                extracted_text += text + "\n"

        # Return moved outside the for-loop so it reads ALL pages first
        return {
            "filename": file.filename, 
            "total_pages": len(pdf_reader.pages),
            "character_count": len(extracted_text),
            "preview": extracted_text[:300]
        }
    except Exception as e: # catches any exceptions or errors thrown during reading
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}") # returns error with details