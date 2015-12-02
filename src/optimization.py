# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 18:56:00 2015

@author: matthewolson
"""
import cvxpy as cvx
import numpy as np
from scipy import sparse

class Lineup(object):
    '''
    Object to organize lineups neatly
    '''
    def __init__(self, player_list, indicator):
        self.players = [player_list[i] for (i,x) in enumerate(indicator) if x > 0]
        
    def get_total_points(self):
        return sum([player['pred_points'] for player in self.players])
    
    def get_players(self):
        return [player['name'] for player in self.players]
    
        
        
def optimize_lineup(player_list, force_in, force_out, salary_cap):
    """
    Maximize fantasy points subject to salary cap and position constraints
    Args:
        player_list: list of dictionaries with keys: name, team, pos, salary
                     pred_points
        force_in: list of player names to force in lineup
        force_out: list of player names to exclude from lineup
    """
    
    def position_constraint(player_list, pos):
        """
        Helper function to create a sparse position constraint matrix
        """
        A = np.array(map(lambda x: x['pos'] == pos, player_list), dtype=np.intp)
        return A
    
    def force_constraint(player_list, force_list):
        """
        Helper function to create a sparse matrix for force in/out player 
        constraint
        """
        n_force = len(force_list)
        n_players = len(player_list)
        V = np.ones(n_force)
        I = np.arange(n_force)
        J = [i for (i, player) in enumerate(player_list) if player['name'] in
            force_list]
        return sparse.coo_matrix((V,(I,J)),shape=(n_force,n_players))
    
    # Create constraint matrices
    A_qb = position_constraint(player_list, 'QB')
    A_rb = position_constraint(player_list, 'RB')
    A_wr = position_constraint(player_list, 'WR')
    A_te = position_constraint(player_list, 'TE')
    A_k = position_constraint(player_list, 'K')
    A_dst = position_constraint(player_list, 'D')
    
    A_force_in = force_constraint(player_list, force_in)
    A_force_out = force_constraint(player_list, force_out)
    
    salary = np.array([player['salary'] for player in player_list])
    pred_points = np.array([player['pred_points'] for player in player_list])
        
    # Set up optimization problem and solve
    players = cvx.Bool(len(player_list))
    
    constraints = [A_qb*players == 1,
                   A_rb*players == 2,
                   A_wr*players == 3,
                   A_te*players == 1,
                   A_k*players == 1,
                   A_dst*players == 1,
                   salary.T*players <= salary_cap
                   ]
    
    if len(force_in) > 0:
        constraints.append(A_force_in*players == np.ones(A_force_in.shape[0]))
    
    if len(force_out) > 0:
        constraints.append(A_force_out*players == np.zeros(A_force_out.shape[0]))

    objective = cvx.Maximize(players.T*pred_points)                                                                                                                                              
    prob = cvx.Problem(objective, constraints) 
    prob.solve(solver=cvx.GUROBI, verbose=False)
    
    # Return lineup as a nice object
    return Lineup(player_list, players.value)


def main():
    pass

if __name__ == "__main__":
    pass
    