import gettext
import argparse

from chatbot.commands.handlers import (
    OnJoinHandler, OnTimeHandler, OnTraderHandler, OnWaveHandler, OnDeathHandler
)
from chatbot.commands.command import Command
from chatbot.commands import ALL_WAVES
from utils import warning
from utils.text import trim_string

_ = gettext.gettext


class CommandOnTime(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)
        self.help_text = _("Usage: !start_tc [-r -t] COMMAND\n"
                           "\tCOMMAND - Command to run\n"
                           "\t-r --repeat - Optional, run repeatedly\n"
                           "\t-t --time - Seconds before running\n"
                           "Desc: Runs a command after some time delay")

        subparsers = self.parser.add_subparsers(dest="action")

        add_parser = subparsers.add_parser("add")
        add_parser.add_argument("--interval", "-n", type=int)
        add_parser.add_argument("--repeat", "-r", action="store_true")
        add_parser.add_argument("command", type=str, nargs=argparse.REMAINDER)
        
        subparsers.add_parser("show")
        
        del_parser = subparsers.add_parser("del")
        del_parser.add_argument("id", type=int)

        self.handlers = []

    def action_add(self, command, interval, repeat):
        handler = OnTimeHandler(self.server.event_manager, command, interval, repeat)
        self.handlers.append(handler)
        handler.start()
        return "Command started"

    def action_del(self, id):
        id -= 1
        if id >= 0 and id < len(self.handlers):
            self.handlers[id].close()
            del self.handlers[id]
            return "Command stopped"
        return "Invalid ID"

    def action_show(self):
        if not len(self.handlers):
            return "No commands running"

        message = ""
        for id, handler in enumerate(self.handlers):
            message += "{} - `{}` (n={}, r={})\n".format(id + 1, trim_string(handler.command, 20), handler.interval, int(handler.repeat))

        return message

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        if args.action == "add":
            return self.action_add(" ".join(args.command), args.interval or 10, args.repeat)

        elif args.action == "show":
            return self.action_show()
        
        elif args.action == "del":
            return self.action_del(args.id)

        return self.format_response(self.help_text, args)


class CommandOnJoin(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)
        self.help_text = _("Usage: !start_jc [--returning] COMMAND\n"
                           "\t-r --returning "
                           "- Set for only returning players\n"
                           "\tCOMMAND - Command to run\n"
                           "Desc: Runs a command when a player joins the "
                           "match")

        subparsers = self.parser.add_subparsers(dest="action")

        add_parser = subparsers.add_parser("add")
        add_parser.add_argument("--returning", "-r", action="store_true")
        add_parser.add_argument("command", type=str, nargs=argparse.REMAINDER)
        
        subparsers.add_parser("show")
        
        del_parser = subparsers.add_parser("del")
        del_parser.add_argument("id", type=int)

        self.handlers = []

    def action_add(self, command, returning):
        handler = OnJoinHandler(self.server.event_manager, command, returning)
        self.handlers.append(handler)
        return "Command started"

    def action_del(self, id):
        id -= 1
        if id >= 0 and id < len(self.handlers):
            self.handlers[id].close()
            del self.handlers[id]
            return "Command stopped"
        return "Invalid ID"

    def action_show(self):
        if not len(self.handlers):
            return "No commands running"

        message = ""
        for id, handler in enumerate(self.handlers):
            message += "{} - `{}` (r={})\n".format(id + 1, trim_string(handler.command, 20), int(handler.returning))

        return message

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        if args.action == "add":
            return self.action_add(" ".join(args.command), args.returning)

        elif args.action == "show":
            return self.action_show()
        
        elif args.action == "del":
            return self.action_del(args.id)

        return self.format_response(self.help_text, args)


class CommandOnWave(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=True)
        self.help_text = _("Usage: !start_wc [--wave] COMMAND\n"
                           "\t-w --wave - Optional, wave to run on\n"
                           "\tCOMMAND - Command to run\n"
                           "Desc: Run a command at the start of a wave, wave"
                           " can be omitted top run on every wave")

        subparsers = self.parser.add_subparsers(dest="action")

        add_parser = subparsers.add_parser("add")
        add_parser.add_argument("--wave", "-w", type=int)
        add_parser.add_argument("command", type=str, nargs=argparse.REMAINDER)
        
        subparsers.add_parser("show")
        
        del_parser = subparsers.add_parser("del")
        del_parser.add_argument("id", type=int)

        self.handlers = []

    def action_add(self, command, wave):
        handler = OnWaveHandler(self.server.event_manager, command, wave or ALL_WAVES)
        self.handlers.append(handler)
        return "Command started"

    def action_del(self, id):
        id -= 1
        if id >= 0 and id < len(self.handlers):
            self.handlers[id].close()
            del self.handlers[id]
            return "Command stopped"
        return "Invalid ID"

    def action_show(self):
        if not len(self.handlers):
            return "No commands running"

        message = ""
        for id, handler in enumerate(self.handlers):
            message += "{} - `{}` (w={})\n".format(id + 1, trim_string(handler.command, 20), int(handler.wave))

        return message

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        if args.action == "add":
            return self.action_add(" ".join(args.command), args.wave)

        elif args.action == "show":
            return self.action_show()
        
        elif args.action == "del":
            return self.action_del(args.id)

        return self.format_response(self.help_text, args)


class CommandOnTrader(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=True)
        self.help_text = _("Usage: !start_trc [--wave] COMMAND\n"
                           "\tCOMMAND - Command to run\n"
                           "\t-w --wave - Optional, wave to run on\n"
                           "Desc: Runs a command when the trader opens, wave"
                           " can be omitted to run every time the trader "
                           "opens")

        subparsers = self.parser.add_subparsers(dest="action")

        add_parser = subparsers.add_parser("add")
        add_parser.add_argument("--wave", "-w", type=int)
        add_parser.add_argument("command", type=str, nargs=argparse.REMAINDER)
        
        subparsers.add_parser("show")
        
        del_parser = subparsers.add_parser("del")
        del_parser.add_argument("id", type=int)

        self.handlers = []

    def action_add(self, command, wave):
        handler = OnTraderHandler(self.server.event_manager, command, wave or ALL_WAVES)
        self.handlers.append(handler)
        return "Command started"

    def action_del(self, id):
        id -= 1
        if id >= 0 and id < len(self.handlers):
            self.handlers[id].close()
            del self.handlers[id]
            return "Command stopped"
        return "Invalid ID"

    def action_show(self):
        if not len(self.handlers):
            return "No commands running"

        message = ""
        for id, handler in enumerate(self.handlers):
            message += "{} - `{}` (w={})\n".format(id + 1, trim_string(handler.command, 20), int(handler.wave))

        return message

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        if args.action == "add":
            return self.action_add(" ".join(args.command), args.wave)

        elif args.action == "show":
            return self.action_show()
        
        elif args.action == "del":
            return self.action_del(args.id)

        return self.format_response(self.help_text, args)


class CommandOnDeath(Command):
    def __init__(self, server):
        Command.__init__(self, server, admin_only=True, requires_patch=False)
        self.help_text = _("Usage: ")

        subparsers = self.parser.add_subparsers(dest="action")

        add_parser = subparsers.add_parser("add")
        add_parser.add_argument("command", type=str, nargs=argparse.REMAINDER)
        
        subparsers.add_parser("show")
        
        del_parser = subparsers.add_parser("del")
        del_parser.add_argument("id", type=int)

        self.handlers = []

    def action_add(self, command):
        handler = OnDeathHandler(self.server.event_manager, command)
        self.handlers.append(handler)
        return "Command started"

    def action_del(self, id):
        id -= 1
        if id >= 0 and id < len(self.handlers):
            self.handlers[id].close()
            del self.handlers[id]
            return "Command stopped"
        return "Invalid ID"

    def action_show(self):
        if not len(self.handlers):
            return "No commands running"

        message = ""
        for id, handler in enumerate(self.handlers):
            message += "{} - `{}`\n".format(id + 1, trim_string(handler.command, 20))

        return message

    def execute(self, username, args, user_flags):
        args, err = self.parse_args(username, args, user_flags)
        if err:
            return err
        if args.help:
            return self.format_response(self.help_text, args)

        if args.action == "add":
            return self.action_add(" ".join(args.command))

        elif args.action == "show":
            return self.action_show()
        
        elif args.action == "del":
            return self.action_del(args.id)

        return self.format_response(self.help_text, args)
