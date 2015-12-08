'''
Matt Olson
Demo script for lineup optimization project
'''

from data_aggregation import *
from db_read_write import *
from optimization import *

# Create DB and write to
db_name = 'junkdb'
week_fd = 14
week = 13

db = FantasyDB(db_name)
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

# Do the optimization
force_in = []
force_out = []
salary_cap = 60000
lineup1 = optimize_lineup(players, force_in, force_out, salary_cap)
print(lineup1)
lineup1.get_total_points()

# Get a second lineup
force_in = ['Cutler, Jay', 'Forte, Matt'] # force in two players
force_out = [player['name'] for player in players if player['team'] == 'PHI']
salary_cap = 60000
lineup2 = optimize_lineup(players, force_in, force_out, salary_cap)
print(lineup2)
lineup2.get_total_points()


