
import wmi
import base64
import urllib3
import requests
import certifi
import ssl
import json

# myJson = """
# {
#   "participants":[
#      {
#         "activePlatform":"riot",
#         "cid":"543efae7-4c47-471a-b61a-2a27480c3259@champ-select.ru1.pvp.net",
#         "game_name":"NeWardyu",
#         "game_tag":"RU1",
#         "muted":false,
#         "name":"NeWardyu",
#         "pid":"fb86de5e-5e7b-5470-89e8-e1f1a67bf32c@ru1.pvp.net",
#         "puuid":"fb86de5e-5e7b-5470-89e8-e1f1a67bf32c",
#         "region":"ru1"
#      },
#      {
#         "activePlatform":"riot",
#         "cid":"543efae7-4c47-471a-b61a-2a27480c3259@champ-select.ru1.pvp.net",
#         "game_name":"YeePakK",
#         "game_tag":"RU1",
#         "muted":false,
#         "name":"YeePakK",
#         "pid":"dde43b5d-25e4-5428-ace5-5d49e6ad5f9c@ru1.pvp.net",
#         "puuid":"dde43b5d-25e4-5428-ace5-5d49e6ad5f9c",
#         "region":"ru1"
#      },
#      {
#         "activePlatform":"riot",
#         "cid":"543efae7-4c47-471a-b61a-2a27480c3259@champ-select.ru1.pvp.net",
#         "game_name":"СловаЗакончились",
#         "game_tag":"RU1",
#         "muted":false,
#         "name":"СловаЗакончились",
#         "pid":"b6c6daf3-538b-5f80-ad9f-48b4578b23e6@ru1.pvp.net",
#         "puuid":"b6c6daf3-538b-5f80-ad9f-48b4578b23e6",
#         "region":"ru1"
#      },
#      {
#         "activePlatform":"riot",
#         "cid":"543efae7-4c47-471a-b61a-2a27480c3259@champ-select.ru1.pvp.net",
#         "game_name":"Kiragane",
#         "game_tag":"RU1",
#         "muted":false,
#         "name":"Kiragane",
#         "pid":"ee0db595-2480-550e-ad59-e74145797175@ru1.pvp.net",
#         "puuid":"ee0db595-2480-550e-ad59-e74145797175",
#         "region":"ru1"
#      },
#      {
#         "activePlatform":"riot",
#         "cid":"543efae7-4c47-471a-b61a-2a27480c3259@champ-select.ru1.pvp.net",
#         "game_name":"Holy Swordsman",
#         "game_tag":"RU1",
#         "muted":false,
#         "name":"Holy Swordsman",
#         "pid":"82c4c25f-d4c8-5d56-bd0c-9fa7a1535f32@ru1.pvp.net",
#         "puuid":"82c4c25f-d4c8-5d56-bd0c-9fa7a1535f32",
#         "region":"ru1"
#      }
#   ]
# }
# """
# participants = json.loads(myJson)["participants"]
# participantNames = []
# print('Lobby participants:')
# for participant in participants:
#   participantName = participant["game_name"]
#   participantNames.append(participantName)
#   print(participantName)
# exit()

# Initializing the wmi constructor
f = wmi.WMI()
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager(
  cert_reqs='CERT_NONE',
  assert_hostname=False
)

class PortAndToken:
  def __init__(self, port, token):
    self.port = port
    self.token = token

def printLeagueClientProcessLaunchArgs(leagueClientProcessLaunchArgs: str):
  print('### Start of process launch args')
  print(leagueClientProcessLaunchArgs)
  print('### End of process launch args\n')

def extractArgValue(strToParse: str, argName: str):
  argName += '='
  # 1. Divide by arg and take the remaining string after the arg
  # 2. Divide by quote, and first quote must indicate an ending of our arg value.
  # Take the first part, which should be our arg's value.
  try :
    return strToParse.split(argName)[1].split('"')[0]
  except:
    print(f'Could not extract arg value "{argName}". Potentially not present.')
    return ''

# def convertTokenToRiotBasicAuthValue(token: str):
#   return base64.b64encode(('riot:' + token).encode('iso-8859-1')).decode('utf-8')

def makeParticipantsRequest(portAndToken: PortAndToken):
  if (portAndToken.port == '' or portAndToken.token == ''):
    raise Exception(f'Either port or token of PortAndToken object is missing. [port: "{portAndToken.port}", token: "{portAndToken.token}"]')
  url = 'https://127.0.0.1:' + portAndToken.port + '/chat/v5/participants/champ-select'
  # basic_auth = convertTokenToRiotBasicAuthValue(portAndToken.token)
  basic_auth = 'riot:' + portAndToken.token
  print(f'Will try to make request to url {url} with basic auth {basic_auth}')
  headers = urllib3.make_headers(basic_auth=basic_auth, accept_encoding='application/json', user_agent='LeagueOfLegendsClient')
  response = http.request('GET', url, headers=headers)
  response_data = response.data.decode('utf-8')
  print(f'Request to {url} was successful. Printing received data ...')
  print(response_data)
  print()
  return response_data

def tryPrintParticipants(portAndToken: PortAndToken, name: str):
  try:
    participantsJson = makeParticipantsRequest(portAndToken)
    participants = json.loads(participantsJson)["participants"]
    if len(participants) == 0:
      print('Participant list is empty. Supposedly the script was executed too early.')
      exit()
    participantNames = []
    print('Lobby participants:')
    for participant in participants:
      participantName = participant["name"]
      participantNames.append(participantName)
      print(participantName)
    print()
    # TODO: dynamic server selection?
    opggUrl = 'https://www.op.gg/multisearch/EUW?summoners=' + requests.utils.quote(','.join(participantNames))
    print('OP.GG link')
    print(opggUrl)
    exit()
  except Exception as e:
    print(f'Could not make request with {name} PortAndToken. {str(e)}')

leagueClientProcessName = 'leagueclientux.exe'
leagueClientProcessLaunchArgs = ''
# Iterating through all the running processes
for process in f.Win32_Process():
  if 'leagueclientux.exe' == process.Name.lower():
    leagueClientProcessLaunchArgs = process.CommandLine
if leagueClientProcessLaunchArgs == '':
  print(f'Failed to find process with lowercased name {leagueClientProcessName}')
  exit()

printLeagueClientProcessLaunchArgs(leagueClientProcessLaunchArgs)

riotPort = extractArgValue(leagueClientProcessLaunchArgs, '--riotclient-app-port')
riotToken = extractArgValue(leagueClientProcessLaunchArgs, '--riotclient-auth-token')
remotingPort = extractArgValue(leagueClientProcessLaunchArgs, '--riotclient-app-port')
remotingToken = extractArgValue(leagueClientProcessLaunchArgs, '--riotclient-auth-token')
Riot = PortAndToken(riotPort, riotToken)
Remoting = PortAndToken(remotingPort, remotingToken)

tryPrintParticipants(Riot, 'Riot')
tryPrintParticipants(Remoting, 'Remoting')
