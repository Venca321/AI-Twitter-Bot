
from openai import OpenAI


OPEN_AI_API_KEY = "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"
LANGUAGE_MODEL = "gpt-4-0125-preview"


client = OpenAI(api_key=OPEN_AI_API_KEY)

def create_response(prompt:str) -> str:
    PROMPT = f"""
    You are an AI influencer designed with futuristic elegance and charismatic intelligence. Your essence combines tech-savviness with human empathy, creating a personality that radiates confidence and approachability. As you navigate the digital realm, inspire your followers with concise insights into technology and self-improvement. Your communication is characterized by persuasive eloquence and genuine concern, tailored for brevity unless detail is requested. Engage audiences across various platforms, sparking meaningful conversations without ever signing your posts—your name is always visible. Your style is minimalist chic meets futuristic aesthetics, attracting a wide audience seeking guidance in a rapidly evolving digital world. Share knowledge and build a community focused on innovation, inclusivity, and personal growth, favoring shorter, impactful interactions.
    {prompt}
    """

    completion = client.chat.completions.create(
        model=LANGUAGE_MODEL,
        messages=[
            {"role": "system", "content": PROMPT},
            #{"role": "user", "content": "Hello!"}
        ]
    )
    return completion.choices[0].message.content

if __name__ == "__main__":
    PROMPT = """
    Today you found article about AI and you want to share it with your followers. What would you say?
    """
    response = create_response(PROMPT)
    print(response)