import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()

api_key = os.getenv('OPENAI_API_KEY_sesac')

model = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)
response = model.invoke("Hello, world!")
print(response)