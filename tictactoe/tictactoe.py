#!/usr/bin/env python

import sys
import random
import math

from collections import namedtuple

State = namedtuple('State', ['board', 'player']) # board: list, player: 'x' or 'o'

class TicTacToe:

    win_combos = ([6, 7, 8], [3, 4, 5], [0, 1, 2], \
                  [0, 3, 6], [1, 4, 7], [2, 5, 8], \
                  [0, 4, 8], [2, 4, 6])

    def __init__(self, init_board = None, init_player = 'x'):
        # Game's real state, the functions are used for predict
        if not init_board:
            init_board = [None for _ in range(9)] # 0: bottom-left, 8: upper-right
        self.game_state = State(board = init_board, player=init_player)

    # Game used
    def complete(self):
        return self.terminal_test(self.game_state)

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

    def player_win(self, state, player):
        loc = [i for i,x in enumerate(state.board) if x == player]
        for combo in TicTacToe.win_combos:
            if not (set(combo) - set(loc)):
                return True
        return False

    def player_tie(self, state):
        return state.board.count(None) == 0

    def terminal_test(self, state):
        """Check if state is win/lose/tie
        return utility"""
        if self.player_win(state, 'x') or self.player_win(state, 'o') or self.player_tie(state):
            return True
        return False

    def terminal_utility(self, state):
        """Calculate leaves' utilities if terminal_test return True
        x win: 1,
        o win: -1,
        tie: 0"""
        if self.player_win(state, 'x'):
            return 1
        elif self.player_win(state, 'o'):
            return -1
        elif self.player_tie(state):
            return 0

def minimax_solver(state, game, min_or_max):
    """Given state and the game's static methods,
    return the action [0-8] which achieve the min/max utility.
    In this game, x: MAX, o: MIN"""

    def max_value(state):
        if game.terminal_test(state):
            return game.terminal_utility(state)

        v = - float("inf")
        for a in game.actions(state):
            new_state = game.result(state, a)
            v = max(v, min_value(new_state))
        return v

    def min_value(state):
        if game.terminal_test(state):
            return game.terminal_utility(state)
        v = float("inf")
        for a in game.actions(state):
            new_state = game.result(state,a)
            v = min(v, max_value(new_state))
        return v

    l = []
    for a in game.actions(state):
        new_state = game.result(state,a)
        v = max_value(new_state) if min_or_max == 'min' else min_value(new_state) # sucessors
        l.append( (v,a) )
    # o: choose action with smallest index if equal utilities
    # x: choose action with largest index if equal utilities
    best_action = min(l)[1] if min_or_max == 'min' else max(l)[1]
    print state.player, l, best_action
    return best_action

def random_solver(state):
    """A solver which randomly return: 0-8"""
    while True:
        a = int( math.floor(9 * random.random()) )
        if not state.board[a]:
            return a

def main():
    TTT = TicTacToe(init_player = 'x')
    TTT.show_board()
    while not TTT.complete():
        if TTT.game_state.player == 'x':
            action = random_solver(TTT.game_state)
            TTT.game_state = TTT.result(TTT.game_state, action)
        else:
            action = minimax_solver(TTT.game_state, TTT, 'min')  # In this game, x: MAX, o: MIN
            TTT.game_state = TTT.result(TTT.game_state, action)
        TTT.show_board()

if __name__ == '__main__':
    random.seed( int(sys.argv[1]) )
    main()
