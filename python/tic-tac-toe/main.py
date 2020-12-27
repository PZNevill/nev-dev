
import sys


def initialize_board():
    """
    function to initialize the board
    """
    # dict((index, [0 for x in range(3)]) for index in ['A', 'B', 'C'])
    # [[0 for x in range(3)] for x in range(3)]
    return dict((index, '') for index in [i + j for i in ['A', 'B', 'C'] for j in ['1', '2', '3']])


def print_board(current_state):
    """
    function to output tic-tac-toe board to console
    """
    print(current_state)
    pass


def winning_move():
    """
    function to determine of the current move is a winning move
    """
    pass


def impossible_move():
    """
    function to determine whether the chosen move has already been taken
    """
    pass


def player_move(player):
    pass


def main():
    """
    main function for running process
    """
    board = initialize_board()
    print_board(board)


if __name__ == '__main__':
    main()
