# Killing Floor 2 Magicked Administrator
Scripted management, statistics, and bot for ranked Killing Floor 2 servers. Provides in-game commands, player stat tracking and ranking, live MOTD scoreboard and stats, greeter, and admin functions. Running entirely through the web administrator, it does not affect a server's ranked/custom status. It can be ran either directly on the server or remotely, and manage multiple servers at once.

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
* !start\_tc _n_ _command_ - repeat _command_ every _n_ seconds
    - Example: !start\_tc 5 say test
* !stop\_tc - stop all timed commands
* !start\_wc _n command_ - run _command_ when wave _n_ is reached.
    - Example: !start\_wc say Wave Started. - posts a message EVERY wave.
    - Example: !start\_wc 4 say Wave 4 Started. - This posts a message when wave 4 starts.
* !stop\_wc - stop all wave commands
* !start\_trc _command_ - run _command_ every time the trader opens
    - Example: !start\_trc say Traders open.
* !stop\_trc - stop trader commands
* !say _mesg_ - display _mesg_ in the chat, generally for use in conjuction with other commands
    - Example: !say This is an example.
* !silent - toggles output in chat
* !restart - immediately restarts the current map
* !load_map _map_name_ - immediately loads _map_name_
* !toggle\_pass - toggles the configured game password (specified in `magicked_admin.conf`)

### Other features
* Writing a `server_name.motd` file with pairs of `%PLR` and `%SCR` and enabling the motd_scoreboard option will put a live scoreboard in the motd. 
    - `%SRV_D` and `%SRV_K` will be replaced by the total dosh and kills on the server respectively.
* Writting a `server_name.init` with a list of commands will run the commands when the bot starts on server_name

## Dependancies/building
* Python 3.4+
* cx_freeze
* requests
* lxml
* colorama
* termcolor

build by running the provided scripts `build.bat` or `build.sh` after installing dependancies via pip.

## Minimal configuration
If running from source you will need to copy the example configs from the `config` folder to the root folder, the build scripts do this automatically.
After the cofiguration is present, edit these lines in `magicked_admin.conf` to match your server details:
```
address = 127.0.0.1:8080
username = Admin
password = 123
```
See the [Steam guide](http://steamcommunity.com/sharedfiles/filedetails/?id=1324364024) for more detailed usage information

## Running
Run `pthon main.py` if executing from source. If you're using a binary execute `magicked_admin.exe`.
