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
  if request.method == 'POST':
    time.sleep(5)
    response['msg'] = 'hello world'
  return JsonResponse(response)

def getItem(request, id):
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
def createItem(request):
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
        chat_history='{}'
      )
      chatItem.save()
    elif body['type'] == 'custom':
      response['id'] = uuid.uuid4()
    else:
      pass
  return JsonResponse(response)