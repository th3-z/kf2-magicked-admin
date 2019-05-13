from utils import debug
from web_admin.constants import *


class Command:

    def __init__(self, server, admin_only=True):
        self.server = server
        self.admin_only = admin_only
        self.not_auth_message = "You're not authorised to use that command."

    def authorise(self, username, user_flags):
        player = self.server.get_player_by_username(username)

        op = True if player and player.op else False
        internal = user_flags & USER_TYPE_INTERNAL
        admin = user_flags & USER_TYPE_ADMIN

        authorised = (not self.admin_only) or op or internal or admin

        if not authorised:
            debug("Auth failure, username: {}, user flags: {:b}".format(
                username, user_flags
            ))

        return authorised

    def execute(self, username, args, user_flags):
        raise NotImplementedError("Command.execute() not implemented")
