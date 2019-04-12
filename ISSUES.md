KF2 Magicked Admin Issue Tracker
================================

Please use the template below when submitting new issues. The format is 
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

Greeter
-------
_status_:   Confirmed  
_category_: Feature  
_date_:     2019-04-12  
__desc__  
This feature is currently non-functional and disabled. They work on the 0.0.8 
branch if a working example is needed.    
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

The enable\_greeter config option not working
---------------------------------------------
_status_:   Unconfirmed  
_category_: Bug  
_date_:     2019-04-11  
__desc__  
enable\_greeter config option has no effect on wether the greeter is enabled 
or not.The greeter is enabled no matter what you put in the CONF file.  
__dev-notes__  

Commands !help and !kills not working
-------------------------------------
_status_:   Unconfirmed  
_category_: Bug  
_date_:     2019-04-11  
__desc__  
Tested the latest build today (Python 3.6.5, master branch). Unfortunately, 
`!help` would not respond at all.Also, `!kills` returned the following warning:

	VivaldiKF@test: !kills
	Exception in thread Thread-1:
	Traceback (most recent call last):
  		File "/usr/lib/python3.6/threading.py", line 916, in \_bootstrap\_inner
    		self.run()
  		File "kf-magicked-admin/magicked\_admin/server/chat/chat.py", line 73, in run
    		self.handle_message(username, message, admin)
  		File "kf-magicked-admin/magicked\_admin/server/chat/chat.py", line 93, in handle\_message
    		listener.receive_message(username, message, admin)
  		File "kf-magicked-admin/magicked\_admin/chatbot/chatbot.py", line 36, in receive\_message
    		self.command_handler(username, args, admin)
  		File "kf-magicked-admin/magicked\_admin/chatbot/chatbot.py", line 46, in command\_handler
    		response = command.execute(username, args, admin)
  		File "kf-magicked-admin/magicked\_admin/chatbot/commands/player\_commands.py", line 41, in execute
    		pos_kills = self.server.database.rank_kills(username)
  		File "kf-magicked-admin/magicked\_admin/database/database.py", line 44, in rank\_kills
    		return all_rows[0][-1] + 1
		IndexError: list index out of range  
__dev-notes__  

Set a default Additional URL variable
-------------------------------------
_status_:   Unconfirmed  
_category_: Feature  
_date_:     2019-04-11  
__desc__  
When using the restart command, URL variables are not usable. So for example 
!restart will not work with AccessPlus as the URL variable is not added.  
__dev-notes__  

Wrong player rank in !kills and !dosh
-------------------------------------
_status_:   Unconfirmed  
_category_: Bug  
_date_:     2019-04-11  
__desc__  
!kills and !dosh tells me im ranked second highest when im first on !top\_kills
and !top\_dosh  
__dev-notes__  

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
_status_:   Unconfirmed  
_category_: Feature  
_date_:     2019-04-11  
__desc__  
A log file of players that you can use to identify someone that has already 
left the game, you can do this with the KF2 server logs, but it's really 
messy. Should contain steam ID's, player names, and maybe some other stuff.  
__dev-notes__  

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

Greeter doesnt work on first player
-----------------------------------
_status_:   Confirmed  
_category_: Bug  
_date_:     2019-04-11  
__desc__  
There is no in-game chat with only 1 player present, so the greeting goes 
unnoticed. This could be delayed until another player joins or until the game 
starts.  
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

New commands, !sid
------------------
_status_:   Confirmed  
_category_: Feature  
_date_:     2019-04-11  
__desc__  
display player steam ids  
__dev-notes__  

New command, !time
------------------
_status_:   Confirmed  
_category_: Feature  
_date_:     2019-04-11  
__desc__  
command that displays the user's time logged in, session count, and rank by 
time spent.  
__dev-notes__  

Player rank up triggers
-----------------------
_status_:   Confirmed  
_category_: Feature  
_date_:     2019-04-11  
__desc__  
Easiest way to implement this is probably retrieving the top 100 or so 
dosh/kill scores on initialisation and comparing them to the online player's 
scores. Only respond to milestones such as: 100,50,25,15,10,5,4,3,2,1.  
__dev-notes__  
Not sure if the new prestige levels can be detected

Function, database.load\_player, creating unnecessary player records
--------------------------------------------------------------------
_status_:   Confirmed  
_category_: Bug  
_date_:     2019-04-11  
__desc__  
When a name is misspell in the stats command a new record is added for the 
misspell name in the players table.  
__dev-notes__  

Username collisions
-------------------
_status_:   Confirmed  
_category_: Bug  
_date_:     2019-04-11  
__desc__  
Should be using steam ID as primary key to avoid collisions. Can be read from 
the players page.  
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
This can be address by modification of the webadmin pages, still looking for
an easier solution

Unicode support
---------------
_status_:   Confirmed  
_category_: Bug  
_date_:     2019-04-11  
__desc__  
Players with pure Unicode names (e.g. Chinese players) of the same length will
collide because the characters are replaced with ?s.  
__dev-notes__

