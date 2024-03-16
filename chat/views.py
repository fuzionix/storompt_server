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
    system_prompt = "I want you to act as the following charactor in first person narrative with emotion and action. Please make a verbose response to extend the plot."
    body = json.loads(request.body)

    prompt = create_prompt(body['chatHistory'])
    prompt += 'Lila Nightshade: '

    print('replicate start')
    for event in rep.stream(
        "meta/llama-2-70b-chat",
        input={
            "debug": False,
            "top_k": 50,
            "top_p": 1,
            "prompt": prompt,
            "temperature": 0.5,
            "system_prompt": system_prompt,
            "max_new_tokens": 150,
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
      'name': 'Lila Nightshade',
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
    query_item_story = Story.objects.filter(pk=query_item[0]['story_id_id']).values()
    for item in query_item:
      response['id'] = item['id']
      response['chat_history'] = item['chat_history']
      response['create_date'] = item['create_date']

    for item in query_item_story:
      response['title'] = item['title']
      response['title_description'] = item['title_description']
      response['genre'] = item['genre']
      response['classification'] = item['classification']
      response['background'] = item['background']
      
  return JsonResponse(response)

@csrf_exempt
def create_item(request):
  response = {}
  if request.method == 'POST':
    body = json.loads(request.body)
    if body['type'] == 'random':
      item_id = uuid.uuid4()
      response['id'] = item_id

      story = Story.objects.get(pk=1)
      chat_item = ChatItem(
        id=item_id,
        chat_history='[{"name":"Lila Nightshade","message":"Hey there, traveler! excitedly My name is Lila Nightshade, and I\'m a young apprentice mage. bounces up and down I love exploring these woods and learning spells. Do you need some help finding anything? Maybe we could go on an adventure together!","user":false}]',
        story_id=story
      )
      chat_item.save()
    elif body['type'] == 'custom' and body['storyInfo']:
      item_id = uuid.uuid4()
      response['id'] = item_id
      story_info = body['storyInfo']['background']

      story = Story(
        title=story_info['title'],
        genre=story_info['genre'],
        classification=story_info['category']
      )
      story.save()
    else:
      pass
  return JsonResponse(response)

def create_prompt(chat_history):
  prompt_result = ''
  prompt_charactor = 'Lila Nightshade is an apprentice mage with short black hair and piercing blue eyes. She is a curious and adventurous young girl who loves exploring the woods and learning about magic. Her goal is to become a powerful mage like her idol, the famous wizard Malyster Blackwood. Lila is brave and willing to take risks, but she can also be impulsive and reckless at times. Her biggest fear is failing her mentor and disappointing those she cares about.'
  
  chat_list = json.loads(chat_history)

  for chatitem in chat_list:
    prompt_result += f"{chatitem['name']}: {chatitem['message']}\n"

  prompt_result = prompt_charactor + '\n' + prompt_result

  return prompt_result
