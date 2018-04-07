class Command:
    def __init__(self, server, admin_only=True):
        self.server = server
        self.admin_only = admin_only
        self.not_auth_message = "You're not authorised to use that command."

    def authorise(self, admin):
        if admin and self.admin_only:
            return True
        elif self.admin_only:
            return False
        else:
            return True

    def execute(self, username, args, admin):
        raise NotImplementedError("Command.execute() not implemented")
