from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, response
from django.views.decorators.csrf import csrf_exempt
from .models import ChatItem, Story

import replicate

import time
import json
import uuid
import os

rep = replicate.Client(api_token=os.environ.get('REPLICATE_API_TOKEN'))

@csrf_exempt
def index(request, id):
  response = {}
  if request.method == 'POST' and id:
    chat_result = ''
    body = json.loads(request.body)

    print('replicate start')
    for event in rep.stream(
        "meta/llama-2-70b-chat",
        input={
            "debug": False,
            "top_k": 50,
            "top_p": 1,
            "prompt": body['userTextInput'],
            "temperature": 0.5,
            "system_prompt": "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.",
            "max_new_tokens": 250,
            "min_new_tokens": -1
        },
    ):
        print(str(event), end="")
        chat_result += str(event)
    print('')
    print('replicate end')

    # FOR DEBUG
    # chat_result = 'Hello world'

    # update when user response
    ChatItem.objects.filter(pk=id).update(
      chat_history=body['chatHistory']
    )

    response = {
      'name': 'Seraphina',
      'message': chat_result,
      'user': False
    }

    try:
      query_item = ChatItem.objects.filter(pk=id).values()
      query_item_result = []
      for item in query_item:
        query_item_result = json.loads(item['chat_history'])
    except ChatItem.DoesNotExist:
      query_item_result = []

    query_item_result.append(response)

    # update when ai response
    ChatItem.objects.filter(pk=id).update(
      chat_history=json.dumps(query_item_result)
    )
  return JsonResponse(response)

def get_item(request, id):
  response = {}
  if request.method == 'GET' and id:
    query_item = ChatItem.objects.filter(pk=id).values()
    for item in query_item:
      response['id'] = item['id']
      response['title'] = item['title']
      response['title_description'] = item['title_description']
      response['chat_history'] = item['chat_history']
      response['genre'] = item['genre']
      response['classification'] = item['classification']
      response['background'] = item['background']
      response['create_date'] = item['create_date']
  return JsonResponse(response)

@csrf_exempt
def create_item(request):
  response = {}
  if request.method == 'POST':
    body = json.loads(request.body)
    if body['type'] == 'random':
      item_id = uuid.uuid4()
      response['id'] = item_id
      chat_item = ChatItem(
        id=item_id,
        title='Forgotten City',
        title_description='Dive into an entire captivating story just by interacting',
        genre='Fantasy',
        classification='Experience',
        background='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut et massa mi. Aliquam in hendrerit urna. Pellentesque sit amet sapien fringilla, mattis ligula consectetur, ultrices mauris. Maecenas vitae mattis tellus. Nullam quis imperdiet augue. Vestibulum auctor ornare leo, non suscipit magna interdum eu. Curabitur pellentesque nibh nibh, at maximus ante fermentum sit amet. Pellentesque commodo lacus at sodales sodales. Quisque sagittis orci ut diam condimentum, vel euismod erat placerat.',
        chat_history='[{"name":"SeraphinaWindwhisper","message":"Item created successfully","user":false},{"name":"You","message":"Nice","user":true}, {"name":"SeraphinaWindwhisper","message":"Et penatibus ut mauris tellus pharetra aliquet vestibulum nunc diam. Tristique duis sed sed fermentum vel.","user":false}]'
      )
      chat_item.save()
    elif body['type'] == 'custom':
      response['id'] = uuid.uuid4()
    else:
      pass
  return JsonResponse(response)