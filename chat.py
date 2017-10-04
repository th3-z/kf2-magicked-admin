import threading
import time

class ChatLogger(threading.Thread):

    
    def __init__(self, server):
        self.server = server
        self.time_interval = 2
        self.message_log = []
        self.listeners = []

        threading.Thread.__init__(self)
    
    def run(self):

        while True:
            print("Fetching chat for " + self.server.name + ".")
            # Scrape self.server's chat and inform listeners of !sometext
            # Save all messages in self.message_log
            
            time.sleep(self.time_interval)

    def add_listener(self, listener):
        self.listeners.append(listener)

