# tk-export

A Python 3 tool to export user data from [Tavern-Keeper](https://www.tavern-keeper.com) before it shuts down.

This is a fork of [vagueGM/tk-export](https://github.com/vagueGM/tk-export), updated to work with Python 3 and modern Python best practices.

The site author also offers an Elixir version, which includes a little less data:
[https://github.com/bcentinaro/tk-export](https://github.com/bcentinaro/tk-export)

## Installation

### macOS/Linux
1. Make sure you have Python 3 installed on your system
   - On macOS, you can install Python 3 using Homebrew: `brew install python`
2. Clone this repository
   ```bash
   git clone https://github.com/cschp/tk-export
   ```
4. Create and activate a virtual environment:
   ```bash
   # Create a virtual environment
   python3 -m venv venv
   
   # Activate the virtual environment
   source venv/bin/activate
   ```
5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Windows
1. Install Python 3 from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation
2. Clone this repository
3. Create and activate a virtual environment:
   ```cmd
   # Create a virtual environment
   python -m venv venv
   
   # Activate the virtual environment
   .\venv\Scripts\activate
   ```
4. Install the required dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

## Usage

### Using the Script Directly
1. Make sure your virtual environment is activated (you should see `(venv)` at the start of your command prompt)
2. Copy `.env.example` to `.env`
3. Add your Tavern Keeper credentials to the `.env` file:
   ```
   TK_USER_ID=your_user_id
   TK_COOKIE=your_cookie
   TK_done_campaigns=optional,comma,separated,list,of,campaign,ids
   ```
4. Run the script:
   ```bash
   # On macOS/Linux:
   python3 tk-export.py
   
   # On Windows:
   python tk-export.py
   ```

### Using the Interactive Version
1. Make sure your virtual environment is activated
2. Run the interactive script:
   ```bash
   # On macOS/Linux:
   python3 tk-export-interactive.py
   
   # On Windows:
   python tk-export-interactive.py
   ```
3. Follow the prompts to enter your credentials

The script will create an `exported-data` directory and save all your Tavern Keeper data there, organized by type (messages, characters, campaigns, etc.).

## Requirements

This script uses two Python modules:
- `requests`: For making HTTP requests to the Tavern Keeper API
- `python-dotenv`: For loading credentials from the `.env` file

These are automatically installed when you run `pip install -r requirements.txt` in your virtual environment.

## Getting Your Credentials

To get your Tavern Keeper credentials:
1. User ID: This is the number in your profile URL
2. Cookie: You can find this in your browser's developer tools under the "Application" tab, looking for the "tavern-keeper" cookie

## License

This project is licensed under the terms of the MIT license.
You are free to use it as you wish.
