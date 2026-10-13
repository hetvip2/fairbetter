import pytest
from unittest.mock import patch, MagicMock
import json
import os
from flask import Flask
from app import app, scrape_about_header, scrape_about_link

ABOUT_JSON = 'about_us_dict.json'

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_scrape_url(client):
    response = client.get('/about_scrape?url=https://accuraty.com/')
    assert response.status_code == 200
    result = json.loads(response.data)

    assert 'found' in result
    assert 'section' in result
    assert 'content' in result

    assert os.path.exists(ABOUT_JSON)

    with open(ABOUT_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert len(data) > 0

def test_scrape_products(client):
    response = client.get('/products_scrape?url=https://www.agtechtools.com/')
    assert response.status_code == 200
    result = json.loads(response.data)

    assert 'found' in result
    assert 'section' in result
    assert 'content' in result

    assert os.path.exists(ABOUT_JSON)

    with open(ABOUT_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert len(data) > 0


mock_about_data = {
     "Home",
    "Join Agtools",
    "Events",
    "Solutions",
    "News & Blogs",
    "About Us",
    "Contact Us",
    "More...",
    "The Ag industry is managed on consignment exposing in particular farmers the most to losses and for the industry to waste and now increased with Covid19 of over 5000 daily in truckloads in the United States and 62,000 daily truckloads in the world.",
    "​",
    "Agtools is a worldwide SaaS platform gathering real-time government and institutional data of over 500 specialty crops and commodities.",
    "",
    "Our platform includes algorithms and M/L for farmers, buyers, and everyone on the supply chain to see and decide how to manage their forecasting and purchase orders.",
    "Contact us:",
    "​​",
    "Agtools Inc.",
    "8502 E. Chapman Avenue.",
    "Suite 137",
    "Orange CA 92869",
    "+1 (714) - 707-4848",
    "info@ag.tools",
    "Orange County, Los Angeles",
    "Salinas, Seattle, Wenatchee,",
    "Puerto Rico, Mexico, Peru, Colombia.",
    "See More | Achieve More"
}

# Test for the summarize_company route
def test_summarize_company(client):
    print("yippee")
    # Send POST request with mock about_data
    response = client.post('/summarize_company', 
                           data=json.dumps(list(mock_about_data)), 
                           content_type='application/json')
    # Assert that the response status code is 200
    assert response.status_code == 200
    
    # Parse the JSON response
    result = json.loads(response.data)
    
    # Assert that the result contains a 'summary' key
    assert 'summary' in result
    
    # Optionally, you can add checks for the content of the summary (e.g., check if the summary text exists)
    assert len(result['summary']) > 0