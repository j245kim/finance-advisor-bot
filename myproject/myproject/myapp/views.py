from django.shortcuts import render

import pandas as pd
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from googletrans import Translator

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import io
from django.views.decorators.csrf import csrf_exempt
from gtts import gTTS
# Create your views here.

def GivemeJson(request,input_string):

    answer = int(input_string)

    if answer >= 26:
        response = 'Aggressive_Investment_Type'
    elif answer >= 21:
        response = 'Active_Investment_Type'
    elif answer >= 16:
        response = 'Risk-Neutral_Type'
    elif answer >= 11:
        response = 'Stability-Seeking_Type'
    else :
        response = 'Conservative_Type'

    return JsonResponse({'type':f'{response}'})


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



@csrf_exempt
def tts(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            input_string = data.get('text', '')

            if not input_string:
                return JsonResponse({'error': 'No text provided'}, status=400)

            # TTS 생성
            tts = gTTS(input_string, lang='ko')
            audio_stream = io.BytesIO()
            tts.write_to_fp(audio_stream)
            audio_stream.seek(0)

            # 오디오 파일 반환
            response = HttpResponse(audio_stream, content_type='audio/mpeg')
            response['Content-Disposition'] = 'attachment; filename="tts_audio.mp3"'
            return response
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
