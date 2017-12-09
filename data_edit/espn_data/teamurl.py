import pandas
from pandas import *
import collections
import numpy
import requests
from bs4 import BeautifulSoup
import csv
import urllib

url = 'http://espn.go.com/nba/teams'
r = urllib.request.urlopen(url)

soup = BeautifulSoup(r,'lxml')
tables = soup.find_all('ul', class_='medium-logos')

teams = []
pre_1 = []
pre_2 = []
teams_urls = []
for table in tables:
    lis = table.find_all('li')
    for li in lis:
        info = li.h5.a
        teams.append(info.text)
        url = info['href']
        teams_urls.append(url)
        pre_1.append(url.split('/')[-2])
        pre_2.append(url.split('/')[-1])


dic = {'url': teams_urls, 'prefix_2': pre_2, 'prefix_1': pre_1}
teams = pandas.DataFrame(dic, index=teams)
teams.index.name = 'team'
print(teams)
teams.to_csv('teamurl.csv')