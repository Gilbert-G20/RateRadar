# Libraries
from fastapi import FastAPI, HTTPException
import urllib3
from bs4 import BeautifulSoup
import os 

webscrapper = FastAPI()

@webscrapper.get("/get-value")
async def get_value(url: str):
    # Path to the custom CA certificate (relative path)
    custom_ca_cert = os.path.join(os.path.dirname(__file__), "certificates", "_.bcv.org.ve.crt")
    
    # Initialize a poolmanager
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=custom_ca_cert)
    
    # Fetch the HTML content of the webpage
    response = http.request('GET', url)
    
    # Check if the request was successful
    if response.status == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.data, "html.parser")
        
        # Find dolar
        element_id = "dolar"
        element = soup.find(id=element_id)
        
        if element:
            # Find the content of the second class named "centered"
            centered_content = element.find(class_="col-sm-6 col-xs-6 centrado")
            if centered_content:
                dolar_value = centered_content.text.strip()
            else:
                raise HTTPException(status_code=404, detail=f"No content found inside element with ID '{element_id}'.")
        else:
            raise HTTPException(status_code=404, detail=f"No element found with ID '{element_id}'.")
        
        # Find euro
        element_id = "euro"
        element = soup.find(id=element_id)
        
        if element:
            # Find the content of the second class named "centered"
            centered_content = element.find(class_="col-sm-6 col-xs-6 centrado")
            if centered_content:
                euro_value = centered_content.text.strip()
            else:
                raise HTTPException(status_code=404, detail=f"No content found inside element with ID '{element_id}'.")
        else:
            raise HTTPException(status_code=404, detail=f"No element found with ID '{element_id}'.")
        
        return {"dolar": dolar_value, "euro": euro_value}
    
    else:
        raise HTTPException(status_code=response.status, detail="Failed to fetch the webpage.")