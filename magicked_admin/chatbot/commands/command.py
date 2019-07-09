from utils import debug
from web_admin.constants import *
from utils.text import pad_output


class Command:
    def __init__(self, server, admin_only=True, requires_patch=False):
        self.server = server
        self.admin_only = admin_only
        self.requires_patch = requires_patch

        not_auth_message = "You're not authorised to use that command."
        self.not_auth_message = pad_output(not_auth_message)

        not_supported_message = "This action isn't supported without Killing"\
                                " Floor 2 Magicked Administrator's server"\
                                " side patch! Please review the documentation"\
                                " at 'th3-z.xyz/kf2ma' for guidance."
        self.not_supported_message = pad_output(not_supported_message)

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

    def supported(self):
        return (not self.requires_patch) or self.server.supported_mode()

    def execute_pretest(self, username, user_flags):
        if not self.authorise(username, user_flags):
            return self.not_auth_message
        if not self.supported():
            return self.not_supported_message
        return None
    
    def execute(self, username, args, user_flags):
        raise NotImplementedError("Command.execute() not implemented")

