import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY n'est pas configurée")


client = OpenAI(api_key=api_key)


response = client.responses.create(
    model="gpt-6-luna",
    input="Explique en une phrase ce qu'est Odoo."
)

print(response.output_text)
