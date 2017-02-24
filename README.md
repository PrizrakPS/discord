# Discord SourceQuery Bot #
Because sometimes telegram isn’t worth it.

## Information ##
### What is SourceQuery bot ###
It is a bot. A discord bot. A python discord bot. A python discord bot that queries Source and GoldSrc servers and notifies those who added several servers to their watchlists if those servers are currently down. Pretty simple. It is also capable of showing you detailed information such as:

* Hostname
* Current map
* VAC status
* Amount of players on server

And so on.

By the way, this thing is meant to be lightweight, so it only utilizes python tools and writes those watchlists to a json file that will be created once you run it for first time.

### Why? ###
There is a dude who made such a thing for Telegram. So I decided to make such a thing for discord.

## Usage ##
### Commands ###
It has just four commands:

* `/query <ip> <*port>` — manually queries the specified server at optional port and returns an embed-message with server information
* `/add <ip> <*port>` — add specified IP:port to your watchlist so bot will check those servers every 2 minutes and notify you with those IP:ports if one of them (or more) go down
* `/remove <ip> <*port>` — removes certain server from your watchlist
* `/check` — force run a check on your watchlist and get an embed with statuses in response

**Note 1:** I am a lazy faggot, so if you’re going to specify a port number, you have to use space instead of a colon: `/add 127.0.0.1 27015`, not `/add 127.0.0.1:27015`. Besides, if a server runs on 27015 port, you don’t have to specify it at all.  
**Note 2:** all these commands have shortcuts — just type their first letter to call them (i.e. `/c` instread if `/check`).

## Installation ##
### Requirements ###
**Hardware:** not a toster and a decent hard drive.  
**Software:** python 3.5.* with latest packages:

* discord.py
* tinydb

### Actually installing & running ###
Grab your python3.5 and pip, install discord.py & tinydb via pip, then download this repo (either `git clone` or just zip it).

Now go to [this page](https://discordapp.com/developers/applications/me/create), log in and create an application (application name is not bot’s name, but the image will be used as your bot’s avatar), then create a bot user & give it a name, save, click on „click to reveal“ near the „Token:“, copy the token.  
Navigate to the root folder of downloaded repo, open `bot.py` with any text editor and replace `paste_your_token_here` at the very bottom with your token. Save the file and close it.

Now, while you’re still here, execute `python3.5 bot.py` (might be called just python3 or just python, depending on your environment) and wait for `Logged in as <botname>` to appear.  
Last step: go back to the application page and copy the **Client ID**, then replace `CLIENT_ID_GOES_HERE` with the actual Client ID in this link: `https://discordapp.com/api/oauth2/authorize?client_id=CLIENT_ID_GOES_HERE&scope=bot&permissions=0`. Visit it and select the server you want your bot to join. Bam, done.