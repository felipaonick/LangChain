from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from third_section.linkedin import scrape_linkedin_profile
from dotenv import load_dotenv
# aggiungiamo l'agente che trova il linkedin url della persona
# poi diamo in input tale profilo per scrapare le sue info
from agents.linkedin_lookup_agent import lookup

def ice_breaker_with(name: str):
    linkedin_url = lookup(name)
    # togliamo le parentesi angolari se ci sono
    if ">" and "<" in linkedin_url:
        linkedin_url = linkedin_url.replace("<", "")
        linkedin_url = linkedin_url.replace(">", "")

    linkedin_profile_info = scrape_linkedin_profile(linkedin_profile_url=linkedin_url)
    summary_template = """
        given the LinkedIn information {information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them
        """

    # creaiamo il nostro modello di prompt
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    # creaimo il modello per chattare con l'LLM
    llm = ChatOpenAI(
        temperature=0,
        base_url="http://localhost:11434/v1",
        api_key="not-needed",
        model="mistral",
    )

    chain = summary_prompt_template | llm

    res = chain.invoke(input={"information": linkedin_profile_info})

    return res

if __name__ == "__main__":

    print("Ice Breaker Enter")
    load_dotenv()
    res = ice_breaker_with(name="Eden Marco Udemy")

    print(res)
