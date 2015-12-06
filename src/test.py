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

# Create DB and write to
db_name = 'junkme'
week_fd = 13
week = 12

db = Fantasy_DB(db_name)
db.initialize_new_db()

# Get data
fan_duel = get_fanduel_data(week_fd)
qb = get_offensive_data(week, 'QB')
rb = get_offensive_data(week, 'RB')
te = get_offensive_data(week, 'TE')
wr = get_offensive_data(week, 'WR')
kicker = get_kicker_data(week)
dst = get_dst_data(week)
matchup = get_matchup(week)

# Write to DB
db.write_db(fan_duel, 'fan_duel')
db.write_db(qb, 'offensive')
db.write_db(rb, 'offensive')
db.write_db(te, 'offensive')
db.write_db(wr, 'offensive')
db.write_db(kicker, 'kicker')
db.write_db(dst, 'dst')
db.write_db(matchup, 'matchups')

# Now read these players from the DB
players = db.read_table('fan_duel', week_fd)
db.close()

# Do the optimizatoin
force_in = []
force_out = []
salary_cap = 10000

lineup = optimize_lineup(players, force_in, force_out, salary_cap)
lineup.get_players()
lineup.get_total_points()


