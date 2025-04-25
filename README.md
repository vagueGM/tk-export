# tk-export

A crude python tool to export user data from
[Tavern-Keeper](https://www.tavern-keeper.com) before it shuts down.

The site author also offers an Elixir version, which includes a little less
data.
[https://github.com/bcentinaro/tk-export](https://github.com/bcentinaro/tk-export)

## Brief How to use

- Copy `.env.example` to `.env`.
- Add your user id number to the `TK_USER_ID=` line in `.env`.
- Add your cookie to the `TK_COOKIE=` line in `.env`.

$ `python tk-export.py`


## "Requirement"

This uses two common python modules. If you don't have- or don't want them, you
can edit the script to avoid them.

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
