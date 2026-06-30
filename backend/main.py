from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from gemini import ask_gemini
import pandas as pd
import shutil
import os
from agent import ask_dataframe

app = FastAPI()

# ---------------- CORS ---------------- #

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://excel-analyser-ai-1.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Upload Folder ---------------- #

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Store uploaded dataframe
uploaded_df = None


# ---------------- Home ---------------- #

@app.get("/")
def home():
    return {"message": "ExcelGPT Backend Running"}


# ---------------- Upload Excel ---------------- #

@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    global uploaded_df

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    uploaded_df = pd.read_excel(file_path)

    return {
        "message": f"{file.filename} uploaded successfully!",
        "filename": file.filename,
        "rows": len(uploaded_df),
        "columns": list(uploaded_df.columns),
        "preview": uploaded_df.head().fillna("").to_dict(orient="records")
    }


# ---------------- Chat Model ---------------- #

class ChatRequest(BaseModel):
    question: str


# ---------------- Chat API ---------------- #

from fastapi import HTTPException

@app.post("/chat")
async def chat(data: ChatRequest):
    global uploaded_df

    if uploaded_df is None:
        return {
            "answer": "Please upload an Excel file first."
        }

    excel_data = uploaded_df.head(100).to_json(orient="records", indent=2)

    prompt = f"""
You are an expert Excel Data Analyst.

The following is data from an uploaded Excel file:

{excel_data}

User Question:
{data.question}

Instructions:
- Answer ONLY from the uploaded Excel data.
- Respond in plain English.
- Do NOT return JSON.
- Do NOT return code blocks.
- Explain naturally like ChatGPT.
- If multiple rows match, summarize them in a readable way.
- If the answer is not found, say:
  "The uploaded Excel does not contain this information."
"""

    try:
        answer = ask_gemini(prompt)
        return {"answer": answer}

    except Exception as e:
        print(f"Gemini Error: {e}")
        raise HTTPException(
            status_code=429,
            detail="Gemini API quota exceeded. Please try again later."
        )