# tk-export

A Python 3 tool to export user data from [Tavern-Keeper](https://www.tavern-keeper.com) before it shuts down.

This is a fork of [vagueGM/tk-export](https://github.com/vagueGM/tk-export), updated to work with Python 3 and modern Python best practices.

The site author also offers an Elixir version, which includes a little less data:
[https://github.com/bcentinaro/tk-export](https://github.com/bcentinaro/tk-export)

## Installation

1. Make sure you have Python 3 installed on your system
   - On macOS, you can install Python 3 using Homebrew: `brew install python`
2. Clone this repository
3. Install the required dependencies:
   ```bash
   # On macOS/Linux:
   pip3 install -r requirements.txt
   
   # On Windows:
   pip install -r requirements.txt
   ```

## Usage

1. Copy `.env.example` to `.env`
2. Add your Tavern Keeper credentials to the `.env` file:
   ```
   TK_USER_ID=your_user_id
   TK_COOKIE=your_cookie
   TK_done_campaigns=optional,comma,separated,list,of,campaign,ids
   ```
3. Run the script:
   ```bash
   python3 tk-export.py
   ```

The script will create an `exported-data` directory and save all your Tavern Keeper data there, organized by type (messages, characters, campaigns, etc.).

## Requirements

This script uses two Python modules:
- `requests`: For making HTTP requests to the Tavern Keeper API
- `python-dotenv`: For loading credentials from the `.env` file

These are automatically installed when you run `pip3 install -r requirements.txt` (or `pip install` on Windows).

## Getting Your Credentials

To get your Tavern Keeper credentials:
1. User ID: This is the number in your profile URL
2. Cookie: You can find this in your browser's developer tools under the "Application" tab, looking for the "tavern-keeper" cookie

## License

This project is licensed under the terms of the MIT license.
You are free to use it as you wish.
