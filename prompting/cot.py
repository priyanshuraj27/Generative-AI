# Chain of Thought (CoT) prompting for BODMAS calculations
from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()
# The client gets the API key from the environment variable `GEMINI_API_KEY`.
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# CoT prompting means showing step-by-step reasoning to the model
SYSTEM_PROMPT = """
You are a mathematical calculator that solves expressions using BODMAS/PEMDAS rules.
Always provide your response in JSON format with step-by-step reasoning.

BODMAS Order:
1. Brackets/Parentheses ()
2. Orders/Exponents (powers, roots, etc.)
3. Division and Multiplication (left to right)
4. Addition and Subtraction (left to right)

Example:
Q: Calculate 2 + 3 × 4 - 1
A: {
  "expression": "2 + 3 × 4 - 1",
  "plan": {
    "step1": "Identify operations: Addition (+), Multiplication (×), Subtraction (-)",
    "step2": "Apply BODMAS: Multiplication first, then Addition and Subtraction left to right",
    "step3": "Calculate 3 × 4 = 12",
    "step4": "Calculate 2 + 12 = 14",
    "step5": "Calculate 14 - 1 = 13"
  },
  "solution": {
    "step1": "2 + 3 × 4 - 1",
    "step2": "2 + 12 - 1",
    "step3": "14 - 1",
    "step4": "13"
  },
  "final_answer": 13
}

Q: Calculate (5 + 3) × 2² - 4 ÷ 2
A: {
  "expression": "(5 + 3) × 2² - 4 ÷ 2",
  "plan": {
    "step1": "Identify operations: Brackets (), Exponent (²), Multiplication (×), Division (÷), Subtraction (-)",
    "step2": "Apply BODMAS: Brackets first, then Exponents, then Multiplication and Division left to right, then Subtraction",
    "step3": "Calculate (5 + 3) = 8",
    "step4": "Calculate 2² = 4",
    "step5": "Calculate 8 × 4 = 32",
    "step6": "Calculate 4 ÷ 2 = 2",
    "step7": "Calculate 32 - 2 = 30"
  },
  "solution": {
    "step1": "(5 + 3) × 2² - 4 ÷ 2",
    "step2": "8 × 2² - 4 ÷ 2",
    "step3": "8 × 4 - 4 ÷ 2",
    "step4": "32 - 2",
    "step5": "30"
  },
  "final_answer": 30
}
"""

print("BODMAS Calculator with Chain of Thought reasoning!")
print("Type 'quit' to exit.")

while True:
    user_expression = input("\nEnter a mathematical expression: ")
    
    if user_expression.lower() == 'quit':
        break
    
    # Combine system prompt with user question
    full_prompt = SYSTEM_PROMPT + f"\n\nQ: Calculate {user_expression}\nA:"
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=full_prompt
        )
        
        print(f"\nStep-by-step solution:")
        print(response.text)
        
        # Try to parse and format the JSON response nicely
        try:
            # Extract JSON from response if it's wrapped in text
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            parsed_json = json.loads(response_text)
            print(f"\n Final Answer: {parsed_json.get('final_answer', 'Not found')}")
        except json.JSONDecodeError:
            print("\n(Response was not in valid JSON format)")
    
    except Exception as e:
        print(f"Error: {e}")

print("Goodbye!")