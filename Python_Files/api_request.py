import openai
import os
import base64
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("CHATGPT_KEY")

def chat_with_gpt_image(prompt: str, image_path: str):
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/png;base64,{base64_image}",
                        "detail": "auto"
                    }},
                ]
            }
        ]
    )
    return response.choices[0].message["content"]

def chat_with_gpt_text(prompt: str):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message["content"]

def chat_with_gpt(prompt=None, image_path=None):
    if prompt and image_path:
        return chat_with_gpt_image(prompt, image_path)
    elif prompt:
        return chat_with_gpt_text(prompt)
    elif image_path:
        return chat_with_gpt_image("Describe this image.", image_path)
    else:
        raise ValueError("Must provide at least a prompt or an image.")
