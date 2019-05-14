KF2 Magicked Admin Issue Tracker
================================

Please use the template below for recording new issues. The format is 
Markdown (CommonMark), 79 columns.

Template title
--------------
_status_:   Confirmed  
_category_: Feature  
_date_:     2019-04-11  
__desc__  
Detailed template description. Status options are as follows: 'Confirmed', 
'Unconfirmed', 'In-Progress'. Category options are as follows: 'Feature', 
'Bug'. Please use two or more spaces to add a line break after the description.  
__dev-notes__  
Example developer notes. Please delete issues after they are addressed.  

No endgame when switching to Endless
------------------------------------
_status_:   Confirmed  
_category_: Bug  
_date_:     2019-05-14  
__desc__  
The the game mode changes from Survival to Endless the end game event isn't
triggered. Only when not installed.   
__dev-notes__  
Caused by code to get around missing wave data in Endless's webadmin  

Greeter
-------
_status_:   Confirmed  
_category_: Bug  
_date_:     2019-05-14  
__desc__  
Recent regression causes the greeter not to run on player join.  
__dev-notes__  

Add top players rank by wave achieved
-------------------------------------
_status_:   Confirmed  
_category_: Feature  
_date_:     2019-04-11  
__desc__  
I'm not sure if this tool is still being maintained and updated. Would you 
consider adding a rank system sorted by highest wave number achieved by a 
player?  
__dev-notes__  
This is for the endless mode. Should probably record which map it was on too.  

Set a default Additional URL variable
-------------------------------------
_status_:   Confirmed  
_category_: Feature  
_date_:     2019-05-14  
__desc__  
When using the restart command, URL variables are not usable. So for example 
!restart will not work with AccessPlus as the URL variable is not added.  
__dev-notes__  
URL parameters config option  

Command, !toggle\_pass, is broken
---------------------------------
_status_:   Unconfirmed  
_category_: Bug  
_date_:     2019-04-11  
__desc__  
!toggle\_pass does not print to in-game chat and doesnt toggle game pass  
__dev-notes__  

Player log files
----------------
_status_:   Confirmed  
_category_: Feature  
_date_:     2019-05-14  
__desc__  
A log file of players that you can use to identify someone that has already 
left the game, you can do this with the KF2 server logs, but it's really 
messy. Should contain steam ID's, player names, and maybe some other stuff.  
__dev-notes__  
Add last login time to players table, and recently left players command  

Command to issue a command at a certain times and dates
-------------------------------------------------------
_status_:   Confirmed  
_category_: Feature  
_date_:     2019-04-11  
__desc__  
Implementing a command to issue a command at certain times and dates might 
make alerting people to:- Server restarts.- Server events.- Scheduling private
server times.- Server update information, for those that might have regularly 
scheduled update windows. Significantly easier and more efficient. Thanks to 
this idea goes out to Deliverance.  
__dev-notes__  

Wave number for !start\_trc
---------------------------
_status_:   Confirmed  
_category_: Feature  
_date_:     2019-04-11  
__desc__  
Optional wave number argument for `start_trc` to run commands when the trader 
opens on a specific wave.E.g. `!start_trc 2 say wave two trader is open`  
__dev-notes__

Perk thresholds
---------------
_status_:   Confirmed  
_category_: Feature  
_date_:     2019-04-11  
__desc__  
Get player level from info page when it is enabled. option to boot perks below
a certain level.  
__dev-notes__  
Not sure if the new prestige levels can be detected

Player rankings on existing commands
------------------------------------
_status_:   Confirmed  
_category_: Feature  
_date_:     2019-04-11  
__desc__  
Commands `kills` `dosh` `stats` should display the user's current rank  
__dev-notes__  
Kills and dosh have this now  

New command, !time
------------------
_status_:   Confirmed  
_category_: Feature  
_date_:     2019-04-11  
__desc__  
command that displays the user's time logged in, session count, and rank by 
time spent.  
__dev-notes__  
rank by time query, session counter, player time already implemented  

Player rank up triggers
-----------------------
_status_:   Confirmed  
_category_: Feature  
_date_:     2019-05-14  
__desc__  
Run command at player kill/dosh/time rank milestones such as: 100,50,25,15,
10,5,4,3,2,1  
__dev-notes__  

Function, database.load\_player, creating unnecessary player records
--------------------------------------------------------------------
_status_:   Unconfirmed  
_category_: Bug  
_date_:     2019-05-14  
__desc__  
When a name is misspell in the stats command a new record is added for the 
misspell name in the players table.
Not sure if this still occurs, used to be confirmed.  
__dev-notes__  

Doesn't work on weekly/endless servers
--------------------------------------
_status_:   Confirmed  
_category_: Feature  
_date_:     2019-04-11  
__desc__  
The info page parsing assumes the server is running survival mode. 
The info page is different on weekly servers.  
__dev-notes__  
Work in progress

