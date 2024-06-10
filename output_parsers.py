from typing import List, Dict, Any
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

# creaimo la nostra classe che sarà il formato di output che vogliamo per le risposte della app LLM
# Pydantic ci aiuta a creare oggetti strutturati
class Summary(BaseModel):
    summary: str = Field(description='summary')
    facts: List[str] = Field(description='Interesting facts about them')

    #creaimo un metodo per convertire in Dict che ci è utile per serializzare l'oggetot pydantic
    def to_dict(self) -> Dict[str, Any]:
        return {'summary': self.summary, 'facts': self.facts}


# ora creaimo l'OutputParser
summary_parser = PydanticOutputParser(pydantic_object=Summary)