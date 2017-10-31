# Killing Floor 2 Magicked Administrator
Automated management and statistics for ranked Killing Floor 2 servers.

### Finished features
* !help - displays the help text in chat
* !silent - toggles output in chat, administrator only command
* !diff {normal|hard|suicidal|hell} - sets difficulty of next game
* !length {short|medium|long} - sets length of next game
* !start\_tc n command - repeat command every n seconds, administrator only command
* !stop\_tc - stop all timed commands, administrator only command
* !players - displays currently logged in player stats for debugging
* !game - displays current game information for debugging

### Planned features
* !say mesg - display mesg, for use in conjunction with !start\_tc
* !kills - display the players recorded kills and rank by kills
* !dosh - display the players recorded dosh and rank by dosh
* !time - display the players time logged in and log in count
* Recording of dosh, time, kills over time
* Automatically switch map after inactivity to avoid server stalling on a broken one
* Count number of times each map is played as a metric of popularity, with automatic maplist section updating
* Attempt to detect out of date maps and delete them to force re-downloading

## Dependancies/installation
* Python 3.4+
* requests
* lxml
* configparser

Install Python then install the others using pip.

## Configuration
Before running you'll need to rename `config.example` to `config` and fill out your server information. Username will appear in chat, enabling multi-admin and creating an account for the bot is reccomended. Address should be of format ip:port where port is the port number for webadmin.

## Running
Just run `main.py` with python
```python main.py```
