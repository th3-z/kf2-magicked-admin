# Killing Floor 2 Magicked Administrator
Automated management and statistics for ranked Killing Floor 2 servers.

### Finished features
* !help - displays the help text in chat
* !silent - toggles output in chat, administrator only command
* !diff {normal|hard|suicidal|hell} - sets difficulty of next game
* !length {short|medium|long} - sets length of next game
* !start\_tc n command - repeat command every n seconds, administrator only command
* !stop\_tc - stop all timed commands, administrator only command

### Planned features
* Retrieve `score`, `map`, `players`, and `time` from Steam API rather than GT https://developer.valvesoftware.com/wiki/Server_queries
  * Score translates to current dosh, requires monitoring change frequently to get total over time.
* Count kills by scrapping the web admin
* Automatically switch map after inactivity to avoid server stalling on a broken one

* Chat bot with commands
  * !kills
  * !hrs
  * !dosh
  * !rank - Rank by dosh total
  * !rankk - Rank by kills
  * !rankt - Rank by play time
  * !votediff sui|hard|hoe
  * !votelength s|m|l
  * !commands

## Running (linux)
Add a line to your crontab that executes `run.sh` at the desired interval. 

```*/15 * * * * /home/the_z/bin/motd/run.sh >> /home/the_z/bin/motd/cron.log 2>&1```
