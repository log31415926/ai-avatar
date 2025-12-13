# dashscope_http.py
import requests
import os

DASHSCOPE_API_KEY = "sk-28e1ec1fb4d74e69a573e9f6dd8cd2f8"

def generate_image(image_url: str, prompt: str):
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DASHSCOPE_API_KEY}"
    }

    payload = {
        "model": "qwen-image-edit-plus",
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"image": image_url},
                        {"text": prompt}
                    ]
                }
            ]
        },
        "parameters": {
            "n": 2,
            "watermark": False
        }
    }

    resp = requests.post(url, json=payload, headers=headers, timeout=60)
    resp.raise_for_status()
    return resp.json()
