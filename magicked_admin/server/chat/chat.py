import threading
import requests
import time
from lxml import html
from termcolor import colored
from utils.logger import logger



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
            except requests.exceptions.RequestException:
                logger.debug("Couldn't retrieve chat (RequestException) ({})"
                             .format(self.server.name))
                time.sleep(self.time_interval + 3)
                continue

            if response.text:
                # trailing new line ends up in list without the strip
                messages_html = response.text.strip().split("\r\n\r\n")

                for message_html in messages_html:
                    message_tree = html.fromstring(message_html)
                    # xpath returns a list but theres only ever one of each because i split earlier
                    username_arr = message_tree.xpath('//span[starts-with(@class,\'username\')]/text()')
                    message = message_tree.xpath('//span[@class="message"]/text()')[0]
                    if len(username_arr) < 1:
                        logger.debug("Message without username '{}' ({})"
                                     .format(message, self.server.name))
                        continue
                    username = username_arr[0]

                    user_type_arr = message_tree.xpath('//span[starts-with(@class,\'username\')]/@class')
                    if len(user_type_arr) < 1:
                        logger.debug("Message without user type '{}' ({})"
                                     .format(message, self.server.name))
                        continue
                    user_type = user_type_arr[0]

                    admin = True if "admin" in user_type else False

                    self.handle_message(username, message, admin)

            time.sleep(self.time_interval)

    def handle_message(self, username, message, admin):

        command = True if message[0] == '!' else False

        if self.print_messages and username != "server":
            print_line = username + "@" + self.server.name +  ": " + message
            
            if command:
                print_line = colored(print_line, 'green')
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
        except requests.exceptions.RequestException:
            logger.debug("Couldn't submit message (RequestException)")
