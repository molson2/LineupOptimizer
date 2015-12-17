# -*- coding: utf-8 -*-
'''
Matt Olson
Command line tool for reading in player statistics and writing to DB
'''

import argparse
import data_aggregation
from db_read_write import FantasyDB, DBError
import sys


def main():
    desc = '''
    Command line tool to read in historical player stats from a given week at
    every position into a database.
    '''
    # Parse command line args
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--db_name', action='store', default=None,
                        required=True,
                        help='Name of database to write data')
    parser.add_argument('--stat_week', action='store', default=None,
                        required=True,
                        help='Select week to get player stats', type=int)
    args = parser.parse_args()
    db_name = args.db_name
    stat_week = args.stat_week

    # Create a connection to the db
    try:
        db = FantasyDB(db_name)
    except:
        raise DBError('Could not connect to DB')

    # Write historical player data
    if stat_week is not None:
        if stat_week < 1 or stat_week > 17:
            sys.stderr.write('Week outside of range [1,17] \n')
            sys.exit(0)

        # Check to see if data already exists in db
        data = db.read_table('offensive', stat_week)
        if len(data) > 0:
            warn_str = 'Data from week {} already saved'.format(stat_week)
            warn_str += ' continue: Y/N?'
            response = raw_input(warn_str)
            if response.upper() != 'Y':
                sys.exit(0)

        # Read in data and store to DB
        stats = data_aggregation.get_all_stats(stat_week)
        db.write_table(stats['qb'], 'offensive')
        db.write_table(stats['rb'], 'offensive')
        db.write_table(stats['wr'], 'offensive')
        db.write_table(stats['te'], 'offensive')
        db.write_table(stats['dst'], 'dst')
        db.write_table(stats['kicker'], 'kicker')
        db.write_table(stats['matchup'], 'matchups')
    db.close()


if __name__ == '__main__':
    main()
