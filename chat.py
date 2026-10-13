import os
from typing import List

import google.generativeai as genai
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel

from io import BytesIO
import pdfminer.high_level
import docx

app = FastAPI(title="FairBetter")

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

class ResumeText(BaseModel):
    resume_text: str

class SkillsResponse(BaseModel):
    top_skills: List[str]

def extract_text_from_file(file_content: bytes, content_type: str) -> str:
    # temporary code -> insert hetvi's code later
    try:
        if content_type == "application/pdf":
            return pdfminer.high_level.extract_text(BytesIO(file_content))
        elif content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(BytesIO(file_content))
            return "\n".join([para.text for para in doc.paragraphs])
        elif content_type == "text/plain":
            return file_content.decode('utf-8')
        else:
            raise ValueError("Unsupported file type.")
    except Exception as e:
        raise ValueError(f"Error extracting text: {e}")

def extract_top_skills(resume_text: str) -> List[str]:
    # gets top 5 skills from the resume text.
    prompt = (
        "Extract the top 5 skills from the following resume and list them as a JSON array:\n\n"
        f"{resume_text}\n\n"
        "Top Skills:"
    )

    try:
        response = model.generate(
            prompt=prompt,
            temperature=0.2,  # lower temperature for more consistent output
            max_tokens=100,    # change later?
            stop_sequences=["\n"]
        )

        skills = response.generations[0].text.strip()

        import json
        top_skills = json.loads(skills)

        return top_skills[:5]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting skills: {e}")

@app.post("/parse_resume", response_model=SkillsResponse)
def parse_resume(resume: ResumeText):
    # parse resume text and extract top 5 skills
    if not resume.resume_text:
        raise HTTPException(status_code=400, detail="Resume text is empty.")

    top_skills = extract_top_skills(resume.resume_text)

    if not top_skills:
        raise HTTPException(status_code=404, detail="No skills found in the resume.")

    return SkillsResponse(top_skills=top_skills)

@app.post("/parse_resume_file", response_model=SkillsResponse)
async def parse_resume_file(file: UploadFile = File(...)):
    # error checking for uploaded file, get top 5 skills. allows text, pdf, docx
    
    # file type test
    supported_types = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain",
    ]

    if file.content_type not in supported_types:
        raise HTTPException(status_code=400, detail="Unsupported file type.")

    try:
        contents = await file.read()
        resume_text = extract_text_from_file(contents, file.content_type)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")

    if not resume_text.strip():
        raise HTTPException(status_code=400, detail="No text found in the uploaded file.")

    top_skills = extract_top_skills(resume_text)

    if not top_skills:
        raise HTTPException(status_code=404, detail="No skills found in the resume.")

    return SkillsResponse(top_skills=top_skills)
