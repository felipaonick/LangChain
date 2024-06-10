# dobbiamo accedere alle variabili d'ambiente
import os

# per fare le richieste HTTP alle API che ci forniscono le info su linkedin
import requests

# dobbiamo caricare le variabili d'ambiente dal file .env
from dotenv import load_dotenv

load_dotenv()

#scriviamo la funzione che fa' funzionare tutto lo scraping
def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """
    scrape information from Linkedin profiles,
    Manually scrape the informaztion from the Linkedin profile
    :param linkedin_profile_url: str
    :param mock: bool
    :return: json
    """

    if mock:
        linkedin_profile_url='https://gist.githubusercontent.com/felipaonick/080050f47ad93e4c0c6d3b0cc62b19f3/raw/2c764645d546e96f8ad345ce143516964f49c265/eden-marco.json'
        response = requests.get(url=linkedin_profile_url, timeout=10)
    else:
        headers = {'Authorization': f'Bearer {os.environ.get('PROXYCURL_API_KEY')}'}
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin/'

        response = requests.get(api_endpoint,
                                params={'url': linkedin_profile_url},
                                headers=headers,
                                timeout=10)

    data = response.json()
    # eliminiamo i campi vuoti
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    return data

if __name__ == "__main__":
    print(scrape_linkedin_profile(linkedin_profile_url='https://www.linkedin.com/in/eden-marco/', mock=True))