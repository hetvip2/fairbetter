import json
import google.generativeai as genai
import os
from typing import List
from pydantic import BaseModel
from io import BytesIO
from flask import Flask, request, jsonify 
from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def extract_text_from_json(file_content: bytes) -> str:
    try:
        if isinstance(file_content, list):
            content = file_content
        else:
            content = json.loads(file_content.decode('utf-8'))
        if not isinstance(content, list):
            raise ValueError("JSON file does not contain a list of strings.")
        
        # Join all text elements in the JSON array into a single text block
        return "\n".join(filter(lambda x: isinstance(x, str) and x.strip(), content))
    except Exception as e:
        raise ValueError(f"Error parsing JSON file: {e}")


def generate_tldr(company_info: str) -> str:
    prompt = (
         f"Summarize the following company information into a quick, 1 paragraph blurb about the company, 100 word cap: \n\n"
        f"{company_info}"
    )

    try:
        response = model.generate_content(prompt)
        generated_text = response.to_dict()

        return generated_text
    except Exception as e:
        raise ValueError(f"Error generating summary: {e}")
    
def generate_products(company_info: str) -> str:
    prompt = (
         f"Summarize the following info, exclude intro sentence, 100 word cap\n\n"
        f"{company_info}"
    )

    try:
        response = model.generate_content(prompt)
        generated_text = response.to_dict()

        return generated_text
    except Exception as e:
        raise ValueError(f"Error generating summary: {e}")
    
def generate_questions(company_info: str) -> str:
    prompt = (
         f"Generate three questions you could ask a recruiter based on this info \n\n"
        f"{company_info}"
    )

    try:
        response = model.generate_content(prompt)
        generated_text = response.to_dict()

        return generated_text
    except Exception as e:
        raise ValueError(f"Error generating summary: {e}")

def generate_posquestions(company_info: str) -> str:
    prompt = (
         f"Generate three questions you could ask a recruiter based on this position \n\n"
        f"{company_info}"
    )

    try:
        response = model.generate_content(prompt)
        generated_text = response.to_dict()

        return generated_text
    except Exception as e:
        raise ValueError(f"Error generating summary: {e}")
