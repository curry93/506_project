import urllib
from bs4 import BeautifulSoup
url = 'http://www.espn.com/nba/team/schedule/_/name/bos/year/2009/seasontype/2'

r = urllib.request.urlopen(url)
match_id = []
table = BeautifulSoup(r,'lxml').table
for row in table.find_all('tr')[1:]:
    columns = row.find_all('td')
    try:
        #print(columns[2].a['href'][-9:])
        print(columns[2].a['href'].split('/id/')[1])
    except:
        pass
    #print(columns[2])
    #for td in columns[2]:
        #try:
            #print(td.a['href'][-9:])
        #except:
            #pass