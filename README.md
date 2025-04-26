# tk-export

A crude python tool to export user data from
[Tavern-Keeper](https://www.tavern-keeper.com) before it shuts down.

The site author also offers an Elixir version, which includes a little less
data.
[https://github.com/bcentinaro/tk-export](https://github.com/bcentinaro/tk-export)

This repo and scripting is a fork based off of https://github.com/vagueGM/tk-export

## Installation and Setup

1. Create a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install required dependencies:
   ```bash
   pip install requests python-dotenv
   ```

3. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

4. Configure your `.env` file:
   - Add your user id number to the `TK_USER_ID=` line this can be found in the url of your user profile like tavern-keeper.com/user/1234 1234 would be your userid
   - Add your cookie to the `TK_COOKIE=` line to find this go to developer tools -> application tab -> cookies on the left -> tavern-keeper at the bottom row. 

## Running the Script

To run the export tool:
```bash
python tk-export.py
```

## Dependencies

This script requires:
- Python 3
- requests
- python-dotenv

The `json` module is purely to pretty print the data.
If you don't want to install python-json, simply change the single line:
`json.dump(data, f, indent=2)`
to
`f.write(data)`

The `dotenv` module loads the user id and cookie from a .env file.
If you don't want to use python-dotenv remove the lines
`import dotenv`
`dotenv.load_dotenv()`
and ensure that `TK_USER_ID` and `TK_COOKIE` are set in your environment.

I don't have an opinion on how you install these modules, package manager, pip,
pip-env, pipx, ..., use whatever you like.

I am not going to explain how to get your user id and cookie, it varies by
browser and the web is full of helpful advice and the 'Shutting Down' thread
had instructions. :)

## License

This project is licensed under the terms of the MIT license.
You are free to use it as you wish.
