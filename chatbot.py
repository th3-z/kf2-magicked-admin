from listener import Listener

class Chatbot(Listener):
    
    def __init__(self, server):
        self.server = server
        # The in-game chat can fit 21 Ws
        self.word_wrap = 21
        self.max_lines = 7

    def recieveMessage(self, username, message, admin):
        
        if message[0] == '!':
            # Drop the '!' because its no longer relevant
            args = message[1:].split(' ')
            self.command_handler(username, args, admin)
            

    def command_handler(self, username, args, admin):
        self.submitMessage("Recieved command from " + username + " : " + str(args) + \
            "\nAdmin: " + str(admin))
        if args[0] == "players":
            self.submitMessage(str(self.server.players))
        if args[0] == "game":
            self.submitMessage(str(self.server.game))
        

    def submitMessage(self, message):
        # note, \n works fine in chat
        # messages submitted here will not appear in ChatLogger
        chat_submit_url = "http://" + self.server.address + "/ServerAdmin/current/chat+frame+data"

        message_payload = {
            'ajax': '1',
            'message': message,
            'teamsay': '-1'
        }

        self.server.session.post(chat_submit_url, message_payload)
        
        
