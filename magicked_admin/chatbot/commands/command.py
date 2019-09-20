from argparse import ArgumentError

from chatbot.commands.argument_parser import ArgumentParser
from utils import debug
from utils.text import pad_output
from web_admin.constants import *


class Command:
    def __init__(self, server, admin_only=True, requires_patch=False):
        self.server = server
        self.admin_only = admin_only
        self.requires_patch = requires_patch

        not_auth_message = "You're not authorised to use that command."
        self.not_auth_message = pad_output(not_auth_message)

        not_supported_message = "This action isn't supported without Killing" \
                                " Floor 2 Magicked Administrator's server" \
                                " side patch! Please review the documentation" \
                                " at 'th3-z.xyz/kf2ma' for guidance."
        self.not_supported_message = pad_output(not_supported_message)

        self.help_text = "The help text for this command hasn't been written!"
        self.currency_symbol = "$"
        # TODO: implement
        self.language = "en_GB.lang"

        self.parser = ArgumentParser(add_help=False)
        self.parser.add_argument(
            "-h", "--help",
            action="store_true"
        )
        self.parser.add_argument(
            "-p", "--pad",
            action="store_true"
        )

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

    def parse_args(self, username, args, user_flags):
        if not self.authorise(username, user_flags):
            return None, self.not_auth_message
        elif not self.supported():
            return None, self.not_supported_message

        try:
            args, _ = self.parser.parse_known_args(args[1:])
            error = None
        except ArgumentError as exc:
            if exc.argument:
                error = "{} Argument ({})".format(exc.message, exc.argument)
            else:
                error = exc.message
            debug("Argparse error in {}: {}".format(
                self.__class__.__name__, error
            ))
        except SystemExit:
            error = None
            debug("Argparse tried to exit!\n\tCommand: {}\n\tArgs: {}".format(
                args[0], args[1:]
            ))

        return args, error

    # TODO: Add *vars for str.format(message, *vars) and apply lang translation
    def format_response(self, message, args):
        message = message.replace("£", self.currency_symbol)
        if args.pad:
            return pad_output(message)
        else:
            return message

    def execute(self, username, args, user_flags):
        raise NotImplementedError("Command.execute() not implemented")
