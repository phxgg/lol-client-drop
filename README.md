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

* <b>MacOS:</b>
    * Use `open -n "run-league.app"` to start a new client (check `bin` folder).

The `run-league.app` is a simple AppleScript application used to send the `--allow-multiple-clients` argument
to the client executable. You can compile your own using the following code:
```
do shell script "/Applications/League\\ of\\ Legends.app/Contents/LoL/LeagueClient.app/Contents/MacOS/LeagueClient --allow-multiple-clients & killall League\\ of\\ Legends.app"
```

# Installation & Usage

1. Install requirements with `pip install -r requirements.txt`
2. You have to import your LeagueClient app port & auth token in `main.py` for each account you have logged into (see `auths` variable in `main.py`).

### How to get app port & auth token

* <b>Windows:</b>
    1. Place `SimpleDebugger.exe` inside your League of Legends folder (where `LeagueClient.exe` is located).
    2. Start SimpleDebugger and press `enter` to hook the client, then exit.
    * Now each time you start your League Client, the SimpleDebugger process will pop up and show you useful info.

* <b>MacOS:</b>
    * TODO: Create simple debugger for MacOS
    * For now, use `ps -A | grep LeagueClientUx` to get app port & auth token

# ToDo:

* Re-work the script using an LCU driver so we don't have to manually grab the app port & auth token for each account.<br>
A nice project that could be used is this one https://github.com/sousa-andre/lcu-driver but for the 5 minutes I checked,
it does not support multiple clients. I can work this around and add support for multiple clients but too bored right now lol.

# Disclaimer

This is made public for education purposes only. You are solely responsible for all activities that occur by using this script.