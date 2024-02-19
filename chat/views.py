from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, response
from django.views.decorators.csrf import csrf_exempt

import time

response = {}

@csrf_exempt
def index(request, id):
  print('request: ', request.method)
  print('id is -', id)
  if request.method == 'POST':
    print('headers: ', request.headers)
    print('body:    ', request.body)

    time.sleep(5)
    response['msg'] = 'hello world'
  return JsonResponse(response)

@csrf_exempt
def createItem(request):
  if request.method == 'POST':
    response['msg'] = 'item created'
    print('type:  ', request.body)
  return JsonResponse(response)