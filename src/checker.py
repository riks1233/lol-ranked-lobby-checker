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


def log_league_client_process_launch_args(leagueClientProcessLaunchArgs: str):
    log(
        f"""
### Start of process launch args
{leagueClientProcessLaunchArgs}
### End of process launch args\n
"""
    )


def extract_arg_value(strToParse: str, argName: str):
    argName += "="
    # 1. Divide by arg and take the remaining string after the arg
    # 2. Divide by quote, and first quote must indicate an ending of our arg value.
    # Take the first part, which should be our arg's value.
    try:
        return strToParse.split(argName)[1].split('"')[0]
    except:
        log(f'Could not extract arg value "{argName}". Potentially not present.')
        return ""


def makeParticipantsRequest(portAndToken: PortAndToken):
    if portAndToken.port == "" or portAndToken.token == "":
        raise Exception(
            f'Either port or token of PortAndToken object is missing. [port: "{portAndToken.port}", token: "{portAndToken.token}"]'
        )
    url = (
        "https://127.0.0.1:" + portAndToken.port + "/chat/v5/participants/champ-select"
    )
    # basic_auth = convertTokenToRiotBasicAuthValue(portAndToken.token)
    basic_auth = "riot:" + portAndToken.token
    log(f"Will try to make request to url {url} with basic auth {basic_auth}")
    headers = urllib3.make_headers(
        basic_auth=basic_auth,
        accept_encoding="application/json",
        user_agent="LeagueOfLegendsClient",
    )
    response = globals.http.request("GET", url, headers=headers)
    response_data = response.data.decode("utf-8")
    log(f"Request to {url} was successful. Printing received data ...")
    log(response_data)
    log()
    return response_data


def tryPrintParticipants(portAndToken: PortAndToken, name: str):
    try:
        participantsJson = makeParticipantsRequest(portAndToken)
        participants = json.loads(participantsJson)["participants"]
        if len(participants) == 0:
            log(
                "Participant list is empty. Supposedly the script was executed too early."
            )
            return False
        participantNames = []
        log("Lobby participants:")
        for participant in participants:
            participantName = participant["name"]
            participantNames.append(participantName)
            log(participantName)
        log()
        # TODO: dynamic server selection?
        opggUrl = "https://www.op.gg/multisearch/EUW?summoners=" + requests.utils.quote(
            ",".join(participantNames)
        )
        log("OP.GG link")
        log(opggUrl)
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
    remotingPort = extract_arg_value(
        league_client_process_launch_args, "--app-port"
    )
    remotingToken = extract_arg_value(
        league_client_process_launch_args, "--remoting-auth-token"
    )
    Riot = PortAndToken(riot_port, riot_token)
    Remoting = PortAndToken(remotingPort, remotingToken)

    printSuccessful = tryPrintParticipants(Riot, "Riot")
    if not printSuccessful:
        tryPrintParticipants(Remoting, "Remoting")
