import sys
import requests
from urllib3 import disable_warnings
import json
from time import sleep
from selenium import webdriver
from datetime import datetime
import platform
import subprocess
import psutil
import threading
import base64

g_auths = {}
g_regions = {}

lcu_name = None

# suppress warnings
#requests.packages.urllib3.disable_warnings() 
disable_warnings()

def getLCUName():
    global lcu_name
    if platform.system() == 'Windows':
        lcu_name = 'LeagueClientUx.exe'
    elif platform.system() == 'Darwin':
        lcu_name = 'LeagueClientUx'
    elif platform.system() == 'Linux':
        lcu_name = 'LeagueClientUx'

def LCUAvailable():
    return lcu_name in (p.name() for p in psutil.process_iter())

def getLCUArguments():
    if not LCUAvailable():
        print('No ' + lcu_name + ' found. Login to an account and try again.')
        sys.exit()

    for p in psutil.process_iter():
        if p.name() == lcu_name:
            args = p.cmdline()

            remoting_auth_token = None
            app_port = None
            region = None
            for a in args:
                if '--region=' in a:
                    region = a.split('--region=', 1)[1].lower()
                if '--remoting-auth-token=' in a:
                    remoting_auth_token = a.split('--remoting-auth-token=', 1)[1]
                if '--app-port' in a:
                    app_port = a.split('--app-port=', 1)[1]
            
            g_auths[app_port] = remoting_auth_token
            g_regions[app_port] = region

def spam(url, data, headers):
    # start flooding invitations
    while True:
        r = requests.post(url, data=data.encode('utf-8'), headers=headers, verify=False)
        print('[' + datetime.now().strftime('%H:%M:%S') + '] Flooding...')
        print('[Response] ' + r.text)
        #sleep(0.01)

def main():
    # get LeagueClient name
    getLCUName()

    if len(sys.argv) < 3:
        print('Usage: python main.py "Summoner Name" "Region"')
        sys.exit()

    summoner_name = sys.argv[1]
    region = sys.argv[2]

    # get app port & auth token for each client
    getLCUArguments()

    # region validation
    if (not region == 'eune') and (not region == 'euw') and (not region == 'na'):
        print('Invalid region. Please use: eune / euw / na')
        sys.exit()

    gameServerRegion = 'EUN1'
    if region == 'euw':
        gameServerRegion = 'EUW1'
    elif region == 'na':
        gameServerRegion = 'NA1'

    # check if user has clients connected to given region
    flag = False
    for x, y in g_regions.items():
        if y == region:
            flag = True
            break

    if not flag:
        print('You are running 1 or more clients but there are no accounts connected on region: ' + region)
        sys.exit()

    # grab summoner info
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

    try:
        sid_element = driver.find_element_by_xpath('//div[@class="GameListContainer"]')
    except:
        print('Could not find summoner. Check summoner name and/or region.')
        sys.exit()


    summoner_id = sid_element.get_attribute('data-summoner-id')
    summoner_name = driver.find_element_by_xpath('//span[@class="Name"]').text
    summoner_name = summoner_name.encode('utf-8').decode('utf-8')

    driver.quit()

    print('Summoner Name: ' + summoner_name)
    print('Summoner ID: ' + summoner_id)

    sleep(1)
    
    for app_port, auth_token in g_auths.items():
        if g_regions[app_port] == region:
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

            # text to one line cuz why not
            post_lobby_data = '{"customGameLobby": {"configuration": {"gameMode": "CLASSIC","gameServerRegion": "' + gameServerRegion + '","gameTypeConfig": {"advancedLearningQuests": true,"allowTrades": true,"banMode": "string","banTimerDuration": 0,"battleBoost": true,"crossTeamChampionPool": true,"deathMatch": true,"doNotRemove": true,"duplicatePick": true,"exclusivePick": true,"gameModeOverride": "string","id": 0,"learningQuests": true,"mainPickTimerDuration": 0,"maxAllowableBans": 0,"name": "string","numPlayersPerTeamOverride": 0,"onboardCoopBeginner": true,"pickMode": "string","postPickTimerDuration": 0,"reroll": true,"teamChampionPool": true},"mapId": 11,"maxPlayerCount": 0,"mutators": {"advancedLearningQuests": true,"allowTrades": true,"banMode": "string","banTimerDuration": 0,"battleBoost": true,"crossTeamChampionPool": true,"deathMatch": true,"doNotRemove": true,"duplicatePick": true,"exclusivePick": true,"gameModeOverride": "string","id": 0,"learningQuests": true,"mainPickTimerDuration": 0,"maxAllowableBans": 0,"name": "string","numPlayersPerTeamOverride": 0,"onboardCoopBeginner": true,"pickMode": "string","postPickTimerDuration": 0,"reroll": true,"teamChampionPool": true},"spectatorPolicy": "NotAllowed","teamSize": 0,"tournamentGameMode": "string","tournamentPassbackDataPacket": "string","tournamentPassbackUrl": "string"},"gameId": 0,"lobbyName": "string","lobbyPassword": "string","practiceGameRewardsDisabledReasons": ["string"],"spectators": [{"autoFillEligible": true,"autoFillProtectedForPromos": true,"autoFillProtectedForSoloing": true,"autoFillProtectedForStreaking": true,"botChampionId": 0,"botDifficulty": "NONE","canInviteOthers": true,"excludedPositionPreference": "string","id": 0,"isBot": true,"isOwner": true,"isSpectator": true,"positionPreferences": {"firstPreference": "string","secondPreference": "string"},"showPositionExcluder": true,"summonerInternalName": "string"}],"teamOne": [{"autoFillEligible": true,"autoFillProtectedForPromos": true,"autoFillProtectedForSoloing": true,"autoFillProtectedForStreaking": true,"botChampionId": 0,"botDifficulty": "NONE","canInviteOthers": true,"excludedPositionPreference": "string","id": 0,"isBot": true,"isOwner": true,"isSpectator": true,"positionPreferences": {"firstPreference": "string","secondPreference": "string"},"showPositionExcluder": true,"summonerInternalName": "string"}],"teamTwo": [{"autoFillEligible": true,"autoFillProtectedForPromos": true,"autoFillProtectedForSoloing": true,"autoFillProtectedForStreaking": true,"botChampionId": 0,"botDifficulty": "NONE","canInviteOthers": true,"excludedPositionPreference": "string","id": 0,"isBot": true,"isOwner": true,"isSpectator": true,"positionPreferences": {"firstPreference": "string","secondPreference": "string"},"showPositionExcluder": true,"summonerInternalName": "string"}]},"gameCustomization": {},"isCustom": false,"queueId": 830}'
            post_inv_data = '[{"invitationId": "", "state": "Requested", "timestamp": "", "toSummonerId": ' + summoner_id + ', "toSummonerName": "' + summoner_name + '"}]'

            print(post_inv_data)

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

if __name__ == '__main__':
    main()