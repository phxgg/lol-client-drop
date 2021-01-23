import sys
import requests
from urllib3 import disable_warnings
import json
from time import sleep
from selenium import webdriver
from datetime import datetime
import subprocess
import psutil
#from lcu_driver import Connector
import threading
import base64

# TODO: use lcu_driver

# fill in with this format:
# 'app_port': 'auth_token',
auths = {}

# suppress warnings
#requests.packages.urllib3.disable_warnings() 
disable_warnings()

def leagueClientsAvailable():
    return 'LeagueClientUx' in (p.name() for p in psutil.process_iter())

'''def leagueClientAvailable1():
    result = subprocess.Popen(['ps -A | grep LeagueClientUx'], shell=True, stdout=subprocess.PIPE)
    readable = result.stdout.read().decode('utf-8')
    if not ('--remoting-auth-token' in readable):
        return False
    return True'''

def insertAuths():
    if not leagueClientsAvailable():
        print('No LeagueClient found. Login to an account and try again. Exiting...')
        sys.exit()

    result = subprocess.Popen(['ps -A | grep LeagueClientUx'], shell=True, stdout=subprocess.PIPE)
    lines = result.stdout.readlines()
    
    for line in lines:
        l = line.decode('utf-8')
        if '--remoting-auth-token' in l:
            remoting_auth_token = l.split('--remoting-auth-token=',1)[1].split(' ')[0]
            app_port = l.split('--app-port=',1)[1].split(' ')[0]
            auths[app_port] = remoting_auth_token

def spam(url, data, headers):
    # start flooding invitations
    while True:
        r = requests.post(url, data=data, headers=headers, verify=False)
        print('[' + datetime.now().strftime('%H:%M:%S') + '] Flooding...')
        print('[Response] ' + r.text)
        #sleep(0.01)

def main():
    # implement method to get app port & session token

    if len(sys.argv) < 3:
        print('Usage: python main.py "Summoner Name" "Region"')
        sys.exit()

    # get app port & auth token for each client
    insertAuths()

    summoner_name = sys.argv[1]
    region = sys.argv[2]

    if (not region == 'eune') and (not region == 'euw') and (not region == 'na'):
        print('Invalid region. Please use: eune / euw / na')
        sys.exit()

    gameServerRegion = 'EUN1'
    if region == 'euw':
        gameServerRegion = 'EUW1'
    elif region == 'na':
        gameServerRegion = 'NA1'

    print('Loading ChromeDriver...')

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--start-maximized') # works on Windows
    chrome_options.add_argument('--start-fullscreen') # works on Mac
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--mute-audio')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument('--log-level=3') # hide console warnings

    driver = webdriver.Chrome('chromedriver', options=chrome_options)

    opgg_link = 'https://' + region + '.op.gg/summoner/userName=' + summoner_name

    print('Grabbing Summoner Name & ID...')

    driver.get(opgg_link)

    sid_element = driver.find_element_by_xpath('//div[@class="GameListContainer"]')

    summoner_id = sid_element.get_attribute('data-summoner-id')
    summoner_name = driver.find_element_by_xpath('//span[@class="Name"]').text

    driver.quit()

    print('Summoner Name: ' + summoner_name)
    print('Summoner ID: ' + summoner_id)

    sleep(1)

    for app_port, auth_token in auths.items():
        api = 'https://127.0.0.1:' + app_port

        session_token = base64.b64encode(('riot:' + auth_token).encode('ascii')).decode('ascii')

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Basic ' + session_token
        }

        # actual script
        post_lobby_url = api + '/lol-lobby/v2/lobby'
        post_inv_url = api + '/lol-lobby/v2/lobby/invitations'

        # text to one line
        post_lobby_data = '{"customGameLobby": {"configuration": {"gameMode": "CLASSIC","gameServerRegion": "' + gameServerRegion + '","gameTypeConfig": {"advancedLearningQuests": true,"allowTrades": true,"banMode": "string","banTimerDuration": 0,"battleBoost": true,"crossTeamChampionPool": true,"deathMatch": true,"doNotRemove": true,"duplicatePick": true,"exclusivePick": true,"gameModeOverride": "string","id": 0,"learningQuests": true,"mainPickTimerDuration": 0,"maxAllowableBans": 0,"name": "string","numPlayersPerTeamOverride": 0,"onboardCoopBeginner": true,"pickMode": "string","postPickTimerDuration": 0,"reroll": true,"teamChampionPool": true},"mapId": 11,"maxPlayerCount": 0,"mutators": {"advancedLearningQuests": true,"allowTrades": true,"banMode": "string","banTimerDuration": 0,"battleBoost": true,"crossTeamChampionPool": true,"deathMatch": true,"doNotRemove": true,"duplicatePick": true,"exclusivePick": true,"gameModeOverride": "string","id": 0,"learningQuests": true,"mainPickTimerDuration": 0,"maxAllowableBans": 0,"name": "string","numPlayersPerTeamOverride": 0,"onboardCoopBeginner": true,"pickMode": "string","postPickTimerDuration": 0,"reroll": true,"teamChampionPool": true},"spectatorPolicy": "NotAllowed","teamSize": 0,"tournamentGameMode": "string","tournamentPassbackDataPacket": "string","tournamentPassbackUrl": "string"},"gameId": 0,"lobbyName": "string","lobbyPassword": "string","practiceGameRewardsDisabledReasons": ["string"],"spectators": [{"autoFillEligible": true,"autoFillProtectedForPromos": true,"autoFillProtectedForSoloing": true,"autoFillProtectedForStreaking": true,"botChampionId": 0,"botDifficulty": "NONE","canInviteOthers": true,"excludedPositionPreference": "string","id": 0,"isBot": true,"isOwner": true,"isSpectator": true,"positionPreferences": {"firstPreference": "string","secondPreference": "string"},"showPositionExcluder": true,"summonerInternalName": "string"}],"teamOne": [{"autoFillEligible": true,"autoFillProtectedForPromos": true,"autoFillProtectedForSoloing": true,"autoFillProtectedForStreaking": true,"botChampionId": 0,"botDifficulty": "NONE","canInviteOthers": true,"excludedPositionPreference": "string","id": 0,"isBot": true,"isOwner": true,"isSpectator": true,"positionPreferences": {"firstPreference": "string","secondPreference": "string"},"showPositionExcluder": true,"summonerInternalName": "string"}],"teamTwo": [{"autoFillEligible": true,"autoFillProtectedForPromos": true,"autoFillProtectedForSoloing": true,"autoFillProtectedForStreaking": true,"botChampionId": 0,"botDifficulty": "NONE","canInviteOthers": true,"excludedPositionPreference": "string","id": 0,"isBot": true,"isOwner": true,"isSpectator": true,"positionPreferences": {"firstPreference": "string","secondPreference": "string"},"showPositionExcluder": true,"summonerInternalName": "string"}]},"gameCustomization": {},"isCustom": false,"queueId": 830}'
        post_inv_data = '[{"invitationId": "", "state": "Requested", "timestamp": "", "toSummonerId": ' + summoner_id + ', "toSummonerName": "' + summoner_name + '"}]'

        # create lobby
        r = requests.post(post_lobby_url, data=post_lobby_data, headers=headers, verify=False)

        thr = threading.Thread(target=spam, args=(post_inv_url, post_inv_data, headers,))
        thr.daemon = True # make thread daemon so it kills when we exit script
        thr.start()

    # keep main thread alive
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        sys.exit()

#debugging
def findProcessIdByName(processName):
    '''
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    '''
    listOfProcessObjects = []
    #Iterate over the all the running process
    for proc in psutil.process_iter():
       try:
           pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
           # Check if process name contains the given name string.
           if processName.lower() in pinfo['name'].lower() :
               listOfProcessObjects.append(pinfo)
       except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
           pass
    return listOfProcessObjects

#debugging
def main1():
    print(leagueClientsAvailable())
    sys.exit()

if __name__ == '__main__':
    main()