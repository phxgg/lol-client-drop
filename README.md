# lol-client-drop #

*Under construction*

This is referring to people who know what they're doing.
I won't bother explaining every single step you have to take to make this script work.

# What this is

So what this script actually does is spam invites to an account with multiple clients of yours.<br>
The result is making the victim's client completely unresponsive.<br>
This shit will literally not stop until you cancel the attack.

# Run multiple clients

* <b>Windows:</b>
    * Run League of Legends with this argument: `--allow-multiple-clients`

* <b>macOS:</b>
    * Run `runleague.app` (see `bins` folder).

### What is `runleague.app`
The `runleague.app` is a simple AppleScript application used to send the `--allow-multiple-clients` argument
to the client executable. You can compile your own using the following code:
```
do shell script "open -a /Applications/League\\ of\\ Legends.app --args --allow-multiple-clients"
```
<b>Save it as an application</b>

### Older verions of macOS

For older versions of macOS, you might need to use this code instead:
```
do shell script "/Applications/League\\ of\\ Legends.app/Contents/LoL/LeagueClient.app/Contents/MacOS/LeagueClient --allow-multiple-clients & killall runleague.app"
```
Where `runleague.app` is whatever you have named the script + .app

<b><u>Please note:</u></b> For macOS users, you must open whatever number of clients you want <b>before</b> logging in to any account.
When you login to any account you won't be able to start a new client.

# Installation & Usage

### Setup

1. Create accounts on the same region as your victim (3 accounts should be quite powerful).
2. Skip the tutorial on each one of your accounts, so when you login you can see the client home page.
3. Install requirements with `pip install -r requirements.txt`

### Usage

* Run `python MAINFILE.py "Summoner Name" "Region"`<br>
Where `MAINFILE.py` is the main python file depending on your platform. For windows you should use `main_win.py`, and for macOS `main_mac.py`.

For example: `python main_mac.py "Kwsfour" "eune"`

<b>Available regions:</b> `eune`, `euw`, `na`

### How to get app port & auth token

* <b>Windows:</b>
    1. Place `SimpleDebugger.exe` inside your League of Legends folder (where `LeagueClient.exe` is located).
    2. Start SimpleDebugger and press `enter` to hook the client, then exit.
    * Now each time you start your League Client, the SimpleDebugger process will pop up and show you useful info.

* <b>macOS:</b>
    * App port & auth token are now automatically in the script (using: `ps -A | grep LeagueClientUx`)

# ToDo:

* Re-work the script using an LCU driver so we don't have to manually grab the app port & auth token for each account.<br>
A nice project that could be used is this one https://github.com/sousa-andre/lcu-driver but for the 5 minutes I checked,
it does not support multiple clients. I can work this around and add support for multiple clients but too bored right now lol.

# Disclaimer

This is made public for education purposes only. You are solely responsible for all activities that occur by using this script.