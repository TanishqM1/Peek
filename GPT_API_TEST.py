import openai
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Access the key
openai.api_key = os.getenv("CHATGPT_KEY")

def chat_with_gpt(prompt: str):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7
)

    return response.choices[0].message["content"]

if __name__ == "__main__":
    user_prompt = input("Enter your question: ")
    reply = chat_with_gpt(user_prompt)
    print("\nResponse:\n", reply)
