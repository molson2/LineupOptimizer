# LineupOptimizer #

This project contains code to collect fantasy football data for each player
in the NFL for each week, along with FanDuel salary data.  Also included is a
function to optimize lineups by solving a mixed-integer program.  Requires
a license to GUROBI.

* `src/data_aggregation.py`: web scrapers to collect fantasy football data
* `src/db_read_write.pd`: database class to facilitate storing/accessing data
* `src/optimization.py`: create optimal lineup (max. predicted points given
  salary cap constraints, position constraints, and force in/out constraints)
* `src/demo.py`: self contained code for running an example
