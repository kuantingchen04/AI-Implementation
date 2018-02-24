Given game state (board, player) and game's static methods,
return the action [0-8] which achieve the min/max utility.

In this game, x: MAX, o: MIN

Strategy for equal utilities:
    o: choose action with smallest index
    x: choose action with largest index

- Structure

    - TicTacToe Class
        - general method (game use):
            complete()
            show_board()

        - static method (minimax solver use):

    - minimax_solver
    - random_solver

- Usage
    Run `python tictactoe.py 42`, 42 is the seed you have to specify