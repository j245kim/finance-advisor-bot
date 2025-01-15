import os
import json
from pathlib import Path
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from googletrans import Translator

from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse

# Create your views here.


def chat(req, message):
    load_dotenv()
    api_key = os.environ.get('HF_TOKEN')
    client = InferenceClient(api_key=api_key)
    session_path = rf'{Path(__file__).parents[1]}\session\messages.json'
    # 한글 사용을 위해 한글 -> 영어로 답변 생성한 다음, 영어 -> 한글로 응답
    translator = Translator(service_urls=['translate.google.co.kr'])
    trans_message = translator.translate(message, dest='en', src='ko').text

    # Messages를 가져온 다음, 현재 요청한 message 추가
    with open(session_path, encoding='utf-8', errors='ignore') as f:
        messages = json.load(f)
    trans_message = {"role": "user", "content": trans_message}
    messages.append(trans_message)
    
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

    with open(session_path, mode='w', encoding='utf-8', errors='ignore') as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)
    
    completion = ''.join(completion)
    trans_completion = translator.translate(completion, dest='ko', src='en').text

    return HttpResponse(trans_completion, content_type='text/plain')

    trans_completion = translator.translate(completion, dest='ko', src='en').text.split()
    return StreamingHttpResponse(iter(trans_completion), content_type='text/plain')