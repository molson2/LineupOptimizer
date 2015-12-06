# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 21:45:00 2015

@author: matthewolson
"""

import unittest

class ProjectTests(unittest.TestCase):
    def setUp(self):
        pass
    
from data_aggregation import *
from db_read_write import *
from optimization import *

week_fd = 13
week = 12

fan_duel = get_fanduel_data(week_fd)
qb = get_offensive_data(week, 'QB')
rb = get_offensive_data(week, 'RB')
te = get_offensive_data(week, 'TE')
wr = get_offensive_data(week, 'WR')

kicker = get_kicker_data(week)
dst = get_dst_data(week)
matchup = get_matchup(week)

db_name = 'junkme'
tbl_name = 'fan_duel'
init_db(db_name)

conn = lite.connect(db_name)
write_db(fan_duel, conn, tbl_name)
conn.close()

players = read_players_db(db_name, tbl_name, week_fd)

force_in = []
force_out = []
salary_cap = 60000

lineup = optimize_lineup(players, force_in, force_out, salary_cap)
lineup.get_players()


