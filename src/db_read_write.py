# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 21:22:11 2015

@author: matthewolson
"""

import sqlite3 as lite


def init_db(db_name):
    '''
    Function to initialize tables in a databse to hold fantasy football data
    '''
    conn = lite.connect(db_name)
    cur = conn.cursor() 
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
                              week REAL)'''
    
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
    
    fan_duel = '''CREATE TABLE fan_duel(name TEXT,
                                        team TEXT,
                                        pos TEXT,
                                        opp TEXT,
                                        location TEXT,
                                        injury TEXT,
                                        ml REAL,
                                        ou REAL,
                                        spread REAL,
                                        salary REAL,
                                        pred_points REAL,
                                        week REAL)
    '''
    
    matchups = ''' CREATE TABLE matchups(away TEXT,
                                         away_score REAL,
                                         home TEXT,
                                         home_score REAL,
                                         week REAL)
    '''
    
    
    offensive = offensive.replace('\n','')
    dst = dst.replace('\n', '')
    k = k.replace('\n', '')
    fan_duel = fan_duel.replace('\n','')
    matchups = matchups.replace('\n','')
                              
    cur.execute(offensive)
    cur.execute(dst)
    cur.execute(k)
    cur.execute(fan_duel)
    cur.execute(matchups)
    conn.close()


def write_db(players, conn, tbl_name):
    
    with conn:
        cur = conn.cursor()
        cur.execute('PRAGMA table_info({})'.format(tbl_name))
        data = cur.fetchall()
        fields = [x[1] for x in data]
        n_f = len(fields)
        query_string = 'insert into ' + tbl_name + ' values(' + '?,'*(n_f-1) + '?)'
        for player in players:
            vals = [player[x] for x in fields]
            cur.execute(query_string, vals)

def read_players_db(db_name, tbl_name, week):
    """
    Read in player salary data / predictions from sqlite database named db_name 
    for a give week (give a citation for this code ... zetcode). Database table 
    is assumed to have colnames (name, team, pos, salary, pred_points)
    """
    
    conn = lite.connect(db_name)

    with conn:
        conn.row_factory = lite.Row
        cur = conn.cursor()
        query = 'select * from ' + tbl_name + ' where week = ' + str(week)
        cur.execute(query)
        rows = cur.fetchall()

    players = []
    for row in rows:
        player = {'name': row['name'], 
                  'team': row['team'], 
                  'pos': row['pos'], 
                  'salary': row['salary'], 
                  'pred_points': row['pred_points']
                 }
        players.append(player)
    
    conn.close()
    return players
  

def main():
    pass

if __name__ == "__main__":
    pass

