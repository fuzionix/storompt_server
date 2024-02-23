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
    body = json.loads(request.body)
    print(body)
    ChatItem.objects.filter(pk=id).update(
      title='Rendered Lake',
      genre='Romantic'
    )
    time.sleep(5)
    response['msg'] = 'hello world'
  return JsonResponse(response)

def get_item(request, id):
  response = {}
  if request.method == 'GET' and id:
    queryItem = ChatItem.objects.filter(pk=id).values()
    for item in queryItem:
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
      itemId = uuid.uuid4()
      response['id'] = itemId
      chatItem = ChatItem(
        id=itemId,
        title='Forgotten City',
        title_description='Dive into an entire captivating story just by interacting',
        genre='Fantasy',
        classification='Experience',
        background='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut et massa mi. Aliquam in hendrerit urna. Pellentesque sit amet sapien fringilla, mattis ligula consectetur, ultrices mauris. Maecenas vitae mattis tellus. Nullam quis imperdiet augue. Vestibulum auctor ornare leo, non suscipit magna interdum eu. Curabitur pellentesque nibh nibh, at maximus ante fermentum sit amet. Pellentesque commodo lacus at sodales sodales. Quisque sagittis orci ut diam condimentum, vel euismod erat placerat.',
        chat_history='[{"name":"SeraphinaWindwhisper","message":"Item created successfully","user":false},{"name":"You","message":"Nice","user":true}, {"name":"SeraphinaWindwhisper","message":"Et penatibus ut mauris tellus pharetra aliquet vestibulum nunc diam. Tristique duis sed sed fermentum vel.","user":false}]'
      )
      chatItem.save()
    elif body['type'] == 'custom':
      response['id'] = uuid.uuid4()
    else:
      pass
  return JsonResponse(response)