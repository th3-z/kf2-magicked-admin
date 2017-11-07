import threading
import time

class Watchdog(threading.Thread):

    def __init__(self, server):
        # 5 minutes
        self.time_interval = 5 * 60
        self.server = server

        self.last_map = ""

        self.exit_flag = threading.Event()

        threading.Thread.__init__(self)
        print("Started watchdog for " + server.name)

    def run(self):
        
        while not self.exit_flag.wait(self.time_interval):
            if self.last_map == self.server.game['map_title'] and len(self.server.players) < 1:
                print("INFO: Watchdog found a stuck map " + self.server.game['map_title']) 
                self.server.change_map("KF-Outpost")

            self.last_map = self.server.game['map_title']

    def terminate(self):
        self.exit_flag.set()

