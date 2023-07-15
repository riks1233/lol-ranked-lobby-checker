import urllib3
import requests
import json
import globals
import pythoncom
import wmi

from datetime import datetime


class PortAndToken:
    def __init__(self, port, token):
        self.port = port
        self.token = token


def log(msg=""):
    if msg == "":
        print()
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    print("[" + now + "]", msg)


def log_league_client_process_launch_args(league_client_process_launch_args: str):
    log(
        f"""
### Start of process launch args
{league_client_process_launch_args}
### End of process launch args\n
"""
    )


def extract_arg_value(str_to_parse: str, arg_name: str):
    arg_name += "="
    # 1. Divide by arg and take the remaining string after the arg
    # 2. Divide by quote, and first quote must indicate an ending of our arg value.
    # Take the first part, which should be our arg's value.
    try:
        return str_to_parse.split(arg_name)[1].split('"')[0]
    except:
        log(f'Could not extract arg value "{arg_name}". Potentially not present.')
        return ""


def make_participants_request(port_and_token: PortAndToken):
    if port_and_token.port == "" or port_and_token.token == "":
        raise Exception(
            f'Either port or token of PortAndToken object is missing. [port: "{port_and_token.port}", token: "{port_and_token.token}"]'
        )
    url = (
        "https://127.0.0.1:" + port_and_token.port + "/chat/v5/participants/champ-select"
    )
    basic_auth = "riot:" + port_and_token.token
    log(f"Will try to make request to url {url} with basic auth {basic_auth}")
    headers = urllib3.make_headers(
        basic_auth=basic_auth,
        accept_encoding="application/json",
        user_agent="LeagueOfLegendsClient",
    )
    response = globals.http.request("GET", url, headers=headers)
    response_data = response.data.decode("utf-8")
    # log(f"Request to {url} was successful. Printing received data ...")
    # log(response_data)
    # log()
    return response_data


def try_print_participants(port_and_token: PortAndToken, name: str):
    try:
        participants_json = make_participants_request(port_and_token)
        participants = json.loads(participants_json)["participants"]
        if len(participants) == 0:
            log(
                "Participant list is empty. Supposedly the script was executed too early."
            )
            return False
        participant_names = []
        log("Lobby participants:")
        for participant in participants:
            participant_name = participant["name"]
            participant_names.append(participant_name)
            log(participant_name)
        log()
        # TODO: dynamic server selection?
        opgg_url = "https://www.op.gg/multisearch/EUW?summoners=" + requests.utils.quote(
            ",".join(participant_names)
        )
        log("OP.GG link")
        log(opgg_url)
        return True
    except Exception as e:
        log(f"Could not make request with {name} PortAndToken. {str(e)}")
    return False


def run_check():
    pythoncom.CoInitialize()
    win_utils = wmi.WMI()
    league_client_process_name = "LeagueClientUx.exe"
    league_client_process_launch_args = ""
    # Iterating through all the running processes
    for process in win_utils.Win32_Process():
        if process.Name.lower() == league_client_process_name.lower():
            league_client_process_launch_args = process.CommandLine
    if league_client_process_launch_args == "":
        log(f"Failed to find process with name {league_client_process_name}")
        return

    # log_league_client_process_launch_args(league_client_process_launch_args)

    riot_port = extract_arg_value(
        league_client_process_launch_args, "--riotclient-app-port"
    )
    riot_token = extract_arg_value(
        league_client_process_launch_args, "--riotclient-auth-token"
    )
    riot = PortAndToken(riot_port, riot_token)

    try_print_participants(riot, "Riot")
