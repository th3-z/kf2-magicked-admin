import threading
import math

class MotdUpdater(threading.Thread):

    def __init__(self, server):
        self.server = server

        self.time_interval = 8 * 60

        self.exit_flag = threading.Event()

        threading.Thread.__init__(self)
    
    def run(self):
        while not self.exit_flag.wait(self.time_interval):
            motd = self.render_motd()
            self.server.submit_motd(motd)
            

    def millify(self,n):
        millnames = ['','K','M','B','T']
        
        n = float(n)
        millidx = max(0,min(len(millnames)-1,
            int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

        return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])
        

    def render_motd(self):
        name_len = 13
        players = 9

        scores = self.server.database.top_kills()

        src_motd = self.server.motd

        for player in scores:
            name = player[0]
            name = (name[:name_len-2] + '..') if len(name) > name_len else name
            score = player[1]

            src_motd = src_motd.replace("%PLR", name, 1)
            src_motd = src_motd.replace("%SCR", self.millify(score), 1)
        
        return src_motd

    def terminate(self):
        self.exit_flag.set()
