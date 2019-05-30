#importing dependencies
import requests
import bs4
import io
import lxml

#getting html page of players from espn website
data = requests.get("http://www.espncricinfo.com/ci/content/player/index.html")
# print(data)

#convering the request data to beautiful-soup data type
data = bs4.BeautifulSoup(data.text, "html.parser")
# print(data)

total = data.select(".ciPlayersHomeCtryList")

#Getting teams name present on website
teams = []
for i in total:
    teams = i.find_all("a")
    print(teams)

import re
from collections import defaultdict
main_url = "http://www.espncricinfo.com/ci/content/player/caps.html?country="
player_url = "http://www.espncricinfo.com/ci/content/player/"
task2_url = "http://stats.espncricinfo.com/ci/engine/player/"
padd_url = "?class=2;template=results;type=allround;view=match"


#Scrapping data player data teamwise
cnt = len(teams)

with io.open("Runs_Cumulify_By_Year.csv", "w", encoding="utf8") as f1:
    f1.write("PLAYER NAME,NATIONALITY,RUNS MADE TILL THAT YEAR \n")
    f1.close()

for j in range(cnt):
    url = teams[j].get("href")
    url = re.split("=", url)
    url = main_url + url[1] + ";class=2"
    teamname = teams[j].text
    teamdata = requests.get(url)
    teamdata = bs4.BeautifulSoup(teamdata.text,"html.parser")
    playerdata = teamdata.select(".ciPlayerbycapstable")



    for k in playerdata:
        playerstats = k.find_all("li", class_="sep")
        for m in playerstats:
            number = m.find_all("li", class_="ciPlayerbycapstable")

            if(len(number)<1):
                number = m.find_all("li", class_="ciPlayerserialno")

                name = m.find_all("li", class_="ciPlayername")

                player = name[0]
                player = player.find_all("a")
                player = player[0].get("href")
                player = re.split("/", player)
                player = player[4]

    #Finding runs made by each player each year

                url2 = task2_url + player + padd
                player = requests.get(url2)
                player = bs4.BeautifulSoup(player.text, "html.parser")
                player = player.select(".pnl650M")
                player = player[0].find_all("table", class_="engineTable")
                player = player[3].find_all("tr", class_="data1")

                Dict = defaultdict(int)
                for l in player:
                    temp1 = l.find_all("td")
                    temp2 = temp1[12].text
                    temp2 = temp2[len(temp2)-4:len(temp2)+1]


                    run = temp1[0].text
                    if run[len(run)-1] is '*':
                        run = run[0:len(run)-1]

                    if run[0] is 'D' or run[0] is 'T' or run[0] is 'a' or run[0] is 's':
                        run = "0"

                    Dict[temp2] += int(run)

                dataline = name[0].text + "," + teamname + ","
                total_run = 0
                for l in Dict.items():
                    total_run += l[1]
                    dataline += str(total_run) + "(" + "till" + l[0] + ")" +","
                print(dataline)

                with io.open("Runs_Cumulify_By_Year.csv","a", encoding="utf8") as f1:
                    f1.write(dataline + "\n")
                    f1.close()


print("done")
