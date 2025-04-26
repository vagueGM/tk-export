import os
from typing import Optional, List, Dict
from dataclasses import dataclass
import dotenv

@dataclass
class Config:
    """Configuration settings for the Tavern Keeper export tool."""
    export_dir: str = 'exported-data'
    sleep_delay: float = 0.5
    host: str = 'https://www.tavern-keeper.com'
    headers: Dict[str, str] = None
    uid: str = None
    cookies: Dict[str, str] = None
    done_campaigns: Optional[List[str]] = None

    def __post_init__(self):
        """Initialize default values after dataclass initialization."""
        if self.headers is None:
            self.headers = {'accept': 'application/json', 'X-CSRF-Token': 'something'}

    @classmethod
    def from_env(cls) -> 'Config':
        """Create a Config instance from environment variables."""
        dotenv.load_dotenv()
        
        uid = os.environ.get('TK_USER_ID')
        cookie_value = os.environ.get('TK_COOKIE', '')
        
        done_campaigns = os.environ.get('TK_done_campaigns')
        if done_campaigns:
            done_campaigns = done_campaigns.split(",")
        
        return cls(
            uid=uid,
            cookies={'tavern-keeper': cookie_value},
            done_campaigns=done_campaigns
        )

    @classmethod
    def from_interactive(cls) -> 'Config':
        """Create a Config instance by prompting the user."""
        import getpass
        
        print("Welcome to Tavern Keeper Export Tool!")
        print("\nPlease enter your Tavern Keeper credentials:")
        
        uid = input("Enter your User ID: ").strip()
        if not uid:
            print("Error: User ID cannot be empty")
            exit(1)
        
        cookie = getpass.getpass("Enter your Tavern Keeper cookie (input will be hidden): ").strip()
        if not cookie:
            print("Error: Cookie cannot be empty")
            exit(1)
        
        done_campaigns_input = input("\nEnter any completed campaign IDs (comma-separated, or press Enter to skip): ").strip()
        done_campaigns = done_campaigns_input.split(",") if done_campaigns_input else None
        
        return cls(
            uid=uid,
            cookies={'tavern-keeper': cookie},
            done_campaigns=done_campaigns
        ) 