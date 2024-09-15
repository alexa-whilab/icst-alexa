import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()


class BaseAgent(ABC):
    def __init__(self):
        self.model = ChatOpenAI(model="gpt-4", 
                                api_key=os.getenv('OPENAI_API_KEY'))
        self.system_prompt = ""  # Placeholder to be defined by child classes
        
    @abstractmethod
    def build_prompt(self, *args, **kwargs):
        """
        Abstract method to construct the full prompt.
        To be implemented by subclasses.
        """
        pass

    
    def generate_response_from_llm(self, system_prompt, human_prompt) -> str:
        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", human_prompt),
        ])

        chain = (chat_prompt | self.model | StrOutputParser())
        response = chain.invoke({})
        return response