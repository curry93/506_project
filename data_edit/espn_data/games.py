import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
import urllib
teams = pd.read_csv('teamurl.csv')
BASE_URL = 'http://espn.go.com/nba/team/schedule/_/name/{0}/year/{1}/seasontype/2'


log = open('errorlog.log','w')    
match_id = []
dates = []
home_team = []
home_team_score = []
visit_team = []
visit_team_score = []
for year in [2009,2010,2011]:
    for index, row in teams.iterrows():
        _team = row['prefix_1']
        print (year, _team)
        url = BASE_URL.format(_team, str(year))
        #r = urllib.request.urlopen(url)
        r = requests.get(url)
        table = BeautifulSoup(r.text,'lxml').table
        #table = BeautifulSoup(r,'lxml').find_all('table', class_ = 'mod-data')
          
        for row in table.find_all('tr')[1:]: # Remove header
            columns = row.find_all('td')
            try:
                _home = True if columns[1].li.text == 'vs' else False
                _other_team = columns[1].find_all('a')[1]['href'].split('/')[7]
                _score = columns[2].a.text.split(' ')[0].split('-')
                _won = True if columns[2].span.text == 'W' else False
                home_team.append(_team if _home else _other_team)
                visit_team.append(_team if not _home else _other_team)
                try:
                    d = datetime.strptime(columns[0].text, '%a, %b %d')
                    dates.append(date(year, d.month, d.day))
                except:
                    dates.append(date(year, 2, 29))
                if _home:
                    if _won:
                        home_team_score.append(_score[0])
                        visit_team_score.append(_score[1])
                    else:
                        home_team_score.append(_score[1])
                        visit_team_score.append(_score[0])
                else:
                    if _won:
                        home_team_score.append(_score[1])
                        visit_team_score.append(_score[0])
                    else:
                        home_team_score.append(_score[0])
                        visit_team_score.append(_score[1])
                try:
                    match_id.append(columns[2].a['href'][-9:])   #edit match_id
                except:
                    pass
            except Exception as e:
                print (log, e, columns)
                pass # Not all columns row are a match, is OK
            

log.close()  
print (len(match_id),len(dates),len(home_team),len(visit_team),len(home_team_score),len(visit_team_score) )     
dic = {'match_id': match_id, 'date': dates, 'home_team': home_team, 'visit_team': visit_team,
        'home_team_score': home_team_score, 'visit_team_score': visit_team_score}


games = pd.DataFrame(dic)
games.set_index('match_id')
games = games.drop_duplicates(subset='match_id').set_index('match_id')
#print(games)
games.to_csv('Games_2009_2011.csv')