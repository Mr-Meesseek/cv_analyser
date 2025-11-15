from fastapi import FastAPI, UploadFile, File, HTTPException
from utils.cv_processing_utils import split_cv_into_sections, process_cv, combine_results
from utils.file_extractor import extract_text_from_pdf, extract_text_from_docx
from models.t5_model import T5Model

app = FastAPI()

# Initialize the T5 model
t5_model = T5Model()

@app.post("/upload/")
async def upload_cv(file: UploadFile = File(...)):
    if not file.filename.endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Unsupported file format. Please upload a PDF or DOCX file.")

    # Extract text from the file
    if file.filename.endswith('.pdf'):
        text = extract_text_from_pdf(file.file)
    elif file.filename.endswith('.docx'):
        text = extract_text_from_docx(file.file)

    # Process the CV in chunks
    structured_data = t5_model.process_cv(text)

    # Return the structured data
    return {"structured_data": structured_data}