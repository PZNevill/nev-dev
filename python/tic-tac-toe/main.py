import sys

# global variables
is_running = True
players = {
    'Player 1': {
        'is_turn': False,
        'is_human': True,
        'is_winner': False,
        'player_mark': 'X'
    },
    'Player 2': {
        'is_turn': False,
        'is_human': True,
        'is_winner': False,
        'player_mark': 'O'
    }
}


def initialize_board():
    """
    function to initialize the board
    """
    # dict((index, [0 for x in range(3)]) for index in ['A', 'B', 'C'])
    # [[0 for x in range(3)] for x in range(3)]
    return dict((index, None) for index in [i + j for i in ['A', 'B', 'C'] for j in ['1', '2', '3']])


def print_board(board):
    """
    function to output tic-tac-toe board to console
    """
    print(board)


def winning_move():
    """
    function to determine of the current move is a winning move
    """
    return True


def impossible_move(move, board):
    """
    function to determine whether the chosen move has already been taken
    """
    if move in board.keys():
        if board[move] is None:
            return False
    return True


def player_move(player, player_details, board):
    """
    function to allow current player to make move
    """
    move = input(f'{player}, your turn:\n')
    while player_details['is_turn']:

        if impossible_move(move, board):
            move = input(f'Try again! {move} is not a valid option:\n')
        else:
            player_details['is_turn'] = False
            board[move] = player_details['player_mark']


def main():
    """
    main function for running process
    """
    global is_running
    board = initialize_board()

    while is_running:
        for player in players:
            players[player]['is_turn'] = True
            print_board(board)
            player_move(player, players[player], board)

        if winning_move():
            is_running = True


if __name__ == '__main__':
    main()
