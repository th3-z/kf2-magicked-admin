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

I'll put builds here once I've got master ready for releases. I currently
have no access to a Windows machine, assistance is needed here.

Users looking for the most recent stable version should visit the releases page
on GitHub for now, you want 
[0.0.7](https://github.com/th3-z/kf-magicked-admin/releases/tag/0.0.7). The 
Documentation on this page isn't valid for 0.0.7, so please visit the 
[Steam guide](http://steamcommunity.com/sharedfiles/filedetails/?id=1324364024) 
for more information about 0.0.7.

Running from Python sources
---------------------------

### Requirements
Examples work on Debian 9 and Ubuntu 18.04, may differ for other operating 
systems. Install the following packages.

* Python 3.x - `apt install python3`
* Pip - `apt install python3-pip`
* Python 3 dependencies - `pip3 install -r requirements.txt`

### Running 
`git clone https://th3-z.xyz/git/kf2-magicked-admin.git`  
`cd kf2-magicked-admin`  
`python3 -O magicked_admin/magicked_admin.py`  

Building
--------

You can build a binary release with `make` after installing both the run and 
build requirements.

### Requirements
Examples work on Debian 9 and Ubuntu 18.04, may differ for other operating 
systems.

* Python 3.x - `apt install python3`
* Pip - `apt install python3-pip`
* Python 3 dependencies - `pip3 install -r requirements.txt`
* Make - `apt install make`

### Reccomended
Development make targets also use the following dependencies.

* isort - `apt install isort`
* flake8 - `apt install flake8`

Usage
-----

This usage documentation is from the old version (0.0.7). Although 
functionally the program is mostly unchanged, many of these will not work 
right in master. This is a complete list of the features that need testing.

### Player commands
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

### Admin commands
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
* !say _mesg_ - display _mesg_ in the chat, generally for use in conjuction 
with other commands
    - Example: !say This is an example.
* !silent - toggles output in chat
* !restart - immediately restarts the current map
* !load\_map _map-name_ - immediately loads _map-name_
* !toggle\_pass - toggles the configured game password (specified in 
`magicked_admin.conf`)
* !game_mode {endless|survival|weekly|versus} - changes the current GameType
    - Example: !game_mode endless

### Other features
* Writing a `server_name.motd` file with pairs of `%PLR` and `%SCR` and 
enabling the motd_scoreboard option will put a live scoreboard in the motd. 
    - `%SRV_D` and `%SRV_K` will be replaced by the total dosh and kills on 
    the server respectively.
* Writting a `server_name.init` with a list of commands will run the commands 
when the bot starts on server_name.

Configuration
---------------------

There is a config file, `magicked_admin.conf`, that is created after the first
run, you can change the settings with this file. I haven't documentation the 
options here, so you'll just have to figure it out.

