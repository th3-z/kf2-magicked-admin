import argparse
import sys


class ArgumentParser(argparse.ArgumentParser):
    def _get_action_from_name(self, name):
        if name is None:
            return None

        for action in self._actions:
            if '/'.join(action.option_strings) == name:
                return action
            elif action.metavar == name:
                return action
            elif action.dest == name:
                return action 

    def error(self, message):
        exc = sys.exc_info()[1]
        if exc:
            exc.argument = self._get_action_from_name(exc.argument_name)
            raise exc 
        else:
            raise argparse.ArgumentError(None, message)
