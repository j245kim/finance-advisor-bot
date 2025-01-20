import os
import json
from pathlib import Path

from llama_cpp import Llama
from transformers import AutoTokenizer

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.


def chat(req, message):
    model_dir_path = rf'{Path(__file__).parents[1]}\model'
    model_path = rf'{model_dir_path}\llama-3.2-Korean-Bllossom-3B-gguf-Q4_K_M.gguf'
    tokenizer = AutoTokenizer.from_pretrained(model_dir_path)
    model = Llama(model_path)
    # session 디렉토리에 있는 message.json 파일 경로
    session_path = rf'{Path(__file__).parents[1]}\session\messages.json'

    # Messages를 가져온 다음, 현재 요청한 message 추가
    with open(session_path, encoding='utf-8', errors='ignore') as f:
        messages = json.load(f)
    messages.append({"role": "user", "content": message})
    
    # ChatBot 대답
    prompt = tokenizer.apply_chat_template(
                                                messages, 
                                                tokenize = False,
                                                add_generation_prompt=True
                                            )

    prompt = prompt.replace('<|begin_of_text|>', '').replace('<|eot_id|>', '')
    prompt = prompt.replace('<|start_header_id|>', '\n\n<|start_header_id|>').strip()

    generation_kwargs = {
                            "max_tokens":512,
                            "stop":["<|eot_id|>"],
                            "echo":True,
                            "top_p":0.9,
                            "temperature":0.6,
                        }

    resonse_msg = model(prompt, **generation_kwargs)
    completion = resonse_msg['choices'][0]['text'][len(prompt):].strip()

    messages.append({"role": "assistant", "content": completion})
    with open(session_path, mode='w', encoding='utf-8', errors='ignore') as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)
    
    model._sampler.close()
    model.close()

    return HttpResponse(completion, content_type='text/plain')


def invest_chat(req, invest_rank):
    return JsonResponse({'response': '확인'}, json_dumps_params={'ensure_ascii': False}, safe=False, status=200)