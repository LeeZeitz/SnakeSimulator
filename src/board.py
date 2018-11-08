import random

# Board object that holds the state of the game
#
class Board:

    # Parameters:
    #      height:      (int) the height of the game board
    #      width:       (int) the width of the game board
    #      snakes:      (list) a list of snake objects present in the game
    #
    def __init__(self, height, width, snakes):

        self.height = height
        self.width = width
        self.snakes = snakes
        self.food = []

        heads = []
        for snake in snakes:
            while True:
                x = random.randint(0, width)
                y = random.randint(0, height)

                if [x, y] not in heads:
                    break

            snake.head = [x, y]
            heads.append([x, y])

    def print(self):
        print ({
            'height': self.height,
            'width': self.width,
            'food': self.food,
            'snakes': [snake.print() for snake in self.snakes]
        })



    