import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("GPT_KEY")

# generates response to message from gpt-3.5 turbo
def get_answer(messages, max_tokens=50, outputs=3):
    response = openai.ChatCompletion.create(
        model = gpt-3.5-turbo,
        messages = messages,
        max_tokens = max_tokens,
        n = outputs
    )
    return response.choices[0].message

