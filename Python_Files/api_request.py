import openai
import os
import json
import base64
import json 
import sys

def get_appdata_path():
    appdata = os.getenv("APPDATA") or os.path.expanduser("~/.config")
    path = os.path.join(appdata, "Peek")
    os.makedirs(path, exist_ok=True)
    return path

def get_config_file():
    return os.path.join(get_appdata_path(), "config.json")

def load_api_key():
    # Try config.json first
    config_file = get_config_file()
    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as f:
                config = json.load(f)
                key = config.get("api_key")
                if key:
                    return key.strip()
        except Exception as e:
            print("Error loading config.json:", e)
    return None

# Set key
openai.api_key = load_api_key()
if not openai.api_key:
    print(" No API key found. Please run Peek to set it up.")
    sys.exit(1)

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
