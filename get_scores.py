from subprocess import call
import re, mmap
try:
    # Python 2.6-2.7 
    from HTMLParser import HTMLParser
except ImportError:
    # Python 3
    from html.parser import HTMLParser


print("Downloading score page...")
call(["wget", "-q", "-O", "./score_page.html", "http://www.gametracker.com/server_info/173.199.74.63:23000/top_players/"])


print("Parsing for score table...")

score_table = ""

table_ex = "(" + re.escape("<table class=\"table_lst table_lst_spn\">") + "(.|\n|\r)*" + re.escape("</table>") + ")" + "(.|\n|\r)*" + "<table>"

with open('score_page.html', 'r+') as score_page:
  data = mmap.mmap(score_page.fileno(), 0)
  mo = re.search(table_ex, data)
  if mo:
     score_table += mo.group(1)

csv = "rank,player,score,hours\n"

for player_row in " ".join(score_table.split()).split("<tr>")[2:-1]:
    player_row = player_row[1:-7] # drop trailing <tr> bits
    player_attrs = player_row[4:-5].split("</td> <td>")

    # Regex name out of <a> tag
    name_ex = "<a href=.*>(.*)<\/a>"
    mo = re.search(name_ex, player_attrs[1])
    h = HTMLParser()
    player_attrs[1] = h.unescape(mo.group(1))
    del player_attrs[2]
    
    for i in range(0,len(player_attrs)):
        player_attrs[i] = player_attrs[i].strip()
    
    csv += ",".join(player_attrs[:-1])+"\n" # Drop score per hour
    
scores_file = open("scores.csv","w")
scores_file.write(csv.encode('utf8'))
scores_file.close()

