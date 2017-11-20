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
* !start\_tc n command - repeat command every n seconds                                                                  Example: !start\_tc 5 say test
* !stop\_tc - stop all timed commands
* !start\_wc n command - run command when wave n is reached.                                                             Example: !start\_wc say Wave Started. - This posts a message at EVERY wave start.                                        Example: !start\_wc 4 say Wave 4 Started. - This posts a message when wave 4 starts.
* !stop\_wc - stop all wave commands
* !start\_trc command - run command every time the trader opens                                                          Example: !start\_trc say Traders open.
* !stop\_trc - stop trader commands
* !say mesg - display mesg, for use in conjuction with other admin commands                                              Example: !say This is an example.
* !silent - toggles output in chat
* !restart - immidiately restarts the current map
* !toggle\_pass - enables or disables the configured game password (the password you entered in your config)

### Other features
* Writing a server_name.motd file with pairs of %PLR and %SCR and enabling the motd_scoreboard option will put a live scoreboard             in the motd.
* Enabling the map_autochange option will change the map to a random one from official Killing floor 2 maps if the server gets stuck on the same map with 0 players for 4 hours.
* Writting a server_name.init with a list of commands will run the commands when the bot starts on server_name

## Dependancies/building
* Python 3.4+
* cx_freeze
* requests
* lxml
* configparser
* sqlite3

build by running the provided scripts `build.bat` or `build.sh` after installing dependancies via pip.

## Configuration
Before running you'll need to create a config file containing your server's webadmin credentials. This file has to be named `magicked_admin.conf` and placed next to the executable or `main.py`. An example file is provided inside `magicked_admin/config`.

## Running
Just run `pthon main.py` after installing the dependancies if you're using the source.
For windows binaries, open a command line in the install folder and run `magicked_admin`.
