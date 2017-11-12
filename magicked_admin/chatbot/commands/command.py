

class Command():
    
    def __init__(self, server, adminOnly = True):
        self.server = server
        self.adminOnly = adminOnly
        self.not_auth_message = "You're not authorised to use that command."

    def authorise(self, admin):
        if admin and self.adminOnly:
            return True
        elif self.adminOnly:
            return False
        else:
            return True
            
    def execute(self, username, args, admin):
        raise NotImplementedError("Command.execute() not implemented")

