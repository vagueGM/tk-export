#!/usr/bin/env python3

import requests
from datetime import datetime
from time import sleep
import os
from sys import exit
import json
from typing import Dict, List, Tuple, Optional, Any

export_dir = 'exported-data' ## Saved files end up here. Reletive to script.
sleep_delay = 0.5 ## seconds between request, to be polite to the site.

host='https://www.tavern-keeper.com'
headers = { 'accept': 'application/json', 'X-CSRF-Token': 'something', }

def load_settings() -> Tuple[str, Dict[str, str], Optional[List[str]]]:
    """
    Load settings from environment variables using python-dotenv.
    
    Returns:
        Tuple containing:
        - User ID
        - Cookies dictionary
        - List of completed campaigns (if any)
    """
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

def merge(old: Dict[str, Any], new: Dict[str, Any]) -> None:
    """
    Merge two dictionaries, handling lists appropriately.
    
    Args:
        old: The dictionary to merge into
        new: The dictionary to merge from
    """
    for key, value in new.items():
        if isinstance(value, list) and key in old and isinstance(old[key], list):
            old[key].extend(value)
        else:
            old[key] = value

def pull(req: str) -> Dict[str, Any]:
    """
    Make a GET request to the Tavern Keeper API and handle pagination.
    
    Args:
        req: The API endpoint to request
        
    Returns:
        Dictionary containing the API response data
    """
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
def sanitise(name: str) -> str:
    """
    Make filenames safer by replacing special characters.
    
    Args:
        name: The string to sanitize
        
    Returns:
        Sanitized string safe for use as a filename
    """
    name = name.strip()
    name = name.translate(transTable)
    return ''.join([char if char.isalnum() or char in '-_,.!?()"\'…—' else '_' for char in name])

def write(data: Dict[str, Any], dir: str, name: str, date: datetime) -> None:
    """
    Write data to a JSON file with proper timestamp.
    
    Args:
        data: The data to write
        dir: Directory to write to
        name: Name of the file
        date: Timestamp to use for the file
    """
    filename = sanitise(name)
    dir = f'{export_dir}/{dir}'

    timestamp = date.timestamp()
    date_str = date.strftime('%Y%m%d%H%M')
    path = os.path.join(dir, f'{date_str}.{filename}.json')
    print(f'Writing to {path}')

    if not os.path.exists(dir):
        os.makedirs(dir)

    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

    os.utime(path, (timestamp, timestamp))

def get_messages() -> None:
    """Fetch and save all messages from the Tavern Keeper API."""
    req = '/api_v0/messages?filter=all'
    messages = pull(req)

    for message in messages['messages']:
        mid = str(message['id'])
        name = message['name']
        print(f'+++ {name}')

        req = f'/api_v0/messages/{mid}'
        message = pull(req)
        req = f'/api_v0/messages/{mid}/comments'
        comments = pull(req)
        merge(message, comments)

        if len(message['comments']) > 0:
            date = message['comments'][0]['updated_at']
        else:
            date = message['updated_at']
        date = datetime.strptime(date, '%Y-%m-%d %I:%M %p')

        dir = 'messages'
        write(message, dir, name, date)

def get_characters() -> None:
    """Fetch and save all characters from the Tavern Keeper API."""
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
        date_str = date.strftime('%Y%m%d%H%M')
        path = os.path.join(dir, f'{date_str}.{filename}.jpg')
        print(f'Writing to {path}')

        if not os.path.exists(dir):
            os.makedirs(dir)

        with open(path, 'wb') as f:
            for chunk in r:
                f.write(chunk)

        os.utime(path, (timestamp, timestamp))

def get_roleplays(cid: str, campaign_name: str) -> None:
    """
    Fetch and save all roleplays for a specific campaign.
    
    Args:
        cid: Campaign ID
        campaign_name: Name of the campaign
    """
    req = f'/api_v0/campaigns/{cid}/roleplays'
    roleplays = pull(req)

    for roleplay in roleplays['roleplays']:
        rid = str(roleplay['id'])
        name = roleplay['name']
        print(f'+++ {name}')
        req = f'/api_v0/roleplays/{rid}'
        roleplay = pull(req)

        req = f'/api_v0/roleplays/{rid}/messages'
        messages = pull(req)

        merge(roleplay, messages)

        for message in roleplay['messages']:
            if message['comment_count'] > 0:
                mid = str(message['id']) 
                req = f'/api_v0/roleplays/{rid}/messages/{mid}/comments'
                comments = pull(req)
                merge(message, comments)

        dir = f'campaigns/{campaign_name}/roleplays'
        date = roleplay['created_at']
        date = datetime.fromtimestamp(date/1000)

        write(roleplay, dir, name, date)

def get_discussions(cid: str, campaign_name: str) -> None:
    """
    Fetch and save all discussions for a specific campaign.
    
    Args:
        cid: Campaign ID
        campaign_name: Name of the campaign
    """
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

def get_campaigns() -> None:
    """Fetch and save all campaigns from the Tavern Keeper API."""
    req = f'/api_v0/users/{uid}/campaigns'
    campaigns = pull(req)

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

def test():

    req = f'/api_v0/users/{uid}'
    data = pull(req)

    print(data)

    if 'account' in data:
        print(f"+ {data['name']} logged in")
    else:
        print('+ not logged in')
        exit(2)

test()
get_campaigns()
get_characters()
get_messages()

