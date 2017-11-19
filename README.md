# Killing Floor 2 Magicked Administrator
Scripted management, statistics, and bot for ranked Killing Floor 2 servers.

### Player commands
* !help - displays the help text in chat   Example:
* !dosh - display the players recorded dosh and rank by dosh
* !top\_dosh - displays the players with the highest recorded dosh
* !kills - display the players recorded kills and rank by kills
* !top\_kills - displays the players with the most recorded kills
* !difficulty {normal|hard|suicidal|hell} - sets difficulty of next game    Example: !difficulty hard
* !length {short|medium|long} - sets length of next game                    Example: !length medium

### Admin commands
* !start\_tc n command - repeat command every n seconds
Example: !start\_tc 5 say test
* !stop\_tc - stop all timed commands
* !start\_wc n command - run command when wave n is reached.
Example: !start\_wc say Wave Started. - This posts a message at EVERY wave start.
Example: !start\_wc 4 say Wave 4 Started. - This posts a message when wave 4 starts.
* !stop\_wc - stop all wave commands
* !start\_trc command - run command every time the trader opens
Example: !start\_trc say Traders open.
* !stop\_trc - stop trader commands
* !say mesg - display mesg, for use in conjuction with other admin commands
Example: !say This is an example.
* !silent - toggles output in chat
* !restart - immidiately restarts the current map
* !toggle\_pass - enables or disables the configured game password (the password you entered in your config)

### Other features
* Writing a server_name.motd file with pairs of %PLR and %SCR and enabling the motd_scoreboard option will put a live scoreboard             in the motd.
* Enabling the map_autochange option will change the map to a random one from official Killing floor 2 maps if the server gets stuck on the same map with 0 players for 4 hours.
* Writting a server_name.init with a list of commands will run the commands when the bot starts on server_name

### Planned features
* Player joined messages: Welcome back player Dave. Kills xxx, deaths xxx, logins xxx, ect.
* Player with top Kills and least health lost for current round displayed in chat at the end of each round.
* !next_map and !previous_map, to change map to previous or next map in the map cycle.
* Add server name to the print messages like "INFO: Player bon joined server Hard" and "INFO: Player bon quit from Hard".
* INFO: Submitting motd for "Server.name".
* Option in config to choose what interval you want Watchdog to be set at.
* %DSH and %KLS to represent Dosh and Kills in motd.
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
