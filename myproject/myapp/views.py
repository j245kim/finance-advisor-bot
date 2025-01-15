from django.shortcuts import render
from django.http import JsonResponse
import os
from django.conf import settings
import requests

# Create your views here.

def hello(request):
    return JsonResponse({'message': 'hello'})
def bye(request):
    return JsonResponse({'message': 'bye'})
def whoami(request):
    return JsonResponse({'message': 'ari'})
def greeting(request,name):
    return JsonResponse({'message': f'{name} hello'})

def index(request):
    return render(request, "index.html")

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from huggingface_hub import InferenceClient
from langchain.prompts import ChatPromptTemplate

# Hugging Face API 키 입력
api_key = "YOUR_HF_API_KEY"  # Ensure you replace this with your actual API key
client = InferenceClient(api_key=api_key)

# 프롬프트 템플릿 정의
prompt = ChatPromptTemplate.from_template(
    """You are an analyst who answers questions accurately based on coin data and newspaper articles, English question/Korean question.

#Previous Chat History:
{chat_history}

#Question: 
{question} 

#Context: 
{context} 

#Answer:"""
)

messages = []

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        user_question = request.POST.get('question')

        chat_history = "\n".join([msg['content'] for msg in messages])

        context = "" 

        prompt_input = prompt.format(chat_history=chat_history, question=user_question, context=context)

        try:
            completion = client.chat.completions.create(
                model="meta-llama/Llama-3.2-1B-Instruct",  
                messages=[{"role": "user", "content": prompt_input}],
                max_tokens=500
            )


            bot_reply = completion.choices[0].message['content']

            # Append the new message to the conversation history
            messages.append({"role": "user", "content": user_question})
            messages.append({"role": "assistant", "content": bot_reply})

            # Return the response as JSON
            return JsonResponse({"answer": bot_reply})

        except Exception as e:
            # Handle errors gracefully
            return JsonResponse({"error": str(e)})