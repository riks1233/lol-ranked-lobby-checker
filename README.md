# What is this

League of legends ranked lobby revealer / inspector. Running this program will try to communicate with league of legends client and if you are in a ranked lobby, it will gather information about all players and print an OP.GG link for the whole lobby. This let's you decide whether those people are worth your time grinding ranked games.

P.S. This is a scuffed ported solution of essential functionality, which was looked up from https://github.com/Riotphobia/LobbyReveal project. Ported in order to run an unbuilt and lightweight set of commands which does not launch a consistent `while` loop running in the background.

# How to run

- You need to have python3 installed (at least version 3.11).
- Create a python virtual environment in project root by running `python -m venv venv`.
- Activate the newly created venv (you should see `(venv)` prefix in your terminal)
  - Activation on Unix: `. venv/bin/activate`
  - Activation on Windows: `. venv/Scripts/activate`
- Install requirements into the launched venv from `requirements.txt` file by running `python -m pip install -r requirements.txt`
- Run the program when you have joined a ranked lobby with `python main.py`. **Make sure you are doing this with an activated venv.**

# Other notes

- `requirements.txt` was generated with the help of globally installed `pipreqs` package.
  - Ran `pipreqs --encoding=utf8 .` in the project root.
