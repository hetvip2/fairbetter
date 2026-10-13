# app.py
import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from web_scraping.pdf_parser import extract_text_from_pdf  # Ensure correct import
from web_scraping.gemini_user import configure_gemini, extract_skills

app = Flask(__name__)

configure_gemini()

app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    """
    check if ok
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    """
    Endpoint to upload a resume PDF and extract top 5 skills.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request."}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected for uploading."}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        try:
            # Extract text from PDF
            resume_text = extract_text_from_pdf(file.stream)

            # Extract skills using Gemini API
            top_skills = extract_skills(resume_text, top_n=5)

            return ({"top_skills": top_skills}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Allowed file types are pdf."}), 400

