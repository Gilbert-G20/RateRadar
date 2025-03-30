# Libraries
from fastapi import FastAPI, HTTPException
import urllib3
from bs4 import BeautifulSoup
import os
from urllib3.exceptions import HTTPError, MaxRetryError, TimeoutError
import logging

# Configure logging
logging.basicConfig(
    filename="webscrapper.log",  # Log file name
    level=logging.INFO,          # Log level (INFO, DEBUG, ERROR, etc.)
    format="%(asctime)s - %(levelname)s - %(message)s"  # Log format
)

webscrapper = FastAPI()

@webscrapper.get("/get-value")
async def get_value(url: str):
    # Path to the custom CA certificate (relative path)
    custom_ca_cert = os.path.join(os.path.dirname(__file__), "certificates", "_.bcv.org.ve.crt")
    
    # Initialize a poolmanager
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=custom_ca_cert)
    
    try:
        # Fetch the HTML content of the webpage
        response = http.request('GET', url, timeout=5.0)
    except (HTTPError, MaxRetryError, TimeoutError) as e:
        raise HTTPException(status_code=503, detail=f"Error fetching the webpage: {str(e)}")
    
    # Check if the request was successful
    if response.status != 200:
        raise HTTPException(status_code=response.status, detail="Failed to fetch the webpage.")
    
    try:
        # Parse the HTML content
        soup = BeautifulSoup(response.data, "html.parser")
        
        # Find dolar
        element_id = "dolar"
        element = soup.find(id=element_id)
        if not element:
            raise ValueError(f"No element found with ID '{element_id}'.")
        
        centered_content = element.find(class_="col-sm-6 col-xs-6 centrado")
        if not centered_content:
            raise ValueError(f"No content found inside element with ID '{element_id}'.")
        
        dolar_value = centered_content.text.strip()
        
        # Find euro
        element_id = "euro"
        element = soup.find(id=element_id)
        if not element:
            raise ValueError(f"No element found with ID '{element_id}'.")
        
        centered_content = element.find(class_="col-sm-6 col-xs-6 centrado")
        if not centered_content:
            raise ValueError(f"No content found inside element with ID '{element_id}'.")
        
        euro_value = centered_content.text.strip()
        
        return {"dolar": dolar_value, "euro": euro_value}
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")