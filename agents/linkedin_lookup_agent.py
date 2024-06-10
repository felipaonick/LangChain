import os
from dotenv import load_dotenv

from tools.tools import get_profile_url_tavily

load_dotenv()
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate

# importiamo anche Tool che sono le interfacce che aiutano agli agenti, chains, o LLM ad
# interagire col mondo esterno
# prende in input una qualsiasi funzione python (ad es funzione per la ricerca online) e la converte in uno strumento LangChain che lo rende
# accessibile al nostro LLM
from langchain_core.tools import Tool

# la funzione create_react_agent() restituisce un agente basato sull'algoritmo React, che usa un LLM che gli abbiamo fornito
# e che dispone degli strumenti (tools) che gli abbiamo dato

# AgentExecutor è il runtime dell'agente. Questo oggetto riceve i nostri suggerimenti e le nostre istruzioni su cosa fare e porta a termine il
# nostro compito
from langchain.agents import (create_react_agent, AgentExecutor)

# scaricare i prompt preconfezionati
from langchain import hub
def lookup(name: str) -> str:
    llm = ChatOpenAI(
        temperature=0,
        base_url="http://localhost:11434/v1",
        api_key="not-needed",
        model="mistral"
    )

    template = """given the full name {name_of_person} I want you to get it me a link to their Linkedin profile page.
    Your answer should contain only a URL without angled brackets"""

    prompt_template = PromptTemplate(
        template=template, input_variables=['name_of_person']
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google for linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the Linkedin Page URL"
        )
    ]

    """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}
    
    Use the following format:
    
    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question
    
    Begin!
    
    Question: {input}
    Thought:{agent_scratchpad}
    """
    # utilizziamo il prompt preconfezionato qui sopra scaricandolo dall'hub. é un prompt per far si che il modello si comporti in ReAct way
    react_prompt = hub.pull("hwchase17/react")

    # creiamo l'agente
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)

    # esecutore runtime
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linkedin_profile_url = result["output"]
    return linkedin_profile_url

if __name__ == "__main__":
    linkedin_url = lookup(name="Eden Marco Udemy")
    print(linkedin_url)