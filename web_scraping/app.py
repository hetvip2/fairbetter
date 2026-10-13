from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS 
import json
import re
from helpers import extract_text_from_json, generate_tldr, generate_products
import logging
from pdf_parser import extract_text_from_pdf
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

@app.route("/about_scrape", methods=['GET'])
def about_scrape():
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'No url provided'}), 400

    about_info = scrape_about_header(url)

    #if no about header found, scrape for link
    if not about_info:
        about_info = scrape_about_link(url)
    #if no about link found, scrape initial webpage p info
    if not about_info:
        about_info = scrape_p_info(url)
    
    if about_info:
        # about_us_json = "about_us_dict.json" #json file
        # with open(about_us_json, 'w', encoding='utf-8') as json_file:
            # json.dump(about_info, json_file, ensure_ascii=False, indent=4) #writes to json file?
        return jsonify({'found': True, 'section': "About us", 'content': " ".join(about_info)})
    else:
        return jsonify({'found': False, 'message': 'No about info found'})

# # scrape for "work," "solution," "products," "technology"
@app.route("/products_scrape", methods=['GET'])
def products_scrape():
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'No url provided'}), 400

    product_info = scrape_product_header(url)

    #if no product header found, scrape for link
    if not product_info:
        product_info = scrape_product_link(url)
    #if no about link found, scrape initial webpage p info
    if not product_info:
        proudct_info = scrape_p_info(url)
    
    if product_info:
        product_json = "product_dict.json" #json file
        with open(product_json, 'w', encoding='utf-8') as json_file:
            json.dump(product_info, json_file, ensure_ascii=False, indent=4) #writes to json file?
        return jsonify({'found': True, 'section': "Products", 'content': " ".join(product_info)})
    else:
        return jsonify({'found': False, 'message': 'No product info found'})
    
def scrape_about_header(url): #returns about_info
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5'])
    about_info = None
    for header in headers:
        if 'about' in header.get_text().strip().lower():
            about_info = []
            for info in header.find_next_siblings():
                if info.name in ['h1', 'h2', 'h3', 'h4', 'h5']:
                    break
                about_info.append(info.get_text().strip())
            break
    return about_info

def scrape_product_header(url): #returns product info
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5'])
    product_info = None
    for header in headers:
        if 'work' or 'solution' or 'technology' or 'product' in header.get_text().strip().lower():
            product_info = []
            for info in header.find_next_siblings():
                if info.name in ['h1', 'h2', 'h3', 'h4', 'h5']:
                    break
                product_info.append(info.get_text().strip())
            break
    return product_info

def scrape_about_link(url): #returns json
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a', href=True)
    about_url = None

    # if not links:
    #     return {'found': False, 'message': 'about us not found'}
    for link in links:
            href = link['href']
            if re.search(r'\babout\b', href, re.IGNORECASE) or 'about' in link.text.lower():
                if href.startswith('/'):
                    about_url = url + href
                elif not href.startswith('http'):
                    about_url = f"{url}/{href}"
                else:
                    about_url = href
                break
    if about_url:
        return scrape_p_info(about_url)

    return None

def scrape_product_link(url): #returns json
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a', href=True)
    product_url = None

    # if not links:
    #     return {'found': False, 'message': 'about us not found'}
    for link in links:
            href = link['href']
            if re.search(r'\bproduct\b', href, re.IGNORECASE) or 'product' in link.text.lower() or re.search(r'\bwork\b', href, re.IGNORECASE) or 'work' in link.text.lower() or re.search(r'\bsolution\b', href, re.IGNORECASE) or 'solution' in link.text.lower() or re.search(r'\btechnology\b', href, re.IGNORECASE) or 'technology' in link.text.lower():
                if href.startswith('/'):
                    product_url = url + href
                elif not href.startswith('http'):
                    product_url = f"{url}/{href}"
                else:
                    product_url = href
                break
    if product_url:
        return scrape_p_info(product_url)

    return None

                
def scrape_p_info(about_url):
    response = requests.get(about_url)
    #response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    info = soup.find_all('p')
    
    about_info = [info_section.get_text().strip() for info_section in info]
    return about_info


#search for the header "About" in the current page
#if not found search for an About href link and then navigate to about page
#once the about page is found, scrape all the <p> to find the about info
#load that parsed data into a json
#if url is given and no about us data is found just scrape all p info

@app.route("/", methods=["GET"])
def basic_route():
    return jsonify({"worked": "worked"}), 200

@app.route("/summarize_company", methods=["POST"])
def summarize_company():
   #url = request.args.get('url')
    try:
        about_data = request.get_json()
        
        if not about_data:
            return jsonify({"error": "No valid content provided."}), 400

        # company_info = extract_text_from_json()
        company_info = about_data.get("content")
        summary = generate_tldr(company_info)
        if not summary:
            return jsonify({"error": "Could not generate a summary."}), 500

        generated_text = (summary['candidates'][0]['content']['parts'][0]['text'])
        if isinstance(generated_text, set):
            generated_text = list(generated_text)
        return jsonify({"summary": generated_text}), 200
    except Exception as e:
        return jsonify({"idk what happened": str(e)}), 500

@app.route("/summarize_products", methods=["POST"])
def summarize_products():
    try:
        about_data = request.get_json()
        
        if not about_data:
            return jsonify({"error": "No valid content provided."}), 400

        # company_info = extract_text_from_json()
        company_info = about_data.get("content")
        summary = generate_products(company_info)
        if not summary:
            return jsonify({"error": "Could not generate a summary."}), 500

        generated_text = (summary['candidates'][0]['content']['parts'][0]['text'])
        if isinstance(generated_text, set):
            generated_text = list(generated_text)
        return jsonify({"summary": generated_text}), 200
    except Exception as e:
        return jsonify({"idk what happened": str(e)}), 500
    
@app.route("/generate_questions", methods=["POST"])
def output_questions():
    try:
        about_data = request.get_json()
        
        if not about_data:
            return jsonify({"error": "No valid content provided."}), 400

        # company_info = extract_text_from_json()
        company_info = about_data.get("content")
        summary = generate_products(company_info)
        if not summary:
            return jsonify({"error": "Could not generate a summary."}), 500

        generated_text = (summary['candidates'][0]['content']['parts'][0]['text'])
        if isinstance(generated_text, set):
            generated_text = list(generated_text)
        return jsonify({"summary": generated_text}), 200
    except Exception as e:
        return jsonify({"idk what happened": str(e)}), 500

@app.route("/generate_posquestions", methods=["POST"])
def output_questions():
    try:
        about_data = request.get_json()
        
        if not about_data:
            return jsonify({"error": "No valid content provided."}), 400

        # company_info = extract_text_from_json()
        company_info = about_data.get("content")
        summary = generate_products(company_info)
        if not summary:
            return jsonify({"error": "Could not generate a summary."}), 500

        generated_text = (summary['candidates'][0]['content']['parts'][0]['text'])
        if isinstance(generated_text, set):
            generated_text = list(generated_text)
        return jsonify({"summary": generated_text}), 200
    except Exception as e:
        return jsonify({"idk what happened": str(e)}), 500
        
    
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
            # top_skills = extract_skills(resume_text, top_n=5)

            return ({"top_skills": resume_text}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Allowed file types are pdf."}), 400

if __name__ == "__main__":
    app.run(debug=True, port=2000)
