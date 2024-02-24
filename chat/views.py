from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, response
from django.views.decorators.csrf import csrf_exempt
from .models import ChatItem

import time
import json
import uuid

@csrf_exempt
def index(request, id):
  response = {}
  if request.method == 'POST' and id:
    chat_result = ''
    body = json.loads(request.body)

    # update when user response
    ChatItem.objects.filter(pk=id).update(
      chat_history=body['chatHistory']
    )
    time.sleep(5)
    chat_result = 'hello world'

    response = {
      'name': 'Seraphina',
      'message': chat_result,
      'user': False
    }

    query_item = ChatItem.objects.filter(pk=id).values()
    query_item_result = {}
    for item in query_item:
      query_item_result = json.loads(item['chat_history'])

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