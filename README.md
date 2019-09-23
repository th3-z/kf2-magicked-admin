Killing Floor 2 Magicked Admin
==============================

Scripted management, statistics, and bot for ranked Killing Floor 2 servers. 
Provides in-game commands, player stat tracking and ranking, live MOTD 
scoreboard and stats, greeter, and admin functions. Running entirely through 
the web admin, it does not affect a server's ranked/custom status. It can be 
ran either directly on the server or remotely, and manage multiple servers at 
once.

Downloads
---------

The most recent stable version is 
[0.1.3](https://github.com/th3-z/kf-magicked-admin/releases/tag/0.1.3). 

Features
--------

### Commands

When inputting commands into the chat they need to be prefixed with `!`.
When writting commands into a script, or chaining them this should be 
omitted. 

Many commands will look for closest matches to their parameters. 
For example '_biotics_' will match '_kf-biotics-lab_' and '_userO_' will match
'_userOne™/@:®_'.

#### Player commands

Commands that can be executed by any user.

* `!commands` - Shows a list of all commands available to players
* `!stats <user>` - Shows general statistics about a user
    - Example: `!stats` Shows stats about yourself
    - Example: `!stats the_z` Shows stats about the_z
* `!kills` - Shows kill statistics about yourself
* `!dosh` - Shows dosh statistics about yourself
* `!map` - Shows statistics about the current map
* `!record_wave` - Shows the highest wave achieved on the current map
* `!top_kills` - Shows the global kills leaderboard
* `!top_dosh` - Shows the global dosh leaderboard
* `!top_time` - Shows the global play time leaderboard
* `!top_wave_kills` - Shows information about who killed the most ZEDs 
                      in the current wave. Generally for use with `start_trc`
    - Example: `!start_trc top_wave_kills`
* `!top_wave_dosh` - Shwows information about who earned the most dosh in 
                     the current wave. Generally for use with `!start_trc`
    - Example: `!start_trc top_wave_dosh`
* `!server_kills` - Shows total kills on the server
* `!server_dosh` - Shows total dosh earned on the server
* `!game` - Shows information about the current game
* `!maps` - Shows the maplist
* `!player_count` - Shows the player count and max players
			
#### Admin commands

Commands that can be ran by server administrators or users authorized with 
the `!op` command.

* `!op <user>` - Gives a user administrative rights
    - Example: `!op the_z`
* `!deop <user>` - Revokes a user's administrative rights
    - Example: `!deop the_z`
* `!say <message>` - Echoes a message into chat
    - Example: `!say The quick brown fox jumps over the lazy dog`
    - Example: `!start_trc say The trader is open`
* `!players` - 
* `!kick <user>` - 
    - Example: `!kick the_z`
* `!ban <user>` - 
    - Example: `!ban the_z`
    - Warnng: The web admin currently has a bug that causes bans to persist
      after they are deleted, thus there is no unban command
* `!length <length>` - Change the length to <length> next game
    - Example: `!length short`
* `!difficulty <difficulty>` - Change the difficulty to `<difficulty>` next 
                               game
    - Example: `!difficulty hell`
* `!game_mode <game_mode>` - Immediately change the game mode to `<game_mode>`
    - Example: `!game_mode endless` Changes the game mode to Endless
* `!load_map <map>` - Immediately change the map to `<map>`
    - Example: `!load_map biotics` Changes the map to Biotics Lab
* `!restart` - Immediately restart the current game
* `!password [--set] <on|off>`
    - Example: `!password on` Enables the game password defined in the config
    - Example: `!password off` Disables the game password
    - Example: `!password --set somePass` Sets a specific password
* `!start_jc <command>`
	- Example: ``
* `!stop_jc`
* `!start_wc <command>`
    - Example: ``
* `!stop_wc
* `!start_tc <command>`
    - Example: ``
* `!stop_tc
* `!start_trc <command>`
    - Example: ``
* `!stop_trc`
* `!silent`
* `!run`
    - Example: ``
* `!marquee`
    - Example: ``
* `!enforce_dosh`




### MOTD leaderboard

Writing a `server_name.motd` file containing pairs of `%PLR` and `%SCR` and 
enabling the `motd_scoreboard` option will put a live leaderboard in the motd 
and update it every 5 minutes. 

`%SRV_D` and `%SRV_K` will be replaced by the total dosh and kills on the 
server respectively.

The `scoreboard_type` configuration option allows you to change the score 
metric on the leaderboard. The options for this are: `dosh` or `kills`.

### Scripts

Writting a `server_name.init` in the root folder with a series of commands 
will run the commands in sequence when the bot starts on `server_name`.

Additional scripts can be written in the `scripts` folder and ran with the 
`!run` command. There is an example already in there that can be ran with 
`!run example`.

* Comments can be added to scripts by prefixing a line with `;`.


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

Options can be configured in the config file `magicked_admin.conf`.

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
    `!password <on|off>`.
* motd\_scoreboard
    - Boolean value, enable or disable the MOTD scoreboard feature. Defaults to
    disabled.
* scoreboard\_type
    - Possible values: `kills`, or `dosh`. Change the type of scores that are
    displayed in the MOTD scoreboard.
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

* `python3 setup.py build`

