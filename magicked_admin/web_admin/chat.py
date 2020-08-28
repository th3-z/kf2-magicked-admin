import threading
import time
import sys

from colorama import init
from lxml import html
from termcolor import colored

from utils import DEBUG
from web_admin.constants import *

init()


class ChatListener(object):

    def receive_message(self, username, message, user_flags):
        raise NotImplementedError("Listener.receive_message() not implemented")


class Chat(threading.Thread):
    def __init__(self, web_interface):
        threading.Thread.__init__(self)

        self.__web_interface = web_interface
        self.__listeners = []
        self.__exit = False
        self.__refresh_rate = 3

        self.__silent = False

        self.__message_buffer = ""

    def run(self):
        while not self.__exit:
            self.__poll()
            time.sleep(self.__refresh_rate)

    def close(self):
        self.__exit = True

    def __poll(self):
        response = self.__web_interface.get_new_messages().text \
            + self.__message_buffer
        self.__message_buffer = ""

        if not response:
            return

        username_pattern = ".//span[starts-with(@class,\'username\')]/text()"
        user_type_pattern = ".//span[starts-with(@class,\'username\')]/@class"
        message_pattern = ".//span[@class=\'message\']/text()"

        message_roots = html.fromstring(response).find_class("chatmessage")

        for message_root in message_roots:
            username = message_root.xpath(username_pattern)[0]
            user_type = message_root.xpath(user_type_pattern)[0]
            message = message_root.xpath(message_pattern)[0]

            user_flags = USER_TYPE_NONE
            if 'admin' in user_type:
                user_flags += USER_TYPE_ADMIN
            if 'spectator' in user_type:
                user_flags += USER_TYPE_SPECTATOR

            self.handle_message(username, message, user_flags)

    def handle_message(self, username, message, user_flags):
        command = True if message[0] == '!' else False
        internal = user_flags & USER_TYPE_INTERNAL

        if DEBUG or not internal:
            print_line = username + "@" + self.__web_interface.server_name \
                + ": " + message.strip()
            if command:
                print_line = colored(
                    print_line.encode("utf-8").decode(sys.stdout.encoding),
                    'red' if internal else 'green'
                )
            else:
                print_line = colored(
                    print_line.encode("utf-8").decode(sys.stdout.encoding),
                    'red' if internal else 'yellow'
                )
            print(print_line.encode("utf-8").decode(sys.stdout.encoding))

        for listener in self.__listeners:
            listener.receive_message(username, message, user_flags)

    def add_listener(self, listener):
        self.__listeners.append(listener)

    def submit_message(self, message):
        if self.__silent:
            return

        message_payload = {
            'ajax': '1',
            'message': message.encode("iso-8859-1", "ignore"),
            'teamsay': '-1'
        }

        response = self.__web_interface.post_message(message_payload)
        self.__message_buffer += response.text

        return True
