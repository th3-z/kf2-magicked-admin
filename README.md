# Killing Floor 2 Magicked Administrator
Scripted management, statistics, and bot for ranked Killing Floor 2 servers.

### Player commands
* !help - displays the help text in chat
* !dosh - display the players recorded dosh and rank by dosh
* !top_dosh - displays the players with the highest recorded dosh
* !kills - display the players recorded kills and rank by kills
* !top_kills - displays the players with the most recorded kills
* !diff {normal|hard|suicidal|hell} - sets difficulty of next game
* !length {short|medium|long} - sets length of next game

### Admin commands
* !start\_tc n command - repeat command every n seconds
* !stop\_tc - stop all timed commands
* !start\_wc n command - run command when wave n is reached, negative values will count back from the boss wave
* !stop\_wc - stop all commands on waves
* !start_trc command - run command every time the trader opens
* !stop_trc - stop running commands on trader open
* !say mesg - display mesg, for useful in conjuction with other admin commands
* !silent - toggles output in chat
* !restart - immidiately restarts the current map
* !toggle_pass - enables or disables the configured game password

### Other features
* Writing a server_name.motd file with pairs of %PLR and %SCR and enabling the motd_scoreboard option will put a live scoreboard in the motd.
* Enabling the map_autochange option will change the map to a random one from official Killing floor 2 maps if the server gets stuck on the same map with 0 players for 4 hours.

### Planned features
* !next_map and !previous_map, to change map to previous or next map in the map cycle.
* Add server name to the print messages like "INFO: Player bon joined server Hard" and "INFO: Player bon quit from Hard".
* INFO: Submitting motd for "Server.name".
* Option in config to choose what interval you want Watchdog to be set at.
* Option in config to choose what maps you want Watchdog to choose from.
* %DSH and %KLS to represent Dosh and Kills in motd.
* Using !stop_tc or !stop_trc or !stop_wc while there are 0 timed commands active will display "There aren't any tc's set.
* !time - display the players time logged in and log in count
* Count number of times each map is played as a metric of popularity, with automatic maplist section updating
* Attempt to detect out of date maps and delete them to force re-downloading

## Dependancies/installation
* Python 3.4+
* requests
* lxml
* configparser
* sqlite3

Install Python then install the others using pip.

## Configuration
Before running you'll need to rename `config.example` to `config` and fill out your server information. Username will appear in chat, enabling multi-admin and creating an account for the bot is reccomended. Address should be of format ip:port where port is the port number for webadmin. The game_password option is for the `!toggle_pass` command.

## Running
Just run `main.py` with python
```python main.py```
