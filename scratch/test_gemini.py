import os
import toml
from google import genai

secrets = toml.load(".streamlit/secrets.toml")
api_key = secrets.get("gemini", {}).get("api_key")

try:
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents='hello'
    )
    print("2.5 SUCCESS:", response.text)
except Exception as e:
    print("2.5 ERROR:", e)

try:
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents='hello'
    )
    print("1.5 SUCCESS:", response.text)
except Exception as e:
    print("1.5 ERROR:", e)
