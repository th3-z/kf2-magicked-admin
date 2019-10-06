import gettext

_ = gettext.gettext

INIT_TEMPLATE = _('''
; The contents of this file will be ran in sequence on the server it is named
; after when the program starts. Lines starting with ; will be ignored. There
; is no need to prefix commands with ! in this file.
;
; Example:
; silent
; start_wc -w 1 Welcome to wave 1
; silent
''')
