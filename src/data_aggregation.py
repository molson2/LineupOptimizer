# -*- coding: utf-8 -*-
'''
Matt Olson
Collection of webscrapers to get weekly statistics from every player in the NFL
as well as FanDuel price data
'''

import requests
from bs4 import BeautifulSoup
import re


def get_fanduel_data(week):
    '''
    Get fan duel data from 'http://www.rotowire.com/daily/nfl/optimizer.htm'.
    Week indicated what week the data is for (will always be the current week!)
    '''

    BASE_URL = 'http://www.rotowire.com/daily/nfl/optimizer.htm'
    r = requests.get(BASE_URL)
    soup = BeautifulSoup(r.text, "html.parser")
    player_tags = soup.findAll(attrs={'class': 'playerSet'})
    players = []
    for player_tag in player_tags:
        opp = player_tag.findChild(
            attrs={'class': 'span3 lineupopt-opp'}).text
        salary = player_tag.findChild(
            attrs={'class': 'span3 lineupopt-salary'}).text
        salary = salary.replace(',', "").replace('$', '')
        player_tag.findChild(
            attrs={'class': 'span13 firstleft lineupopt-name'}).text
        name = player_tag.findChild(
            attrs={'class': 'span13 firstleft lineupopt-name'}).text

        name_s = name.split(u'\xa0')
        if len(name_s) > 1:
            name, injured = name_s
        else:
            name, injured = name_s[0], 'None'

        opp_s = opp.split('@')
        if len(opp_s) > 1:
            opp, loc = opp_s[1], 'away'
        else:
            opp, loc = opp_s[0], 'home'

        player_dict = {
            'pos': player_tag.findChild(
                attrs={'class': 'span3 lineupopt-position'}).text,
            'name': name,
            'injury': injured,
            'team': player_tag.findChild(
                attrs={'class': 'span3 lineupopt-team'}).text,
            'opp': opp,
            'location': loc,
            'spread': player_tag.findChild(
                attrs={'class': 'span3 lineupopt-spread'}).text,
            'ou': player_tag.findChild(
                attrs={'class': 'span3 lineupopt-ou'}).text,
            'ml': player_tag.findChild(
                attrs={'class': 'span3 lineupopt-ml'}).text,
            'pred_points': player_tag.findChild(
                attrs={'class': 'span3 lineupopt-points'}).text,
            'salary': salary,
            'week': week
        }
        players.append(player_dict)

    return players


def get_offensive_data(week, pos):
    '''
    Get player data for position 'pos' for week 'week' from
    http://www.cbssports.com/fantasy/football/stats/sortable/points/ and store
    in a list of dictionaries.  'pos' must be either 'QB', 'RB, 'WR', or 'TE'
    '''

    BASE_URL = 'http://www.cbssports.com/fantasy/football/stats/sortable/'
    BASE_URL += 'points/'
    pos_url = BASE_URL + ('/{}/standard/week-{}?&print_rows=9999'.
                          format(pos, str(week)))

    r = requests.get(pos_url)
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find('table', attrs={'class': 'data compact'})
    rows = table.findAll('tr', {'class': re.compile(r'row[1-9]')})
    rows = rows[1:]  # skip the header

    players = []
    for row in rows:
        tds = row.findAll('td')
        data = map(lambda x: x.text, tds)
        name, team = data[0].split(',')
        player_data = {
            'name': name,
            'team': team[1:],
            'pos': pos,
            'pass_att': data[1],
            'pass_cmp': data[2],
            'pass_yd': data[3],
            'pass_td': data[4],
            'pass_int': data[5],
            'pass_rating': data[6],
            'rush_att': data[7],
            'rush_yd': data[8],
            'rush_avg': data[9],
            'rush_td': data[10],
            'rec_target': data[11],
            'rec_reception': data[12],
            'rec_yd': data[13],
            'rec_avg': data[14],
            'rec_td': data[15],
            'fumble_lost': data[16],
            'week': week
        }
        players.append(player_data)

    return players


def get_kicker_data(week):
    '''
    Get kicker data for week 'week' from
    http://www.cbssports.com/fantasy/football/stats/sortable/points/ and store
    in a list of dictionaries
    '''

    BASE_URL = 'http://www.cbssports.com/fantasy/football/stats/sortable/'
    BASE_URL += 'points/'
    pos_url = BASE_URL + ('/K/standard/week-{}?&print_rows=9999'.
                          format(str(week)))
    r = requests.get(pos_url)
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find('table', attrs={'class': 'data compact'})
    rows = table.findAll('tr', {'class': re.compile(r'row[1-9]')})

    players = []
    for row in rows:
        tds = row.findAll('td')
        data = map(lambda x: x.text, tds)
        name, team = data[0].split(',')
        player_data = {
            'name': name,
            'team': team[1:],
            'fg': data[1],
            'fga': data[2],
            'fglg': data[3],
            'xp': data[4],
            'xpatt': data[5],
            'xpb': data[6],
            'week': week
        }
        players.append(player_data)

    return players


def get_dst_data(week):
    '''
    Get defense/special teams data for week 'week' from
    http://www.cbssports.com/fantasy/football/stats/sortable/points/ and store
    in a list of dictionaries
    '''
    BASE_URL = 'http://www.cbssports.com/fantasy/football/stats/sortable/'
    BASE_URL += 'points'

    pos_url = BASE_URL + ('/DST/standard/week-{}?&print_rows=9999'.
                          format(str(week)))
    r = requests.get(pos_url)
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find('table', attrs={'class': 'data compact'})
    rows = table.findAll('tr', {'class': re.compile(r'row[1-9]')})

    players = []
    for row in rows:
        tds = row.findAll('td')
        data = map(lambda x: x.text, tds)
        name, team = data[0].split(',')
        player_data = {
            'name': name,
            'team': team[1:],
            'int': data[1],
            'sty': data[2],
            'sacks': data[3],
            'tk': data[4],
            'dfr': data[5],
            'ff': data[6],
            'dtd': data[7],
            'pa': data[8],
            'paneta': data[9],
            'ruyda': data[10],
            'tyda': data[11],
            'week': week
        }
        players.append(player_data)

    return players


def get_matchup(week):
    '''
    Function to get team/team scores for week 'week'
    '''
    BASE_URL = 'http://www.cbssports.com/nfl/scoreboard/2015/week'
    url = BASE_URL + str(week)

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    matchups = soup.findAll('table', attrs={'class': 'lineScore postEvent'})
    reg = re.compile(r'[A-Z]+')

    games = []
    for matchup in matchups:
        away = matchup.find('tr', attrs={'class': 'teamInfo awayTeam'})
        home = matchup.find('tr', attrs={'class': 'teamInfo homeTeam'})
        game = {
            'home': reg.search(home.find('a')['href']).group(),
            'home_score': home.find('td', attrs={'class': 'finalScore'}).text,
            'away': reg.search(away.find('a')['href']).group(),
            'away_score': away.find('td', attrs={'class': 'finalScore'}).text,
            'week': week
            }
        games.append(game)

    return games


def main():
    pass
if __name__ == "__main__":
    pass
