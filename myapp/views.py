import os
import json
from pathlib import Path
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from googletrans import Translator

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.


def chat(req, message):
    load_dotenv()
    api_key = os.environ.get('HF_TOKEN')
    client = InferenceClient(api_key=api_key)
    # session 디렉토리에 있는 message.json 파일 경로
    session_path = rf'{Path(__file__).parents[1]}\session\messages.json'
    # 한글 사용을 위해 한글 -> 영어로 답변 생성한 다음, 영어 -> 한글로 응답
    translator = Translator(service_urls=['translate.google.com'])
    trans_message = translator.translate(message, dest='en', src='ko').text

    # Messages를 가져온 다음, 현재 요청한 message 추가
    with open(session_path, encoding='utf-8', errors='ignore') as f:
        messages = json.load(f)
    trans_message = {"role": "user", "content": trans_message}
    messages.append(trans_message)
    
    # ChatBot 대답
    completion = client.chat.completions.create(
                                                    model="meta-llama/Llama-3.2-3B-Instruct", 
                                                    messages=messages, 
                                                    max_tokens=500
                                                )
    completion = completion.choices[0].message.content

    response = {"role": "assistant", "content": completion}
    messages.append(response)

    with open(session_path, mode='w', encoding='utf-8', errors='ignore') as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)
    
    trans_completion = translator.translate(completion, dest='ko', src='en').text

    return HttpResponse(trans_completion, content_type='text/plain')


def invest_chat(req, invest_rank):
    load_dotenv()
    api_key = os.environ.get('HF_TOKEN')
    client = InferenceClient(api_key=api_key)
    # 한글 사용을 위해 한글 -> 영어로 답변 생성한 다음, 영어 -> 한글로 응답
    translator = Translator(service_urls=['translate.google.com'])

    invest_rank = invest_rank.replace('_', '')

    messages = [
                    {
                        "role": "system",
                        "content": "You are an analyst who answers questions accurately based on coin data and newspaper articles."
                    },
                    {
                        "role": "user",
                        "content": f"My investment tendency is {invest_rank}. Please recommend financial cryptocurrencies and stocks that suit my investment preferences and explain the reasons."
                    }
                ]
    
    # ChatBot 대답
    completion = client.chat.completions.create(
                                                    model="meta-llama/Llama-3.2-3B-Instruct", 
                                                    messages=messages, 
                                                    max_tokens=500
                                                )
    completion = completion.choices[0].message.content
    

    trans_completion = translator.translate(completion, dest='ko', src='en').text
    final_completion = f'당신의 투자 성향은 {invest_rank}입니다. {trans_completion}'
    response_dict = {'response': final_completion}

    return JsonResponse(response_dict, json_dumps_params={'ensure_ascii': False}, safe=False, status=200)