<p align="center">
    <img width=103 height=102 src="https://files.th3-z.xyz/standing/kf2ma.png"/>
</p>

<h1 align="center">Killing Floor 2 Magicked Admin</h1>

[![Downloads](https://img.shields.io/github/downloads/th3-z/kf2-magicked-admin/total.svg)](https://img.shields.io/github/downloads/th3-z/kf2-magicked-admin/total.svg) [![Build Status](https://travis-ci.com/th3-z/kf2-magicked-admin.svg?branch=master)](https://travis-ci.com/th3-z/kf2-magicked-admin) [![Coverage Status](https://coveralls.io/repos/github/th3-z/kf2-magicked-admin/badge.svg?branch=master)](https://coveralls.io/github/th3-z/kf2-magicked-admin?branch=master)

Scripted management, statistics, and bot for ranked Killing Floor 2 servers. 
Provides in-game commands, player stat tracking and ranking, live MOTD 
scoreboard and stats, greeter, and admin functions. Running entirely through 
the web admin, it does not affect a server's ranked/custom status. It can be 
ran either directly on the server or remotely, and manage multiple servers at 
once.

Downloads
---------

The most recent stable version is `0.1.3`. Binaries are provided on the releases 
page for Windows users. Linux and Mac OS users should clone the repo and run
from source.



[Release 0.1.3](https://github.com/th3-z/kf-magicked-admin/releases/tag/0.1.3)

<details>
<summary>Old releases</summary>

Release `0.0.7` has been extensively tested and aligns closer with the Steam guide.
* [Release 0.1.2](https://github.com/th3-z/kf-magicked-admin/releases/tag/0.1.2)
* [Release 0.0.7](https://github.com/th3-z/kf-magicked-admin/releases/tag/0.0.7)
</details>

Features
--------

### Commands

When inputting commands into the chat they need to be prefixed with `!`.
When writting commands into a script, or chaining them this should be 
omitted. 

Many commands will look for closest matches to their parameters. 
For example '_biotics_' will match '_kf-biotics-lab_' and '_userO_' will match
'_userOne™/@:®_'.

All commands have in-game help text that can be accessed with the `-h` flag.

* Example: `!commands -h`

All commands also have the following flags.

* `-q` - Suppresses output
* `-p` - Pads output to hide the username line

Escape sequences as follows are available to format messages.

* `\n` - Newline
    - Example: `!say line 0\nline 1`
* `\t` - Tab
    - Example: `!say line 0\n\tline 1 is indented`

#### Player commands

Commands that can be executed by any player.

<details>
<summary>Click to see the 18 player commands!</summary>
	
* `!commands` - Shows a list of all commands available to players
* `!stats <user>` - Shows general statistics about a user
    - Example: `!stats` Shows stats about yourself
    - Example: `!stats the_z` Shows stats about the_z
* `!kills <user>` - Shows kill statistics about a user
    - Example: `!stats` Shows kill stats about yourself
    - Example: `!stats the_z` Shows killstats about the_z
* `!dosh <user>` - Shows dosh statistics about a user
    - Example: `!stats` Shows dosh stats about yourself
    - Example: `!stats the_z` Shows dosh stats about the_z
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
* `!scoreboard` - Shows the complete player scoreboard, useful on servers with >6 max players
    - Alias: `!sb` Does the same
* `!game` - Shows information about the current game
* `!maps` - Shows the maplist
* `!player_count` - Shows the player count and max players
</details>

#### Admin commands

Commands that can be ran by server administrators or users authorized with 
the `!op` command.

<details>
<summary>Click to see the 24 admin commands!</summary>
	
* `!op <user>` - Gives a user administrative rights
    - Example: `!op the_z`
* `!deop <user>` - Revokes a user's administrative rights
    - Example: `!deop the_z`
* `!say <message>` - Echoes a message into chat
    - Example: `!say The quick brown fox jumps over the lazy dog`
    - Example: `!start_trc say The trader is open`
* `!players` - Shows detailed information about players on the server
* `!kick <user>` - Kicks `<user>` from the match
    - Example: `!kick the_z`
* `!ban <user>` - Bans `<user>` from the server
    - Example: `!ban the_z`
    - Warnng: The web admin currently has a bug that causes bans to persist
      after they are deleted, thus there is no unban command
* `!length <length>` - Change the length to `<length>` next game
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
* `!start_jc <command>` - Start a command that runs every time a player joins
	- Example: `!start_jc say Welcome %PLR%` - Greets a player on join
	- Available tokens: `%PLR` - username, `%KLL%` - total kills, `%DSH%` - 
      total dosh
* `!stop_jc` - Stops all join commands
* `!start_wc [-w <wave>] <command>` - Start a command that runs on wave `<wave>`
    - `-w` Wave to run the command on, can be omitted to have the command
    run every wave
    - `-w` Can be negative to count backwards from the boss wave
    - Example: `!start_wc -1 say Welcome to the boss wave`
* `!stop_wc` - Stops all wave commands
* `!start_tc [-r, -t <seconds>] <command>` - Start a command that runs after
    `<seconds>` seconds
    - Option `-r`: Add to have the command run repeatedly
    - Option `-t`: Required, the number of seconds before the command runs
    - Example: `!start_tc -rt 600 say Join our Steam group!\n
	http://steam.group/`
* `!stop_tc` - Stops all timed commands
* `!start_trc [-w <wave>] <command>` - Start a commands that runs when the trader opens
    - `-w` Wave to run the command on, can be omitted to have the command
        run every wave
    - `-w` Can be negative to count backwards from the boss wave
    - Example: `!start_trc top_wave_dosh` - Shows who earned the most dosh 
	every wave when the trader opens
* `!stop_trc` - Stop all commands that run on trader open
* `!silent` - Toggles suppression of all chat output, commands still have 
              effect, but the response will not be visible to players
* `!run <script_name>` - Executes a script from the `conf/scripts` folder, more
                         information in the scripts section
    - Example: `!run example`
* `!marquee <marquee_name>` - Runs a marquee in the chat from the
                              `conf/marquee` folder, _experimental_
    - Example: `!marquee example`
* `!enforce_dosh` - Kicks all players that have more dosh than the 
                 `dosh_threshold` configuration option
    - Example: `!start_tc 600 enforce_dosh`
</details>

### MOTD leaderboard

Writing a `conf/server_name.motd` file containing pairs of `%PLR` and `%SCR`
and enabling the `motd_scoreboard` option will put a live leaderboard in the
motd and update it every 5 minutes.

`%SRV_D` and `%SRV_K` will be replaced by the total dosh and kills on the 
server respectively.

The `scoreboard_type` configuration option allows you to change the score 
metric on the leaderboard. The options for this are: `dosh` or `kills`.

### Scripts

Writing a `server_name.init` in the `conf` folder with a series of commands
will run the commands in sequence when the bot starts on `server_name`.

Additional scripts can be written in the `conf/scripts` folder and ran with the
`!run` command. There is an example already in there that can be ran with 
`!run example`.

* Comments can be added to scripts by prefixing a line with `;`.

### Webadmin patches

For gamemodes other than survival to function in full patches have to be
applied to the `KFGame/Web/ServerAdmin` folder on the server. For this reason
a script is provided in the `admin-patches` folder that will automatically
patch your server.

There is currently no CLI or Windows build for this component. You can run it
with `python3 admin-patches/admin-patches.py`. A dialogue box will appear
asking you to locate your server.


Configuration options
---------------------

Basic setup is done on the first run. However this does not cover all of the 
options KF2-MA can offer. Please see the config file, `conf/magicked_admin.conf`, 
for more configuration options as some features are disabled by default.

Each server managed by KF2-MA has a section that looks something like 
`[server_one]`, followed by several options (`x = y`). Copy and edit the
default server section if you want to manage multiple servers. `[server_one]`
is the name of the server, this can be changed to whatever you want.

### Options

Options can be configured in the config file `conf/magicked_admin.conf`.

* `address`
    - Web address of the server's webadmin panel. Requires scheme and protocol,
    e.g. `https://0.0.0.0:8080`
* `username`
    - Webadmin username to login with, this will appear in the chat when the 
    bot has something to output. It's recommended to create a separate account
    for the bot.
* `password`
    - Webadmin password that matches the username above.
* `game_password`
    - Default game password to set when the password is toggled using 
    `!password <on|off>`.
* `motd_scoreboard`
    - Boolean value, enable or disable the MOTD scoreboard feature. Defaults to
    disabled.
* `scoreboard_type`
    - Possible values: `kills`, or `dosh`. Change the type of scores that are
    displayed in the MOTD scoreboard.
* `dosh_threshold`
    - Integer value, configures the `!enforce_dosh` command. The dosh threshold
    is the amount of dosh a player can carry before they are kicked by the next
    call to `!enforce_dosh`.
    
Running with Docker
---------------------------

Running with docker is easy. Just issue this command:
```
    docker run -it -p 1880:1880 --name kf2-magicked-admin -v '<host config folder location>':'/magicked_admin/conf' th3z/kf2-magicked-admin
```
You will need to change `<host config folder location>` to wheverever you want
to store your config folder. `/mnt/user/appdata/kf2-magicked-admin` is a popular
choice for systems running Unraid.

After this command runs the container will exit out and the logs will tell you
to setup the config file. Go to your `conf` folder and set things up then run 
the container again and you are good to go!

Running from Python sources
---------------------------

Before contributing code you will need to install the Python requirements.

### Requirements
Examples work on Debian 10 and Ubuntu 19.04, may differ for other operating 
systems. Install the following packages.

* Python 3.x - `apt install python3`
* Pip - `apt install python3-pip`
* Python 3 dependencies - `pip3 install -r requirements.txt`
    - This might complain about cx_freeze not installing if you haven't got 
    zlib, but cx_freeze is only needed for building.

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
Examples work on Debian 10 and Ubuntu Xenial, may differ for other operating 
systems.

* Python 3.x - `apt install python3`
* Pip - `apt install python3-pip`
* Pip dependencies - `pip3 install -r requirements.txt`
* Make - `apt install make`
* zlib-dev - `apt install zlib1g-dev`

### Windows users
You can build the program without make by running `setup.py`.

* `python3 setup.py build`

