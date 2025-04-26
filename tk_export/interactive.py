from sys import exit
from getpass import getpass
from .config import Config
from .exporter import TavernKeeperExporter

def get_credentials() -> Config:
    """Prompt user for Tavern Keeper credentials."""
    print("\nPlease enter your Tavern Keeper credentials:")
    
    uid = input("User ID: ").strip()
    if not uid:
        print("Error: User ID cannot be empty")
        exit(1)
        
    cookie = getpass("Cookie: ").strip()
    if not cookie:
        print("Error: Cookie cannot be empty")
        exit(1)
        
    done_campaigns = input("Completed campaign IDs (comma-separated, optional): ").strip()
    done_campaigns = [cid.strip() for cid in done_campaigns.split(',')] if done_campaigns else None
    
    return Config.from_interactive(uid, cookie, done_campaigns)

def main() -> None:
    """Main function for interactive export."""
    config = get_credentials()
    exporter = TavernKeeperExporter(config)
    exporter.export_all()

if __name__ == "__main__":
    main() 