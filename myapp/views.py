import os
import json
from pathlib import Path
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from django.shortcuts import render
from django.http import StreamingHttpResponse

# Create your views here.


def chat(req, message):
    load_dotenv()
    api_key = os.environ.get('HF_TOKEN')
    client = InferenceClient(api_key=api_key)
    session_path = rf'{Path(__file__).parents[1]}\session\messages.json'

    # Messages를 가져온 다음, 현재 요청한 message 추가
    with open(session_path) as f:
        messages = json.load(f)
    message = {"role": "user", "content": message}
    messages.append(message)
    
    # ChatBot 대답
    stream = client.chat.completions.create(
                                                model="meta-llama/Llama-3.2-1B-Instruct", 
                                                messages=messages, 
                                                max_tokens=500,
                                                stream=True
                                            )

    completion = [chunk.choices[0].delta.content for chunk in stream]
    response = {"role": "assistant", "content": ''.join(completion)}
    messages.append(response)
    

    with open(session_path, mode='w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

    return StreamingHttpResponse(iter(completion), content_type='text/plain')