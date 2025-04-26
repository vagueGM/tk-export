#!/usr/bin/env python

import requests
from datetime import datetime
from time import sleep
import os
from sys import exit
import json

export_dir = 'exported-data' ## Saved files end up here. Reletive to script.
sleep_delay = 0.5 ## seconds between request, to be polite to the site.

host='https://www.tavern-keeper.com'
headers = { 'accept': 'application/json', 'X-CSRF-Token': 'something', }

def load_settings():
    import dotenv
    dotenv.load_dotenv()

    uid = os.environ.get('TK_USER_ID')
    if not uid:
        print("User ID not provided in .env")

    cookie_value = os.environ.get('TK_COOKIE')
    if not cookie_value:
        print("cookie not provided in .env")
        cookie_value = ''
    cookies = { 'tavern-keeper': cookie_value }

    if not uid or not cookie_value:
        exit(1)

    done_campaigns = os.environ.get('TK_done_campaigns')
    if done_campaigns:
        done_campaigns = done_campaigns.split(",")

    return(uid, cookies, done_campaigns)

uid, cookies, done_campaigns = load_settings()

def merge(old, new):
    for key, value in new.items():
        if type(value) is list and key in old and type(old[key]) is list:
            old[key].extend(value)
        else:
            old[key] = value

def pull(req):
    sleep(sleep_delay)
    url = host+req
    print(f'GET: {url}')
    r = requests.get(url, headers=headers, cookies=cookies)
    if r.status_code != 200:
        print(r.status_code)
        return({})

    data=r.json()

    if ('pages' in data) and data['pages'] > 1:
        params = {}
        for page in range(2, data['pages']+1):
            params['page'] = page
            r = requests.get(url, headers=headers, cookies=cookies, params=params)
            if r.status_code != 200:
                print(r.status_code, url)
            merge(data, r.json())

    return(data)

### Make filenames safer
transTable = { '&': '+' }
for bracket in '[{<':
    transTable.update({ bracket: '(' })
for bracket in ']}>':
    transTable.update({ bracket: ')' })
transTable = str.maketrans(transTable)
def sanitise(name):
    name = name.strip()
    name = name.translate(transTable)
    return ''.join([char if char.isalnum() or char in '-_,.!?()"\'…—' else '_' for char in name])

def write(data, dir, name, date):
    filename = sanitise(name)
    dir = f'{export_dir}/{dir}'
    # dir = sanitise(dir)

    timestamp = date.timestamp()
    date = date.strftime('%Y%m%d%H%M')
    path = os.path.join(dir, f'{date}.{filename}.json')

    print(f'Writing to {path}')

    if not os.path.exists(dir):
        os.makedirs(dir)

    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

    os.utime(path, (timestamp, timestamp))

def get_messages():

    req='/api_v0/messages?filter=all'
    messages = pull(req)

    for message in messages['messages']:
        mid = str(message['id'])
        name = message['name']
        print(f'+++ {name}')

        req=f'/api_v0/messages/{mid}'
        message = pull(req)
        req=f'/api_v0/messages/{mid}/comments'
        comments = pull(req)
        merge(message, comments)

        if len(message['comments']) > 0:
            date = message['comments'][0]['updated_at']
        else:
            date = message['updated_at']
        date = datetime.strptime(date, '%Y-%m-%d %I:%M %p')

        dir = 'messages'
        write(message, dir, name, date)

def get_characters():

    req = f'/api_v0/users/{uid}/characters'
    characters = pull(req)

    req = f'/api_v0/users/{uid}/characters?archived=true'
    archived_characters = pull(req)

    merge(characters, archived_characters)

    for character in characters['characters']:
        cid = str(character['id'])
        name = character['name']
        print(f'+++ {name}')

        req = f'/api_v0/characters/{cid}'
        character = pull(req)
        if character == {}:
            continue

        date = character['created_at']
        date = datetime.fromtimestamp(date/1000)

        dir = 'characters'
        write(character, dir, name, date)


        portrait = character['image_url']
        r = requests.get(portrait, stream=True)
        if r.status_code != 200:
            print(r.status_code, 'portrait download failed')
            continue

        filename = sanitise(name)
        dir = f'{export_dir}/{dir}'

        timestamp = date.timestamp()
        date = date.strftime('%Y%m%d%H%M')
        path = os.path.join(dir, f'{date}.{filename}.jpg')
        print(f'Writing to {path}')

        if not os.path.exists(dir):
            os.makedirs(dir)

        with open(path, 'wb') as f:
            for chunk in r:
                f.write(chunk)

        os.utime(path, (timestamp, timestamp))

def get_roleplays(cid, campaign_name):

    req = f'/api_v0/campaigns/{cid}/roleplays'
    roleplays = pull(req)

    for roleplay_item in roleplays['roleplays']:
        rid = str(roleplay_item['id'])
        name = roleplay_item['name']
        print(f'+++ {name}')
        req = f'/api_v0/roleplays/{rid}'
        roleplay_data = pull(req)

        req = f'/api_v0/roleplays/{rid}/messages'
        messages = pull(req)

        merge(roleplay_data, messages)

        for message in roleplay_data['messages']:
            if message['comment_count'] > 0:
                mid = str(message['id']) 
                req = f'/api_v0/roleplays/{rid}/messages/{mid}/comments'
                comments = pull(req)
                merge(message, comments)

        dir = f'campaigns/{campaign_name}/roleplays'
        date = roleplay_data['created_at']
        date = datetime.fromtimestamp(date/1000)

        write(roleplay_data, dir, name, date)

def get_discussions(cid, campaign_name):

    req = f'/api_v0/campaigns/{cid}/discussions'
    discussions = pull(req)

    for discussion in discussions['discussions']:
        did = str(discussion['id'])
        name = discussion['name']
        print(f'+++ {name}')
        req = f'/api_v0/campaigns/{cid}/discussions/{did}'
        head = pull(req)
        del head['campaign']
        merge(discussion, head)

        req = f'/api_v0/campaigns/{cid}/discussions/{did}/comments'
        comments = pull(req)
        merge(discussion, comments)

        dir = f'campaigns/{campaign_name}/discussions'
        date = discussion['created_at']
        date = datetime.fromtimestamp(date/1000)

        write(discussion, dir, name, date)

def get_campaigns():

    req = f'/api_v0/users/{uid}/campaigns'
    campaigns = pull(req)

    # with open('campaigns.json') as f:
    #     campaigns = json.load(f)

    for campaign in campaigns['campaigns']:
        cid = str(campaign['id'])
        if done_campaigns:
            if cid in done_campaigns:
                continue
        campaign_name = campaign['name']
        print(f'++ {campaign_name}')
        campaign_name = sanitise(campaign_name)

        get_roleplays(cid, campaign_name)
        get_discussions(cid, campaign_name)

    # path = 'campaigns.json'
    # with open(path, 'w') as f:
    #     json.dump(campaigns, f, indent=2)

def test():

    req = f'/api_v0/users/{uid}'
    data = pull(req)

    print(data)

    if 'account' in data:
        print(f'+ {data['name']} logged in')
    else:
        print('+ not logged in')
        exit(2)

test()
get_campaigns()
get_characters()
get_messages()

