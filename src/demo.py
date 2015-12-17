'''
Matt Olson
Demo script for lineup optimization project.  This code demonstrates how to
create a new database and store new Fan Duel data in that database, and then
use that data to create lineups with the largest number of predicted points.
Please see the command line tool 'historical_data.py' to see how to read in
historical player stats.
'''

from data_aggregation import get_fanduel_data
from db_read_write import FantasyDB
from optimization import optimize_lineup

# Create DB
db_name = 'testdb'
week_fd = 15
db = FantasyDB(db_name)
db.initialize_new_db()  # only needs to be run once

# Get data
fan_duel = get_fanduel_data(week_fd)

# Write to DB
db.write_table(fan_duel, 'fan_duel')

# Now read these players from the DB (to illustrate functionality)
players = db.read_table('fan_duel', week_fd)
db.close()

# Lineup Optimization
lineup1 = optimize_lineup(players)
print(lineup1)
lineup1.get_total_points()

# Get a second lineup by enforcing constraints
force_in = ['Cutler, Jay', 'Forte, Matt']  # force in two players
force_out = [player['name'] for player in players if player['team'] == 'BUF']
salary_cap = 50000
lineup2 = optimize_lineup(players, force_in, force_out, salary_cap)
print(lineup2)
lineup2.get_total_points()
