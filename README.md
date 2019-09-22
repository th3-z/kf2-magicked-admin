Killing Floor 2 Magicked Admin
==============================

Scripted management, statistics, and bot for ranked Killing Floor 2 servers. 
Provides in-game commands, player stat tracking and ranking, live MOTD 
scoreboard and stats, greeter, and admin functions. Running entirely through 
the web admin, it does not affect a server's ranked/custom status. It can be 
ran either directly on the server or remotely, and manage multiple servers at 
once.

Features
--------

TODO: This section is out of date

### Commands
* !me - display a summary of your stats
* !stats _player_ - display a summary of _player_'s stats
* !help - displays the help text in chat
* !info - displays information about this project
* !dosh - display the players recorded dosh and rank by dosh
* !top\_dosh - displays the players with the highest recorded dosh
* !kills - display the players recorded kills and rank by kills
* !top\_kills - displays the players with the most recorded kills
* !server\_kills - displays total number of zeds killed on the server
* !server\_dosh - displays total dosh earned on the server 

#### Operator commands
* !difficulty {normal|hard|suicidal|hell} - sets difficulty of next game
    - Example: !difficulty hard
* !length {short|medium|long} - sets length of next game
    - Example: !length medium
* !start\_tc _n command_ - repeat _command_ every _n_ seconds
    - Example: !start\_tc 5 say test
* !stop\_tc - stop all timed commands
* !start\_wc _n command_ - run _command_ when wave _n_ is reached.
    - Example: !start\_wc say Wave Started. - posts a message EVERY wave.
    - Example: !start\_wc 4 say Wave 4 Started. - This posts a message when 
    wave 4 starts.
* !stop\_wc - stop all wave commands
* !start\_trc _command_ - run _command_ every time the trader opens
    - Example: !start\_trc say Traders open.
* !stop\_trc - stop trader commands
* !say _mesg_ - display _mesg_ in the chat, generally for use in conjunction
with other commands
    - Example: !say This is an example.
* !silent - toggles output in chat
* !restart - immediately restarts the current map
* !load\_map _map-name_ - immediately loads _map-name_
* !toggle\_pass - toggles the configured game password (specified in 
`magicked_admin.conf`)
* !game_mode {endless|survival|weekly|versus} - changes the current GameType
    - Example: !game_mode endless

### MOTD leaderboard

TODO: Docs

### Greeter

TODO: Docs

### Init scripts

TODO: Docs

### Other
* Writing a `server_name.motd` file with pairs of `%PLR` and `%SCR` and 
enabling the motd_scoreboard option will put a live scoreboard in the motd. 
    - `%SRV_D` and `%SRV_K` will be replaced by the total dosh and kills on 
    the server respectively.
* Witting a `server_name.init` with a list of commands will run the commands
when the bot starts on server_name.

Downloads
---------

The most recent stable version is 
[0.1.3](https://github.com/th3-z/kf-magicked-admin/releases/tag/0.1.3). 

Configuration options
---------------------

Basic setup is done on the first run. However this does not cover all of the 
options KF2-MA can offer. Please see the config file, `magicked_admin.conf`, 
for more configuration options as some features are disabled by default.

Each server managed by KF2-MA has a section that looks something like 
`[server_one]`, followed by several options (`x = y`). Copy and edit the
default server section if you want to manage multiple servers. `[server_one]`
is the name of the server, this can be changed to whatever you want.

### Options
* address
    - Web address of the server's webadmin panel. Requires scheme and protocol,
    e.g. `https://0.0.0.0:8080`
* username
    - Webadmin username to login with, this will appear in the chat when the 
    bot has something to output. It's recommended to create a separate account
    for the bot.
* password
    - Webadmin password that matches the username above.
* game\_password
    - Default game password to set when the password is toggled using 
    `!password`.
* motd\_scoreboard
    - Boolean value, enable or disable the MOTD scoreboard feature. Defaults to
    disabled.
* scoreboard\_type
    - Possible values: `kills`, `dosh`. Change the type of scores that are
    displayed in the MOTD scoreboard.
* enable\_greeter
    - Boolean value, enable or disable the greeter that runs when a player 
    joins the match.
* dosh\_threshold
    - Integer value, configures the `!enforce_dosh` command. The dosh threshold
    is the amount of dosh a player can carry before they are kicked by the next
    call to `!enforce_dosh`.

Running from Python sources
---------------------------

Before contributing code you will need to install the Python requirements.

### Requirements
Examples work on Debian 10 and Ubuntu 19.04, may differ for other operating 
systems. Install the following packages.

* Python 3.x - `apt install python3`
* Pip - `apt install python3-pip`
* Python 3 dependencies - `pip3 install -r requirements.txt`
    - This might complain about cx\_freeze not installing if you haven't got 
    zlib, but cx\_freeze is only needed for building.

### Running 
`git clone git@github.com:th3-z/kf2-magicked-admin.git`

`cd kf2-magicked-admin`  

`pip3 install -r requirements.txt`

`python3 -O magicked_admin/magicked_admin.py`  

The `-O` flag runs the program in release mode, remove it to run KF2-MA in 
debug mode. Debug mode will enable more detailed output.

Building
--------

You can build a binary release for distribution with `make` after installing 
both the run and build requirements. 

### Requirements
Examples work on Debian 10 and Ubuntu 19.04, may differ for other operating 
systems.

* Python 3.x - `apt install python3`
* Pip - `apt install python3-pip`
* Python 3 dependencies - `pip3 install -r requirements.txt`
* Make - `apt install make`
* zlib-dev - `apt install zlib1g-dev`

### Recommended
Development make targets also use the following dependencies.

* isort - `apt install isort`
* flake8 - `apt install flake8`

### Windows users
You can build the program without make by running `setup.py`.

