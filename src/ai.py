
from openai import OpenAI
import dotenv, os


class Model:
    def __init__(self, api_key:str, model:str) -> None:
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def create_response(self, prompt:list[dict], max_tokens:int=2048, response_format:str="text", temperature:float=1.0) -> str:
        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": response_format},
            messages=prompt
        )
        return completion.choices[0].message.content


class Prompts:
    def personality() -> str:
        try: return os.environ["AI_PERSONALITY_PROMPT"]
        except: return dotenv.get_key(".env", "AI_PERSONALITY_PROMPT")

    def create_prompt() -> str:
        with open("config/prompts/creator/create_prompt.txt", "r") as f:
            return f.read()

    def create_name() -> str:
        with open("config/prompts/creator/create_name.txt", "r") as f:
            return f.read()

    def create_bio() -> str:
        with open("config/prompts/creator/create_bio.txt", "r") as f:
            return f.read()
        
    def create_post() -> str:
        with open("config/prompts/create_post.txt", "r") as f:
            return f.read()

    def respond_to_post() -> str:
        with open("config/prompts/respond_to_post.txt", "r") as f:
            return f.read()
