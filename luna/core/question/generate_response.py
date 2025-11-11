import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def get_answer(question, max_tokens=50, outputs=1):
    key = os.getenv('openai_key')
    client = OpenAI(api_key=key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}],
        max_tokens=max_tokens,
        n=outputs
    )
    return response.choices[0].message.content
