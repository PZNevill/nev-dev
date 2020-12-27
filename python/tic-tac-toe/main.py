
# global variables
board_1 = dict((index, [0 for x in range(3)]) for index in ['A', 'B', 'C'])
board_2 = [[0 for x in range(3)] for x in range(3)]
board_3 = dict((index, '') for index in [i+j for i in ['A', 'B', 'C'] for j in ['1', '2', '3']])


def generate_board(current_state):
    """
    function for board generation at any stage of the game
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
    print('Hello, world!')
    generate_board(board_1)
    generate_board(board_2)
    generate_board(board_3)


if __name__ == '__main__':
    main()
