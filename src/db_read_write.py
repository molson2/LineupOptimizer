# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 21:22:11 2015

@author: matthewolson
"""

import sqlite3 as lite
from csv import DictReader

class DBError(Exception):
    pass

class FantasyDB(lite.Connection):
    '''
    Database connection class to handle DB read/write operations specific
    to this project.
    '''
    
    def __init__(self, db_name):
        '''
        Open connection
        '''
        lite.Connection.__init__(self, db_name)
        self.cur = self.cursor()
        self.is_open = True

    
    def write_table(self, players, tbl_name):
        '''
        Write player info to DB.  Note that players will be a list of
        dictionaries, whose keys must match the fields in the table located
        at tbl_name
        '''
        
        self.cur.execute('PRAGMA table_info({})'.format(tbl_name))
        data = self.cur.fetchall()
        fields = [x[1] for x in data]
            
        # check to make sure that fields in DB match up with keys
        if len(players) == 0:
            return
        else:
            if set(players[0].keys()) != set(fields):
                raise DBError('Keys do not match DB fields!')
            
        n_f = len(fields)
        query_string = 'insert into ' + tbl_name + ' values(' + '?,'*(n_f-1) + '?)'
        for player in players:
            vals = [player[x] for x in fields]
            self.cur.execute(query_string, vals)

    
    def read_table(self, tbl_name, week):
        """
         Read in data from a table as a list of dictionaries
        """
        
        # Get field names
        self.cur.execute('PRAGMA table_info({})'.format(tbl_name))
        data = self.cur.fetchall()
        fields = [x[1] for x in data]
        
        # Get rows matching criteria
        self.row_factory = lite.Row
        query = 'select * from ' + tbl_name + ' where week = ' + str(week)
        self.cur.execute(query)
        rows = self.cur.fetchall()
        
        # Convert tuples to dict
        players = []
        for row in rows:
            player = dict(zip(fields, row))
            players.append(player)
    
        return players
    
    def initialize_new_db(self):
        '''
        Function to initialize tables in a databse to hold fantasy football 
        data.  This function will only ever be used once in the lifetime of a
        database.
        '''
        
        # Check to see if there are tables, and promp user to continue
        query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY Name"
        self.cur.execute(query)
        if len(self.cur.fetchall()) != 0:
            warn_string = 'Non-empty database: Continue to create new tables? '
            warn_string += 'Y/N '
            response = raw_input(warn_string)
            if response.upper() != 'Y':
                return 0
        
        offensive = '''CREATE TABLE offensive(name TEXT,
                                              team TEXT,
                                              pos TEXT,
                                              pass_att REAL,
                                              pass_cmp REAL,
                                              pass_int REAL,
                                              pass_rating REAL,
                                              pass_td REAL,
                                              pass_yd REAL,
                                              rush_att REAL,
                                              rush_avg REAL,
                                              rush_yd REAL,
                                              rush_td REAL,
                                              rec_target REAL,
                                              rec_reception REAL,
                                              rec_yd REAL,
                                              rec_td REAL,
                                              rec_avg REAL,
                                              fumble_lost REAL,
                                              week REAL)'''
    
        dst = '''CREATE TABLE dst(name TEXT,
                                  team TEXT,
                                  int REAL, 
                                  sty REAL,
                                  sacks REAL,
                                  tk REAL,
                                  dfr REAL,
                                  ff REAL,
                                  dtd REAL,
                                  paneta REAL,
                                  ruyda REAL,
                                  tyda REAL,
                                  pa REAL,
                                  week REAL)
            '''
    
        k = '''CREATE TABLE kicker(name TEXT,
                                   team TEXT,
                                   fg REAL,
                                   fga REAL,
                                   fglg REAL,
                                   xp REAL,
                                   xpatt REAL,
                                   xpb REAL,
                                   week REAL)
            '''
    
#        fan_duel = '''CREATE TABLE fan_duel(name TEXT,
#                                            team TEXT,
#                                            pos TEXT,
#                                            opp TEXT,
#                                            location TEXT,
#                                            injury TEXT,
#                                            ml REAL,
#                                            ou REAL,
#                                            spread REAL,
#                                            salary REAL,
#                                            pred_points REAL,
#                                            week REAL)
#                  '''
#        matchups = ''' CREATE TABLE matchups(away TEXT,
#                                             away_score REAL,
#                                             home TEXT,
#                                             home_score REAL,
#                                             week REAL)
#                   '''
        offensive = offensive.replace('\n','')
        dst = dst.replace('\n', '')
        k = k.replace('\n', '')
#        fan_duel = fan_duel.replace('\n','')
#        matchups = matchups.replace('\n','')
                              
        self.cur.execute(offensive)
        self.cur.execute(dst)
        self.cur.execute(k)
#        self.cur.execute(fan_duel)
#        self.cur.execute(matchups)


def read_fanduel_data(fname):
    '''
    The "flatfile" version of FantasyDB.read_fan_duel. Entries in file must be 
    separated by '|' and have col names: name, team, pos, salary pred_points
    '''
    with open(fname, 'r') as f:
        field_names = f.readline().strip('\n').split('|')                                                                       
        raw_li = list(DictReader(f, delimiter='|', fieldnames=field_names))
    
    player_li = []
    for x in raw_li:
        player = {'name': x['name'], 
                  'pos': x['pos'],
                  'pred_points': float(x['pred_points']),
                  'salary': float(x['salary']), 
                  'team': x['team']}
        player_li.append(player)

    return player_li
        

def main():
    pass

if __name__ == "__main__":
    pass

