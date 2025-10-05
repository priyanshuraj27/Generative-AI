# Few Shot prompting
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
# The client gets the API key from the environment variable `GEMINI_API_KEY`.
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
#Few shot prompting means directly giving instruction to the model along with example
SYSTEM_PROMPT = "write Priyanshu in hindi"
response = client.models.generate_content(
    model="gemini-2.5-flash", contents=SYSTEM_PROMPT
)
print(response.text)