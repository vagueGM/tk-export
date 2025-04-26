import requests
from time import sleep
from typing import Dict, Any, Optional
from .config import Config

class TavernKeeperAPI:
    """Client for interacting with the Tavern Keeper API."""
    
    def __init__(self, config: Config):
        """Initialize the API client with configuration."""
        self.config = config
        self.session = requests.Session()
        self.session.headers.update(config.headers)
        self.session.cookies.update(config.cookies)

    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a request to the API and handle pagination."""
        sleep(self.config.sleep_delay)
        url = f"{self.config.host}{endpoint}"
        print(f'GET: {url}')
        
        response = self.session.get(url, params=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return {}
            
        data = response.json()
        
        # Handle pagination
        if 'pages' in data and data['pages'] > 1:
            for page in range(2, data['pages'] + 1):
                params = params or {}
                params['page'] = page
                response = self.session.get(url, params=params)
                if response.status_code != 200:
                    print(f"Error: {response.status_code} {url}")
                    continue
                self._merge_data(data, response.json())
                
        return data

    @staticmethod
    def _merge_data(old: Dict[str, Any], new: Dict[str, Any]) -> None:
        """Merge two dictionaries, handling lists appropriately."""
        for key, value in new.items():
            if isinstance(value, list) and key in old and isinstance(old[key], list):
                old[key].extend(value)
            else:
                old[key] = value

    def get_messages(self) -> Dict[str, Any]:
        """Get all messages."""
        return self._make_request('/api_v0/messages?filter=all')

    def get_message(self, message_id: str) -> Dict[str, Any]:
        """Get a specific message."""
        return self._make_request(f'/api_v0/messages/{message_id}')

    def get_message_comments(self, message_id: str) -> Dict[str, Any]:
        """Get comments for a specific message."""
        return self._make_request(f'/api_v0/messages/{message_id}/comments')

    def get_characters(self, archived: bool = False) -> Dict[str, Any]:
        """Get characters, optionally including archived ones."""
        endpoint = f'/api_v0/users/{self.config.uid}/characters'
        if archived:
            endpoint += '?archived=true'
        return self._make_request(endpoint)

    def get_character(self, character_id: str) -> Dict[str, Any]:
        """Get a specific character."""
        return self._make_request(f'/api_v0/characters/{character_id}')

    def get_campaigns(self) -> Dict[str, Any]:
        """Get all campaigns."""
        return self._make_request(f'/api_v0/users/{self.config.uid}/campaigns')

    def get_campaign_roleplays(self, campaign_id: str) -> Dict[str, Any]:
        """Get roleplays for a specific campaign."""
        return self._make_request(f'/api_v0/campaigns/{campaign_id}/roleplays')

    def get_roleplay(self, roleplay_id: str) -> Dict[str, Any]:
        """Get a specific roleplay."""
        return self._make_request(f'/api_v0/roleplays/{roleplay_id}')

    def get_roleplay_messages(self, roleplay_id: str) -> Dict[str, Any]:
        """Get messages for a specific roleplay."""
        return self._make_request(f'/api_v0/roleplays/{roleplay_id}/messages')

    def get_roleplay_message_comments(self, roleplay_id: str, message_id: str) -> Dict[str, Any]:
        """Get comments for a specific roleplay message."""
        return self._make_request(f'/api_v0/roleplays/{roleplay_id}/messages/{message_id}/comments')

    def get_campaign_discussions(self, campaign_id: str) -> Dict[str, Any]:
        """Get discussions for a specific campaign."""
        return self._make_request(f'/api_v0/campaigns/{campaign_id}/discussions')

    def get_discussion(self, campaign_id: str, discussion_id: str) -> Dict[str, Any]:
        """Get a specific discussion."""
        return self._make_request(f'/api_v0/campaigns/{campaign_id}/discussions/{discussion_id}')

    def get_discussion_comments(self, campaign_id: str, discussion_id: str) -> Dict[str, Any]:
        """Get comments for a specific discussion."""
        return self._make_request(f'/api_v0/campaigns/{campaign_id}/discussions/{discussion_id}/comments') 