import gettext

_ = gettext.gettext

INIT_TEMPLATE = _('''
; The contents of this file will be ran in sequence on the server it is named
; after when the program starts. Lines starting with ; will be ignored. There
; is no need to prefix commands with ! in this file.
;
; Example:

; Globally suppress chat output
silent --quiet

; start_wc --wave -1 say If I wasn't commented you'd see this on the boss wave
start_trc top_wave_dosh

; Start the default greeter script `conf/scripts/greeter`
run greeter

; Update the motd scoreboard every 5 minutes
start_tc --repeat --time 300 update_motd

; Re-enable chat output
silent --quiet

''')
