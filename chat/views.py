from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, response
from django.views.decorators.csrf import csrf_exempt
from .models import ChatItem, Story, Charactor

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

    audience = define_audience(body['category'])

    print('category: ', body['category'])

    system_prompt = body['background'] + "\n"
    system_prompt += f"I want you to act as { body['targetName'] } in first person narrative with emotion and action. Prevent repeating conversation response. { audience['content'] }. Each response should contain only one sentence."

    prompt = create_prompt(body['chatHistory'], body['targetName'], body['personality'])
    prompt += f"{ body['targetName'] }: "

    print('system_prompt: ', system_prompt)
    print('prompt: ', prompt)

    print('[replicate start]')
    for event in rep.stream(
        "meta/llama-2-70b-chat",
        input={
            "debug": False,
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
    print('[replicate end]')

    # FOR DEBUG
    # chat_result = 'Hello world'
    # chat_result = "Melody Newman: Thank you, Nancy. Your skills will indeed be valuable to me on this journey. I accept your allegiance and welcome you into my service. Peter: Let us proceed at once, for every moment we waste gives our enemies the opportunity to strengthen their hold on Eldrida. We must move quickly and strike decisively if we are to succeed. The fate of our kingdom hangs in the balance, and I will not rest until it is secure. Shall we depart?"

    chat_result = sanitize_chat_result(chat_result)

    # update when user response
    ChatItem.objects.filter(pk=id).update(
      chat_history=body['chatHistory']
    )

    response = {
      'name': body['targetName'],
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

@csrf_exempt
def receive_message(request, id):
  response = {}
  if request.method == 'POST' and id:
    chat_result = ''
    body = json.loads(request.body)

    audience = define_audience(body['category'])

    system_prompt = body['background'] + "\n"
    system_prompt += f"I want you to act as { body['targetName'] } in first person narrative with emotion and action. Prevent repeating conversation response. { audience['content'] }. Each response should contain only one sentence."

    prompt = create_prompt(body['chatHistory'], body['targetName'], body['personality'])
    prompt += f"{ body['targetName'] }: "

    print('system_prompt: ', system_prompt)
    print('prompt: ', prompt)

    print('[replicate start]')
    for event in rep.stream(
        "meta/llama-2-70b-chat",
        input={
            "debug": False,
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
    print('[replicate end]')

    # FOR DEBUG
    # chat_result = 'Hello receive'

    chat_result = sanitize_chat_result(chat_result)

    # update when user response
    ChatItem.objects.filter(pk=id).update(
      chat_history=body['chatHistory']
    )

    response = {
      'name': body['targetName'],
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

    time.sleep(3)

  return JsonResponse(response)

def get_item(request, id):
  response = {}
  response['charactor'] = []
  if request.method == 'GET' and id:
    query_item = ChatItem.objects.filter(pk=id).values()
    try:
      query_item_story = Story.objects.filter(pk=query_item[0]['story_id_id']).values()
    except:
      response = JsonResponse(response)
      response.content = 'Failed to find story by id'
      return response
    
    try:
      query_item_charactor = Charactor.objects.filter(story_id=query_item[0]['story_id_id']).values()
    except:
      response = JsonResponse(response)
      response.content = 'Failed to find charactor by story id'
      return response
        
    for item in query_item:
      response['id'] = item['id']
      response['chat_history'] = item['chat_history']
      response['create_date'] = item['create_date']

    for item in query_item_story:
      response['story_id'] = item['id']
      response['title'] = item['title']
      response['title_description'] = item['title_description']
      response['genre'] = item['genre']
      response['classification'] = item['classification']
      response['background'] = item['background']

    for item in query_item_charactor:
      response['charactor'].append({
        "name": item['name'],
        "personality": item['personality']
      })
      
    response['charactor'] = json.dumps(response['charactor'])
      
  return JsonResponse(response)

@csrf_exempt
def create_item(request):
  response = {}
  if request.method == 'POST':
    item_id = uuid.uuid4()
    response['id'] = item_id

    body = json.loads(request.body)
    
    char_chatitem = [
      {
        "name": "",
        "message": "",
        "user": False
      }
    ]

    if body['type'] == 'random':
      story = Story.objects.get(pk=15)

      char_chatitem[0]["name"] = "Random Fern"
      char_chatitem[0]["message"] = "Hey there, traveler! excitedly My name is Lila Nightshade, and I\'m a young apprentice mage. bounces up and down I love exploring these woods and learning spells. Do you need some help finding anything? Maybe we could go on an adventure together!"

      char_chatitem_json = json.dumps(char_chatitem)

      chat_item = ChatItem(
        id=item_id,
        chat_history=char_chatitem_json,
        story_id=story
      )
      chat_item.save()
    elif body['type'] == 'custom' and body['storyInfo']:
      story_info = body['storyInfo']

      greeting = create_greeting(story_info)

      char_chatitem[0]["name"] = story_info['charactors'][0]['charname']
      char_chatitem[0]["message"] = greeting
      char_chatitem_json = json.dumps(char_chatitem)

      story = Story(
        title=story_info['background']['title'],
        genre=story_info['background']['genre'],
        classification=story_info['background']['category'],
        background=story_info['portrayal']['content'],
        title_description=story_info['portrayal']['content'].split(".")[0],
      )
      story.save()
      story = Story.objects.filter().latest('id')

      charactor = Charactor(
        name=story_info['charactors'][0]['charname'],
        personality=story_info['charactors'][0]['personality'],
        greeting=greeting,
        story_id=story
      )
      charactor.save()

      chat_item = ChatItem(
        id=item_id,
        chat_history=char_chatitem_json,
        story_id=story
      )
      chat_item.save()
    else:
      pass
  return JsonResponse(response)

@csrf_exempt
def create_portrayal(request):
  response = {}
  if request.method == 'POST':
    portrayal_result = ''
    body = json.loads(request.body)
    prompt = f"""
Given are the information of the story.

Story Name: { body['storyInfo']['background']['title'] }
Genre: { body['storyInfo']['background']['genre'] }
Charactor Name: { body['storyInfo']['charactors'][0]['charname'] }
Personalities: { body['storyInfo']['charactors'][0]['personality'] }
    """
      
    audience = define_audience(body['storyInfo']['background']['category'])
    system_prompt = f"You are a professional story maker { audience['class'] }. Please create a portrayal for the story in 2 paragraphes. { audience['content'] }. The portrayal should include parts of story background and charactors."
    print('system_prompt (create_portrayal): ', system_prompt)

    print('[replicate start]')
    for event in rep.stream(
        "meta/llama-2-70b-chat",
        input={
            "debug": False,
            "top_p": 1,
            "prompt": prompt,
            "temperature": 0.5,
            "system_prompt": system_prompt,
            "max_new_tokens": 250,
            "min_new_tokens": -1
        },
    ):
        print(str(event), end="")
        portrayal_result += str(event)
    print('')
    print('[replicate end]')

    portrayal_result = sanitize_chat_result(portrayal_result)
    response['portrayal'] = portrayal_result.strip()

    # FOR DEBUG
    # response['portrayal'] = 'Hello world'
  else:
      pass
  return JsonResponse(response)

@csrf_exempt
def add_charactor(request):
  response = {}
  if request.method == 'POST':
    body = json.loads(request.body)
    if (body['id'] and body['id'] is not None):
      story = Story.objects.get(pk=int(body['id']))
      charactor = Charactor(
        name=body['name'],
        personality=body['personality'],
        greeting='',
        story_id=story
      )
      charactor.save()
    else:
      response = JsonResponse(response)
      response.content = 'Failed to find charactor by story id'
      return response
  else:
    print('Not a POST request')

  response['test'] = 'test'
  return JsonResponse(response)

def create_greeting(story_info):
  greeting_result = ''
  prompt = f"""
Given are the portrayal of the story.

{ story_info['portrayal']['content'] }
    """
  
  audience = define_audience(story_info['background']['category'])
  system_prompt = f"You are the charactor in a conversation. According to the portrayal. Please create a first response (greeting) as { story_info['charactors'][0]['charname'] } for the story { audience['class'] }. { audience['content'] }. The response should match the character's personality given by the portrayal."
  print('system_prompt (create_greeting): ', system_prompt)
  
  print('[replicate start]')
  for event in rep.stream(
      "meta/llama-2-70b-chat",
      input={
          "debug": False,
          "top_p": 1,
          "prompt": prompt,
          "temperature": 0.5,
          "system_prompt": system_prompt,
          "max_new_tokens": 150,
          "min_new_tokens": -1
      },
  ):
      print(str(event), end="")
      greeting_result += str(event)
  print('')
  print('[replicate end]')

  return greeting_result

@csrf_exempt
def undo(request, id):
  response = {}
  if request.method == 'POST' and id:
    body = json.loads(request.body)

    # update when user press undo button
    ChatItem.objects.filter(pk=id).update(
      chat_history=body['chatHistory']
    )

  return JsonResponse(response)

def define_audience(category = 'Primary'):
  audience = {
    "class": "",
    "content": ""
  }

  if (category == 'Primary'):
    audience['class'] = "for kids"
    audience['content'] = "Use words and sentences that kids can understand"
  elif (category == 'Middle'):
    audience['class'] = "for teenagers"
    audience['content'] = "Use words and sentences that teenagers can understand"
  elif (category == 'Advanced'):
    audience['class'] = "for adults"
    audience['content'] = "Use advanced words and advanced sentences for adults"

  return audience

def create_prompt(chat_history, target_name = "The charactor", personality = '[]'):
  prompt_result = ''
  prompt_charactor = f"{target_name} is a {', '.join(eval(personality))} person"

  prompt_result += f"{prompt_charactor} \n"
  
  chat_list = json.loads(chat_history)

  for chatitem in chat_list:
    prompt_result += f"{chatitem['name']}: {chatitem['message'].strip()}\n"

  prompt_result = prompt_result

  return prompt_result

def sanitize_chat_result(result):
  sanitized_result = result
  if (len(result.split(":")) > 1):
    sanitized_result = result.split(":")[1].strip()
  if (result != sanitized_result):
    print('[sanitized detected]')
  return sanitized_result
