"""
Demo
"""

from data_aggregation import *
from db_read_write import *
from optimization import *

# Create DB and write to
db_name = 'jundb'
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
db.write_table(fan_duel, 'fan_duel')
db.write_table(qb, 'offensive')
db.write_table(rb, 'offensive')
db.write_table(te, 'offensive')
db.write_table(wr, 'offensive')
db.write_table(kicker, 'kicker')
db.write_table(dst, 'dst')
db.write_table(matchup, 'matchups')

# Now read these players from the DB
players = db.read_table('fan_duel', week_fd)
db.close()

# Do the optimizatoin
force_in = []
force_out = []
salary_cap = 100000

lineup = optimize_lineup(players, force_in, force_out, salary_cap)
lineup.get_players()
lineup.get_total_points()

# write fan_duel data to pipe separated file
fname = 'fd_flat'

def write_as_txt(fname, players):
    with open('fd_flat', 'w') as f:
        f.writelines('name|team|pos|salary|pred_points\n')
        for player in fan_duel:
            info = [player['name'], player['team'], player['pos'], 
                    player['salary'], player['pred_points']]
            f.writelines('{}|{}|{}|{}|{}\n'.format(*info))

# and read to check!
fan_duel2 = read_fanduel_data(fname)

lineup = optimize_lineup(fan_duel2, force_in, force_out, salary_cap)
lineup.get_players()
lineup.get_total_points()





