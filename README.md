# lol-client-drop #

*Under construction*

This is referring to people who know what they're doing.
I won't bother explaining every single step you have to take to make this script work.

## Run multiple clients

* <b>Windows:</b>
    * Run League of Legends with this argument: `--allow-multiple-clients`

* <b>MacOS:</b>
    * Use `open -n "run-league.app"` to start a new client (check `bin` folder).

The `run-league.app` is a simple AppleScript application used to send the `--allow-multiple-clients` argument
to the client executable. You can compile your own using the following code:
```
do shell script "/Applications/League\\ of\\ Legends.app/Contents/LoL/LeagueClient.app/Contents/MacOS/LeagueClient --allow-multiple-clients & killall League\\ of\\ Legends.app"
```

## Get app port & auth token

* <b>Windows:</b>
    * Place `SimpleDebugger.exe` inside your League of Legends folder (where `LeagueClient.exe` is located).
    * Start SimpleDebugger and press `enter` to hook the client, then exit.
    * Now each time you start your League Client, the SimpleDebugger process will pop up and show you useful info.

* <b>MacOS:</b>
    * TODO: Create simple debugger for MacOS
    * For now, use `ps -A | grep LeagueClientUx` to get app port & auth token