
from src.ai import Model, Prompts
from src.twitter import Post
import json


class Bot:
    def __init__(self, api_key:str, model:str) -> None:
        self.model = Model(api_key, model)

    def create_post(self) -> str:
        personality = Prompts.personality()
        output = self.model.create_response(
            [{
                "role": "system", "content": Prompts.create_post().replace("{personality}", personality)
            }],
        )
        if len(output) > 280: raise Exception("Post too long")
        return output

    def respond_to_post(self, post:Post) -> str:
        personality = Prompts.personality()
        output = json.loads(self.model.create_response(
            [{
                "role": "system", "content": Prompts.respond_to_post()
                    .replace("{personality}", personality)
                    .replace("{post}", f"Author: {post.author} ({post.author_tag})\nPosted: {post.text}\n({post.posted})")
            }],
            response_format="json_object"
        ))
        if len(output["comment"]) > 280: raise Exception("Comment too long")
        return output

