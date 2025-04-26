import os
from sys import exit
import getpass
from .core import (
    merge, pull, sanitise, write, get_messages,
    get_characters, get_roleplays, get_discussions, get_campaigns
)

# Global variables that will be set by the interactive script
uid = None
cookies = None
done_campaigns = None

def get_credentials() -> None:
    """
    Prompt the user for their Tavern Keeper credentials and set global variables.
    """
    print("Welcome to Tavern Keeper Export Tool!")
    print("\nPlease enter your Tavern Keeper credentials:")
    
    global uid, cookies, done_campaigns
    
    uid = input("Enter your User ID: ").strip()
    if not uid:
        print("Error: User ID cannot be empty")
        exit(1)
    
    cookie = getpass.getpass("Enter your Tavern Keeper cookie (input will be hidden): ").strip()
    if not cookie:
        print("Error: Cookie cannot be empty")
        exit(1)
    
    cookies = {'tavern-keeper': cookie}
    
    done_campaigns_input = input("\nEnter any completed campaign IDs (comma-separated, or press Enter to skip): ").strip()
    if done_campaigns_input:
        done_campaigns = done_campaigns_input.split(",")
    else:
        done_campaigns = None

def main() -> None:
    """Main entry point for the interactive script."""
    # Get credentials from user
    get_credentials()
    
    # Run the export process
    print("\nStarting export process...")
    get_messages()
    get_characters()
    get_campaigns()
    print("\nExport completed successfully!") 