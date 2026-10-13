# gemini_client.py
import os
import google.generativeai as genai
import json

def configure_gemini():
    """
    Configures the Gemini API.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

def extract_skills(text, top_n=5):
    """
    gemini api to extract
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
        f"Extract the top {top_n} skills from the following resume text:\n\n{text}. Put in JSON format."
    )
    # Generate content using the Gemini model
    response = model.generate_content(prompt)

    # Access the 'candidates' list in the response
    candidates = response.candidates

    if not candidates or len(candidates) == 0:
        # raise ValueError("No candidates found in the response.")
        return "na"

    # Extract the text from the first candidate
    generated_text = candidates[0].content.parts[0].text
    print(generated_text)
    return generated_text
