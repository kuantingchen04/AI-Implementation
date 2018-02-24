#!/usr/bin/env python

import sys
import random
import math
from collections import namedtuple

"""TicTacToe game using Minimax algorithm"""

Debug = False

# board: list, player: o/x player's turn
State = namedtuple('State', ['board', 'player'])


class TicTacToe:
    """
    TicTacToe game object

    - general method (game use):
        complete()
        show_board()

    - static method (minimax solver use):

    """
    win_combos = ([6, 7, 8], [3, 4, 5], [0, 1, 2],
                  [0, 3, 6], [1, 4, 7], [2, 5, 8],
                  [0, 4, 8], [2, 4, 6])

    def __init__(self, init_board=None, init_player='x'):
        # Game's real state, the functions are used for predict
        if not init_board:
            # 0: bottom-left, 8: upper-right
            init_board = [None for _ in range(9)]
        self.game_state = State(board=init_board, player=init_player)

    # general methods (Game use)
    def complete(self):
        """Check if game ends"""
        return self.terminal_test(self.game_state)

    def show_board(self):
        """Print out the board:
        None -> -
        'x' -> 'x'
        'o' -> 'o'
        """
        marker_dict = {None: '-', 'x': 'x', 'o': 'o'}

        def get_marker(val):
            return marker_dict[val]
        for i in range(6, -1, -3):
            print("%s,%s,%s" %
                  tuple(map(get_marker, self.game_state.board[i:i + 3])))
        print("")

    # Static methods (Solver use)
    @staticmethod
    def actions(state):
        """Return possible actions(moves)"""
        return [k for k, v in enumerate(state.board) if v is None]

    @staticmethod
    def result(state, action):
        """Return a new state given state & action"""
        def switch_player(player):
            """Return next player"""
            if player == 'x':
                return 'o'
            else:
                return 'x'
        new_board = state.board[:]  # hard copy
        new_board[action] = state.player
        return State(board=new_board, player=switch_player(state.player))

    @staticmethod
    def player_win(state, player):
        """Check if the board contains any combo"""
        loc = [i for i, x in enumerate(state.board) if x == player]
        for combo in TicTacToe.win_combos:
            if not set(combo) - set(loc):
                return True
        return False

    @staticmethod
    def player_tie(state):
        """Check if board is full"""
        return state.board.count(None) == 0

    @staticmethod
    def terminal_test(state):
        """Check if game ends"""
        if TicTacToe.player_win(state, 'x') or TicTacToe.player_win(state, 'o') or TicTacToe.player_tie(state):
            return True
        return False

    @staticmethod
    def terminal_utility(state):
        """Calculate leaves' utilities if terminal_test return True
        x win: 1,
        o win: -1,
        tie: 0
        """
        if TicTacToe.player_win(state, 'x'):
            return 1
        elif TicTacToe.player_win(state, 'o'):
            return -1
        return 0


def minimax_solver(state, game, min_or_max):
    """Given game state (board, player) and game's static methods,
    return the action [0-8] which achieve the min/max utility.

    In this game, x: MAX, o: MIN

    Strategy for equal utilities:
        o: choose action with smallest index if equal utilities
        x: choose action with largest index if equal utilities
    """

    def max_value(state):
        """maximum utility"""
        if game.terminal_test(state):
            return game.terminal_utility(state)

        v = - float("inf")
        for a in game.actions(state):
            new_state = game.result(state, a)
            v = max(v, min_value(new_state))
        return v

    def min_value(state):
        """minimun utility"""
        if game.terminal_test(state):
            return game.terminal_utility(state)
        v = float("inf")
        for a in game.actions(state):
            new_state = game.result(state, a)
            v = min(v, max_value(new_state))
        return v

    l = []
    for a in game.actions(state):
        new_state = game.result(state, a)
        v = max_value(new_state) if min_or_max == 'min' else min_value(new_state)  # get sucessors
        l.append((v, a))
    best_action = min(l)[1] if min_or_max == 'min' else max(l)[1]

    if Debug:
        print(state.player, l, best_action)
    return best_action


def random_solver(state):
    """A solver which randomly return: 0-8"""
    while True:
        a = int(math.floor(9 * random.random()))
        if not state.board[a]:
            return a


def main():
    """Main program
    x go first, x use random strategy, o use minimax strategy
    """
    TTT = TicTacToe(init_player='x')
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

    random.seed(int(sys.argv[1]))
    main() # Run "python tictactoe.py 42", 42 is the seed you set
