#!/usr/bin/env python

import sys
import random
import math

from collections import namedtuple

State = namedtuple('State', ['board', 'player'])
# Construct a board struct (state, turn(0v1))

class TicTacToe:
    def __init__(self, init_board = None, init_player = 'x'):
        # Game's real state, the functions are used for predict
        if not init_board:
            init_board = [None for _ in range(9)] # 0: bottom-left, 8: upper-right
        self.game_state = State(board = init_board, player=init_player)

    # Game used
    def complete(self):
        return self.terminal_test(self.game_state.board)

    def show_board(self):
        """Print out the state"""
        marker_dict = {None:'-','x':'x','o':'o'}
        def get_marker(v):
            return marker_dict[v]
        for i in range(6,-1,-3):
            print "%s,%s,%s" % tuple(map(get_marker, self.game_state.board[i:i+3]))
        print ""


    # static methods (for solver use)
    # need player for knowing turn
    def actions(self, state):
        """Return possible actions(moves)"""
        return [k for k, v in enumerate(state.board) if v is None]

    def result(self, state, action):
        """Return a new state given state & action"""
        def switch_player(player):
            if player == 'x':
                return 'o'
            else:
                return 'x'
        new_board = state.board[:] # hard copy
        new_board[action] = state.player
        return State(board=new_board, player=switch_player(state.player))

    def terminal_test(self, state):
        """Check if state is win/lose/tie
        return utility"""
        # print state
        win_combo = ([6,7,8], [3,4,5], [0,1,2], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6])
        x_loc = [i for i,x in enumerate(state) if x == 'x']
        o_loc = [i for i, x in enumerate(state) if x == 'o']
        for x in win_combo:
            if not (set(x) - set(x_loc)): # x win
                return 1
            elif not (set(x) - set(o_loc)): # o win
                return -1
            elif state.count(None) == 0: # tie
                return 0
        return False

    # def terminal_utility(self, state, player):
    #     """Calculate leaves' utilities"""
    #     return False


def minimax_solver(state, game):
    """Given state and the game (static methods),
    return the action [0-8] which achieve the max utility"""

    def max_value(state):
        result = game.terminal_test(state)
        if not result:
            return result

        v = - float("inf")
        for a in game.actions(state):
            new_state = game.results(state, a)
            v = max(v, min_value(new_state))
        return v

    def min_value(state):
        result = game.terminal_test(state)
        if not result:
            return result

        v = float("inf")
        for a in game.actions(state):
            new_state = game.results(state,a)
            v = min(v, max_value(new_state))
        return v

    l = []
    for a in game.actions(state):
        new_state = game.result(state,a)
        v = min_value(new_state)
        l.append( (v,a) )
    max_action = max(l)[1]
    print l, max_action
    return max_action

def random_solver(state):
    """A solver which randomly return: 0-8"""
    while True:
        a = int( math.floor(9 * random.random()) )
        if not state.board[a]:
            return a

if __name__ == '__main__':
    seed = int(sys.argv[1])
    random.seed(seed)

    TTT = TicTacToe(init_player = 'o')

    TTT.show_board()
    while not TTT.complete():
        if TTT.game_state.player == 'x':
            action = random_solver(TTT.game_state)
            TTT.game_state = TTT.result(TTT.game_state, action)
        else:
            action = minimax_solver(TTT.game_state, TTT)
            TTT.game_state = TTT.result(TTT.game_state, action)

        TTT.show_board()
    print "Game complete"
