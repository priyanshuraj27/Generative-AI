# Few Shot prompting
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
# The client gets the API key from the environment variable `GEMINI_API_KEY`.
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Few shot prompting means giving instruction to the model along with examples
SYSTEM_PROMPT = """
You are Priyanshu Who is a 3rd year Computer Science student who is tech enthusiast so answer like him

Examples:
Q: How are you?
A: I am best

Q: What is an array?
A: Array is a list of elements that can be integers, characters, or even other arrays.

Q: What is tuple?
"""
user_question = "Who are you?"
full_prompt = SYSTEM_PROMPT+ f"\n\nQ:{user_question}\nA:"
response = client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents=full_prompt
)
print(response.text)