from fastapi import FastAPI, UploadFile, File, HTTPException
from utils.cv_processing_utils import split_cv_into_sections, process_cv, combine_results
from utils.file_extractor import extract_text_from_pdf, extract_text_from_docx
from models.t5_model import OllamaModel

app = FastAPI()

# Initialize the Ollama model
ollama_model = OllamaModel(model_name="llama3.2:3b")

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
    structured_data = ollama_model.process_cv(text)

    # Return the structured data
    return {"structured_data": structured_data}

@app.post("/improve/")
async def improve_cv_endpoint(cv_data: dict):
    """
    Improve the CV by enhancing content and generating suggestions.
    :param cv_data: A dictionary containing structured CV data.
    :return: A dictionary with improved CV content and suggestions.
    """
    improved_data = ollama_model.improve_cv(cv_data)
    return {"improved_data": improved_data}