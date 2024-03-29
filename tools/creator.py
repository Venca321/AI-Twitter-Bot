
import sys, os
sys.path.append(f"{os.getcwd()}") # import fix
from src.ai import Model, Prompts
from config.settings import OPEN_AI_API_KEY, LANGUAGE_MODEL
from src.utils import Colors


def get_input(valid_options:list[str]) -> str:
    while True:
        user_input = input("[User]: ").lower()
        if user_input in valid_options: return user_input

def get_bool_input() -> bool:
    return get_input(["y", "n"]) == "y"

def respond(text:str, name:str="The Creator") -> None:
    print(f"{Colors.OK}[{name}]: {text}{Colors.NORMAL}")


if __name__ == "__main__":
    model = Model(OPEN_AI_API_KEY, LANGUAGE_MODEL)

    print("[System]: Please enter a description of the AI influencer's personality:")
    user_personality_desc = input("[User]: ")
    personality_prompt = model.create_response([
        {"role": "system", "content": Prompts.create_prompt()},
        {"role": "user", "content": user_personality_desc}
    ])
    respond(personality_prompt)

    print("\n[System]: Do you have a specific name in mind for the AI influencer? [y/n]")
    has_name = get_bool_input()
    if has_name:
        print("[System]: Please enter the name:")
        ai_name = input("[User]: ")
    else:
        print("[System]: The Creator will now generate a name for the AI influencer.")
        ai_name = model.create_response([
            {"role": "system", "content": Prompts.create_name()},
            {"role": "user", "content": personality_prompt}
        ])
        respond(ai_name)

    print(f"\n[System]: The Creator will now create {ai_name}")
    generated_bio = model.create_response([
        {"role": "system", "content": Prompts.create_bio()},
        {"role": "user", "content": personality_prompt}
    ])
    respond(f"I want this bio please: {generated_bio}", ai_name)

    print("\n[System]: Are you happy with this and want to save it? [y/n]")
    save_prompt = get_bool_input()
    if not save_prompt:
        print("[System]: Ok, goodbye!")
    
    with open("config/prompts/personality.txt", "w") as f: f.write(personality_prompt)
    with open("config/prompts/name.txt", "w") as f: f.write(ai_name)
    with open("config/prompts/bio.txt", "w") as f: f.write(generated_bio)

    print(f"\n[System]: Your prompt was saved. Please create the accounts for the AI influencer with this info:\n--------------------\n{Colors.BOLD}nickname:{Colors.NORMAL} {ai_name}\n{Colors.BOLD}bio:{Colors.NORMAL} {generated_bio}")
