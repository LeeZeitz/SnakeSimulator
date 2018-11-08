import random

# Board object that holds the state of the game
#
class Board:

    # Parameters:
    #      height:      (int) the height of the game board
    #      width:       (int) the width of the game board
    #      snakes:      (list) a list of snake objects present in the game
    #
    def __init__(self, height, width, food_count, snakes):

        self.height = height
        self.width = width
        self.snakes = snakes
        self.food = []

        heads = []
        for snake in snakes:
            # Assign a unique, random starting point for each snake
            while True:
                coord = self.random_coord(width, height)

                if coord not in heads:
                    break

            snake.head = coord
            heads.append(coord)
        
        for i in range (food_count):
            while True:
                coord = self.random_coord(width, height)

                if coord not in heads + self.food:
                    break

            self.food.append(coord)

            


    # Returns a random coordinate pair
    # Parameters:
    #   x_range:    upper limit on x coordinate
    #   y_range:    upper limit on y coordinate
    #
    def random_coord(self, x_range, y_range):
        return [random.randint(0, x_range - 1), random.randint(0, y_range - 1)]

    # Starts a game
    #
    def play(self):
        # While there is more than one snake on the board, keep stepping forward
        while len([snake for snake in self.snakes if snake.health > 0]) > 1:
            self.step()

    # Sends the current board state to all the snakes, gets their moves, and calls update on the board state
    #
    def step(self):
        moves = {}
        for snake in self.snakes:
            moves[snake.id] = snake.move(self)
        print (moves)


    # Serializes and prints the state of the board
    #
    def print(self):
        print ({
            'height': self.height,
            'width': self.width,
            'food': self.food,
            'snakes': [snake.serialize() for snake in self.snakes]
        })



    