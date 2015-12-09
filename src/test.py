# -*- coding: utf-8 -*-
'''
Matt Olson
Some unit tests
'''

import unittest
from data_aggregation import *
from db_read_write import *
from optimization import *


def write_as_txt(fname, players):
    '''
    Function to create a txt file so that we can check the 'read_fanduel_data'
    function.
    '''
    with open(fname, 'w') as f:
        f.writelines('name|team|pos|salary|pred_points\n')
        for player in players:
            info = [player['name'], player['team'], player['pos'],
                    player['salary'], player['pred_points']]
            f.writelines('{}|{}|{}|{}|{}\n'.format(*info))


class ProjectTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_text_read(self):
        '''
        Test standalone text file function
        '''
        fname = 'test.txt'
        # Read in players
        db = FantasyDB('../fantasyFootball2015.db')
        players1 = db.read_table('fan_duel', 14)
        db.close()
        # Write to file
        write_as_txt(fname, players1)
        # Read from file
        players2 = read_fanduel_data(fname)
        self.assertEqual(len(players1), len(players2))

    def test_optim(self):
        '''
        Test optimization routine
        '''
        err_msg = 'Failed to Solve: check salary_cap!'
        db = FantasyDB('../fantasyFootball2015.db')
        players = db.read_table('fan_duel', 14)
        db.close()

        # Should be able to get at least 100 points
        lineup1 = optimize_lineup(players, [], [], 60000)
        self.assertGreater(lineup1.get_total_points(), 100)

        # Check that salary cap is respected
        self.assertLessEqual(lineup1.get_salary(), 60001)
        # Check for forced_in/out players
        lineup2 = optimize_lineup(players, ['Cutler, Jay'], ['Forte, Matt'],
                                  60000)
        self.assertTrue('Cutler, Jay' in lineup2.get_players())
        self.assertFalse('Forte, Matt' in lineup2.get_players())

        with self.assertRaisesRegexp(Exception, err_msg):
            lineup3 = optimize_lineup(players, [], [], 0)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
