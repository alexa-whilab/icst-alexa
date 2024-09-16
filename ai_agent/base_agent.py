import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class BaseAgent(ABC):
    def __init__(self):
        self.model = "gpt-3.5-turbo"
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.system_prompt = ""  # Placeholder to be defined by child classes
        
    @abstractmethod
    def build_prompt(self, *args, **kwargs):
        """
        Abstract method to construct the full prompt.
        To be implemented by subclasses.
        """
        pass

    
    def generate_response_from_llm(self, prompt) -> str:
        completion = self.client.chat.completions.create(
            # Use GPT 3.5 as the LLM
            model=self.model,
            # Pre-define conversation messages for the possible roles 
            messages=prompt
            )
        
        return completion.choices[0].message.content
