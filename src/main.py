from board import Board
from snake import Snake

BOARD_HEIGHT = 15
BOARD_WIDTH = 15
NUMBER_OF_SNAKES = 2
NUMBER_OF_FOOD = 5



if __name__ == '__main__':

    # Create NUMBER_OF_SNAKES snake objects in an array
    snakes = [Snake(x) for x in range(NUMBER_OF_SNAKES)]

    board = Board(BOARD_HEIGHT, BOARD_WIDTH, NUMBER_OF_FOOD, snakes)

    board.print()

    board.play()