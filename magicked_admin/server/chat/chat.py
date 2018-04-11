import threading
import requests
import time
from lxml import html
from colorama import init
from termcolor import colored

# what the fuck does this do
init()


class ChatLogger(threading.Thread):
    def __init__(self, server):
        self.chat_request_url = "http://" + server.address + \
                                "/ServerAdmin/current/chat+data"
        self.chat_request_payload = {
            'ajax': '1'
        }

        self.server = server
        self.time_interval = 2
        self.message_log = []
        self.listeners = []

        self.poll_session = server.new_session()

        self.print_messages = True
        self.silent = False

        threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                response = self.poll_session.post(
                    self.chat_request_url,
                    self.chat_request_payload,
                    timeout=2
                )
            except requests.exceptions.RequestException as e:
                print("INFO: Couldn't retrieve chat (RequestException)")
                continue

            if response.text:
                # trailing new line ends up in list without the strip
                messages_html = response.text.strip().split("\r\n\r\n")

                for message_html in messages_html:
                    message_tree = html.fromstring(message_html)
                    try:
                        # xpath returns a list but theres only ever one of each because i split earlier
                        username = message_tree.xpath('//span[starts-with(@class,\'username\')]/text()')[0]
                        user_type = message_tree.xpath('//span[starts-with(@class,\'username\')]/@class')[0]
                        message = message_tree.xpath('//span[@class="message"]/text()')[0]
                        admin = True if "admin" in user_type else False

                        self.handle_message(username, message, admin)
                    except IndexError:
                        # Messages without usernames are not handled correctly. In particular, Controlled Difficulty
                        # This is basic support for Controlled Difficulty messages. It may need to be expanded to support
                        # other mutators and mods however.
                        username = "Controlled Difficulty"
                        admin = False
                        message = message_tree.xpath('//span[@class="message"]/text()')[0]
                        self.handle_message(username, message, admin)

            time.sleep(self.time_interval)

    def handle_message(self, username, message, admin):

        command = True if message[0] == '!' else False

        if self.print_messages and username != "server":
            print_line = username + "@" + self.server.name +  ": " + message
            
            if command:
                print_line = colored(print_line, 'green')
            elif username == "Controlled Difficulty":
                print_line = colored(print_line, 'cyan')
            else:
                print_line = colored(print_line, 'yellow')
            print(print_line)

        for listener in self.listeners:
            listener.receive_message(username, message, admin)

    def add_listener(self, listener):
        self.listeners.append(listener)

    def submit_message(self, message):
        if self.silent:
            return
        # note, \n works fine in chat
        # messages submitted here will not appear in ChatLogger
        chat_submit_url = "http://" + self.server.address + \
                          "/ServerAdmin/current/chat+frame+data"

        message_payload = {
            'ajax': '1',
            'message': message,
            'teamsay': '-1'
        }

        try:
            self.server.session.post(chat_submit_url, message_payload)
        except requests.exceptions.RequestException as e:
            print("INFO: Couldn't submit message (RequestException)")

