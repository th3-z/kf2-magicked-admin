import threading
import time
import random

class Watchdog(threading.Thread):

    def __init__(self, server):
        # 5 minutes
        self.time_interval = 30 * 60
        self.server = server

        self.last_map = ""

        self.exit_flag = threading.Event()

        threading.Thread.__init__(self)
        print("Started watchdog for " + server.name)

    def run(self):
        
        while not self.exit_flag.wait(self.time_interval):
            if self.last_map == self.server.game['map_title'] and len(self.server.players) < 1:
                print("INFO: Watchdog found a stuck map " + self.server.game['map_title']) 
                self.server.change_map(randon.choice([
                    "KF-BioticsLab","KF-BlackForest","KF-BurningParis",
                    "KF-Catacombs","KF-ContainmentStation","KF-EvacuationPoint",
                    "KF-Farmhouse","KF-HostileGrounds","KF-InfernalRealm",
                    "KF-Nightmare","KF-Nuked","KF-Outpost",
                    "KF-Prison","KF-TragicKingdom","KF-TheDescent",
                    "KF-VolterManor","KF-ZedLanding" 
                ]))
                

            self.last_map = self.server.game['map_title']

    def terminate(self):
        self.exit_flag.set()

