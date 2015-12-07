# TODO #

* command-line script that can be run on tuesdays - Fabric for AWS?
* read player list from CSV
  - for my future self, it would be nice to be able to generate my own
    predictions in R, save them to a csv, and then jam them through the
    optimizer
* refactor database R/W - maybe have a database object that subclasses the
  sqlite one?
  - DB = ffdb(db_name)
    * DB.write('table', what)
    * DB.close()
    * DB.read('table')
    * DB.createNewFramework()
* more graceful optimization exit status optimizatoin terminates unsuccefuly
* (calculate points based on historical data according to fanduel scoring ...
  for historical type backtesting?)

# Refined Todo #

* Standalone script to read in data
  - check to see what week it is, if we have data from that week, etc.
* Unit-testing
* A nice demo
