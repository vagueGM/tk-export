from datetime import datetime
from typing import Optional, List
from .config import Config
from .api import TavernKeeperAPI
from .storage import Storage

class TavernKeeperExporter:
    """Main class for exporting data from Tavern Keeper."""
    
    def __init__(self, config: Config):
        """Initialize the exporter with configuration."""
        self.config = config
        self.api = TavernKeeperAPI(config)
        self.storage = Storage(config)

    def export_messages(self) -> None:
        """Export all messages."""
        messages = self.api.get_messages()
        
        for message in messages['messages']:
            mid = str(message['id'])
            name = message['name']
            print(f'+++ {name}')

            message_data = self.api.get_message(mid)
            comments = self.api.get_message_comments(mid)
            self.api._merge_data(message_data, comments)

            if len(message_data['comments']) > 0:
                date = message_data['comments'][0]['updated_at']
            else:
                date = message_data['updated_at']
            date = datetime.strptime(date, '%Y-%m-%d %I:%M %p')

            self.storage.write_json(message_data, 'messages', name, date)

    def export_characters(self) -> None:
        """Export all characters."""
        characters = self.api.get_characters()
        archived_characters = self.api.get_characters(archived=True)
        self.api._merge_data(characters, archived_characters)

        for character in characters['characters']:
            cid = str(character['id'])
            name = character['name']
            print(f'+++ {name}')

            character_data = self.api.get_character(cid)
            if character_data == {}:
                continue

            date = datetime.fromtimestamp(character_data['created_at']/1000)
            self.storage.write_json(character_data, 'characters', name, date)

            # Download and save character portrait
            portrait_url = character_data['image_url']
            response = self.api.session.get(portrait_url, stream=True)
            if response.status_code != 200:
                print(f"Error {response.status_code}: portrait download failed")
                continue

            self.storage.write_image(response.content, 'characters', name, date)

    def export_campaigns(self) -> None:
        """Export all campaigns."""
        campaigns = self.api.get_campaigns()

        for campaign in campaigns['campaigns']:
            cid = str(campaign['id'])
            if self.config.done_campaigns and cid in self.config.done_campaigns:
                continue
                
            campaign_name = campaign['name']
            print(f'++ {campaign_name}')
            campaign_name = self.storage.sanitize_filename(campaign_name)

            self.export_campaign_roleplays(cid, campaign_name)
            self.export_campaign_discussions(cid, campaign_name)

    def export_campaign_roleplays(self, campaign_id: str, campaign_name: str) -> None:
        """Export roleplays for a specific campaign."""
        roleplays = self.api.get_campaign_roleplays(campaign_id)

        for roleplay in roleplays['roleplays']:
            rid = str(roleplay['id'])
            name = roleplay['name']
            print(f'+++ {name}')
            
            roleplay_data = self.api.get_roleplay(rid)
            messages = self.api.get_roleplay_messages(rid)
            self.api._merge_data(roleplay_data, messages)

            for message in roleplay_data['messages']:
                if message['comment_count'] > 0:
                    mid = str(message['id'])
                    comments = self.api.get_roleplay_message_comments(rid, mid)
                    self.api._merge_data(message, comments)

            date = datetime.fromtimestamp(roleplay_data['created_at']/1000)
            self.storage.write_json(roleplay_data, f'campaigns/{campaign_name}/roleplays', name, date)

    def export_campaign_discussions(self, campaign_id: str, campaign_name: str) -> None:
        """Export discussions for a specific campaign."""
        discussions = self.api.get_campaign_discussions(campaign_id)

        for discussion in discussions['discussions']:
            did = str(discussion['id'])
            name = discussion['name']
            print(f'+++ {name}')
            
            head = self.api.get_discussion(campaign_id, did)
            del head['campaign']
            self.api._merge_data(discussion, head)

            comments = self.api.get_discussion_comments(campaign_id, did)
            self.api._merge_data(discussion, comments)

            date = datetime.fromtimestamp(discussion['created_at']/1000)
            self.storage.write_json(discussion, f'campaigns/{campaign_name}/discussions', name, date)

    def export_all(self) -> None:
        """Export all data from Tavern Keeper."""
        print("\nStarting export process...")
        self.export_messages()
        self.export_characters()
        self.export_campaigns()
        print("\nExport completed successfully!") 