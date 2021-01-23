# lol-client-drop #

*Under construction*

This is referring to people who know what they're doing.
I won't bother explaining every single step you have to take to make this script work.

# What this is

So what this script actually does is spam invites to an account with multiple clients of yours.<br>
The result is making the victim's client completely unresponsive.<br>
This shit will literally not stop until you cancel the attack.

# Installation & Usage

### Setup

1. Install python 3.8 or later: https://www.python.org/
2. Install requirements with `pip install -r requirements.txt`
3. Summoner data is grabbed using Chrome, so download `chromedriver` and add it to your PATH: https://chromedriver.chromium.org/
4. Create accounts on the same region as your victim (3 accounts should be quite powerful).
5. Skip the tutorial on each one of your accounts, so when you login you can see the client home page.

### Usage

* Run `python main.py "Summoner Name" "Region"`<br>

For example: `python main.py "Kwsfour" "eune"`

<b>Available regions:</b> `eune`, `euw`, `na`

# Run multiple clients

* <b>Windows:</b>
    * Run League of Legends with this argument: `--allow-multiple-clients`

* <b>macOS:</b>
    * Run `runleague.app` (see `bin` folder).

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

# Disclaimer

This is made public for education purposes only. You are solely responsible for all activities that occur by using this script.