# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 21:45:00 2015

@author: matthewolson
"""

import unittest
from data_aggregation import *
from db_read_write import *
from optimization import *

def write_as_txt(fname, players):
    '''
    Function to create a txt file so that we can check the 'read_fanduel_data'
    function.
    '''
    with open('fd_flat', 'w') as f:
        f.writelines('name|team|pos|salary|pred_points\n')
        for player in fan_duel:
            info = [player['name'], player['team'], player['pos'], 
                    player['salary'], player['pred_points']]
            f.writelines('{}|{}|{}|{}|{}\n'.format(*info))

            
class ProjectTests(unittest.TestCase):
    def setUp(self):
        pass
    
