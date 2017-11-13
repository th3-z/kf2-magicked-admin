import threading
import time

import requests
from lxml import html
from colorama import init
from termcolor import colored

init()

class ChatLogger(threading.Thread):

    def __init__(self, server):
        self.chat_request_url = "http://" + server.address + "/ServerAdmin/current/chat+data"
        self.chat_request_payload = {
            'ajax': '1'
        }
        
        self.server = server
        self.time_interval = 3
        self.message_log = []
        self.listeners = []
        
        self.poll_session = server.new_session()

        self.exit_flag = threading.Event()

        self.print_messages = True
        self.silent = False

        threading.Thread.__init__(self)
    
    def run(self):
        while not self.exit_flag.wait(self.time_interval):
            try:
                response = self.poll_session.post(
                    self.chat_request_url,
                    self.chat_request_payload,
                    timeout=2
                )
            except requests.exceptions.ConnectionError as e:
                print("INFO: Non-fatal connection error while refreshing chat, may have missed commands")
                continue
            except requests.exceptions.Timeout as e:
                print("WARNING: Connection timed out while refreshing chat, network may be down")
                continue
            
            if response.text:
                # trailing new line ends up in list without the strip
                messages_html = response.text.strip().split("\r\n\r\n")

                for message_html in messages_html:
                    message_tree = html.fromstring(message_html)
                    # xpath returns a list but theres only ever one of each because i split earlier
                    username = message_tree.xpath('//span[starts-with(@class,\'username\')]/text()')[0]
                    user_type = message_tree.xpath('//span[starts-with(@class,\'username\')]/@class')[0]
                    admin = True if "admin" in user_type else False
                    message = message_tree.xpath('//span[@class="message"]/text()')[0]
                    self.handle_message(username, message, admin)

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
            listener.recieveMessage(username, message, admin)

    def add_listener(self, listener):
        self.listeners.append(listener)

    def submit_message(self, message):
        if self.silent:
            return
        # note, \n works fine in chat
        # messages submitted here will not appear in ChatLogger
        chat_submit_url = "http://" + self.server.address + "/ServerAdmin/current/chat+frame+data"

        message_payload = {
            'ajax': '1',
            'message': message,
            'teamsay': '-1'
        }

        self.server.session.post(chat_submit_url, message_payload)

    def terminate(self):
        self.exit_flag.set()

