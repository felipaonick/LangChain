# creaimo la funzione che dato un nome cerva sul web l'URL del profilo linkedin di tale persona
# perciò utilizziamo la integrazione con linkedin tavily API
# Tavily fornisce le API che consentono il collegamento del LLM col web
# utilizza i motori di ricerca come Google

from langchain_community.tools.tavily_search import TavilySearchResults

def get_profile_url_tavily(name: str) -> str:
    """Searches for Linkedin or Twitter Profile Page."""
    search = TavilySearchResults()
    res = search.run(f'{name}')
    return res[0]['url']