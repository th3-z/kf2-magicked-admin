# Breaks if someone puts a comma in their name

import csv
import math

name_len = 13
players = 9
millnames = ['','K',' M',' B',' T']

def millify(n):
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])

scores = []

print("Generating motd...")

with open("scores.csv", "a+") as f:
    for row in f:
        scores += [row.split(",")]
        
scores = scores[1:]

with open("src_motd.txt", "r") as fin:
    src_motd = fin.read()
    for i in range(0,players):
        name = scores[i][1]
        name = (name[:name_len-2] + '..') if len(name) > name_len else name
        
        score = scores[i][2]
        
        src_motd = src_motd.replace("%PLR", name, 1)
        src_motd = src_motd.replace("%SCR", millify(score), 1)
    
    motd = open("motd.txt","w")
    motd.write(src_motd)
    motd.close()
