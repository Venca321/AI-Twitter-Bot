
from openai import OpenAI



class Model:
    def __init__(self, api_key:str, model:str) -> None:
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def create_response(self, prompt:list[dict]) -> str:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=prompt
        )
        return completion.choices[0].message.content


class Prompts:
    def personality() -> str:
        with open("config/prompts/personality.txt", "r") as f:
            return f.read()

    def create_prompt() -> str:
        with open("config/prompts/system/creator/create_prompt.txt", "r") as f:
            return f.read()

    def create_name() -> str:
        with open("config/prompts/system/creator/create_name.txt", "r") as f:
            return f.read()

    def create_bio() -> str:
        with open("config/prompts/system/creator/create_bio.txt", "r") as f:
            return f.read()

