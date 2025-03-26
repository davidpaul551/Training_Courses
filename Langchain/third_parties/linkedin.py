import os
import requests
from dotenv import load_dotenv


load_dotenv()
def scrape_linkedin_profile(linkedin_url:str,mock:bool = False):

    if mock:
        linkedin_url = "https://gist.githubusercontent.com/emarco177/859ec7d786b45d8e3e3f688c6c9139d8/raw/5eaf8e46dc29a98612c8fe0c774123a7a2ac4575/eden-marco-scrapin.json"
        response = requests.get(linkedin_url,timeout=10,verify=False)
    else:
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "apikey": os.getenv("API-Key"),
            "linkedInUrl":linkedin_url
        }
        response = requests.get(api_endpoint , params=params , timeout=10)
    data = response.json()
    data ={
        k:v
        for k,v in data.items()
        if v not in ([],"","",None)
        and k not in ["certifications"]
    }
    return data.get('person').get('firstName')

print(scrape_linkedin_profile("url",True))