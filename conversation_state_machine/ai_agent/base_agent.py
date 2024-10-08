import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class BaseAgent(ABC):
    def __init__(self):
        self.model = "gpt-4o"
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.system_prompt = ""  # Placeholder to be defined by child classes
        
    @abstractmethod
    def build_prompt(self, *args, **kwargs):
        """
        Abstract method to construct the full prompt.
        To be implemented by subclasses.
        """
        pass

    
    def generate_response_from_llm(self, prompt):
        print ("Try generating response. ")
        completion = self.client.chat.completions.create(
            # Use GPT 3.5 as the LLM
            model=self.model,
            # Pre-define conversation messages for the possible roles 
            messages=prompt
            )
        print ("Successfully generated response. ")
        return completion.choices[0].message.content

    def _parse_conversation_history(self, chat_history):
        conversation_list = []
        if chat_history == "":
            return conversation_list
        parts = chat_history.split("|")
        
        # Initialize an empty list to store the dictionary entries

        # Loop through each part and split by ": " to get role and content
        for part in parts:
            if ":" in part:
                role, content = part.split(":", 1)
                conversation_list.append({"role": role, "content": content})    
        return conversation_list

