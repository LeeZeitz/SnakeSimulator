import random
from pprint import pprint

MOVES_DICT = {
    'up': [0, -1],
    'down': [0, 1],
    'left': [-1, 0],
    'right': [1, 0]
}
LOWER_LIMIT = 2

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
        self.heads = []
        self.add_food_flag = 0

        for snake in snakes:
            # Assign a unique, random starting point for each snake
            while True:
                coord = self.random_coord(width, height, LOWER_LIMIT)

                if coord not in self.heads:
                    break

            snake.head = coord
            self.heads.append(coord)
        
        for i in range (food_count):
            self.add_food()


    # Adds a random piece of food to the board. Makes sure the new food will not overlap a snake
    #
    def add_food(self):
        while True:
            coord = self.random_coord(self.width, self.height, 0)
            if coord not in [coord for snake in self.snakes for coord in snake.body] + self.food + self.heads:
                break

        self.food.append(coord)

            
    # Returns a random coordinate pair
    # Parameters:
    #   x_range:    upper limit on x coordinate
    #   y_range:    upper limit on y coordinate
    #
    def random_coord(self, x_range, y_range, lower_limit):
        return [random.randint(lower_limit, x_range - 3), random.randint(lower_limit, y_range - 3)]


    # Invokes a game
    #
    def play(self):
        turn = 0        
        game = {
            'all_moves': [],
            'states': []
        }

        # While there is more than one snake on the board, keep stepping forward
        while len([snake for snake in self.snakes if snake.health > 0]) > 1:
            moves = self.step(turn)
            game['all_moves'].append(moves)
            game['states'].append(self.serialize())
            # self.print()
            turn += 1

        for snake in self.snakes:
            if snake.health > 0:
                game['winner'] = snake.id
                break
        
        return game


    # Sends the current board state to all the snakes, gets their moves, and calls update on the board state
    # Parameters:
    #       turn:   (int) integer corresponding to the number of turns elapsed in the current game
    #
    def step(self, turn):

        moves = []

        for snake in self.snakes:
            move = snake.move(self)
            moves.append(move)
            self.move(snake, move, turn)
        
        # Add food to the board if any food was eaten
        if self.add_food_flag:
            for i in range (self.add_food_flag):
                self.add_food()
            self.add_food_flag = 0
        
        return moves


    # Updates a given snake's state, and the food on the board, according to a given move. 
    # Handles kiling the snake.
    # Parameters:
    #       snake:   (Snake) snake object in game
    #       move:    (str) string according to move to make, one of 'up', 'down', 'left', 'right'
    #       turn:    (int) integer corresponding to the number of turns elapsed in the current game
    #
    def move(self, snake, move, turn):
        new_head = [snake.head[0] + MOVES_DICT[move][0], snake.head[1] + MOVES_DICT[move][1]]

        old_head = snake.head

        # Check if move is off the board and kill snake if it is
        if not self.is_valid_move(new_head):
            snake.health = 0
            return
        else: 
            snake.head = new_head

        # Check if new move causes a collision with another snake
        for enemy_snake in [s for s in self.snakes if s.health > 0 and s.id != snake.id]:
            # Is there a collision at all?
            if new_head in enemy_snake.body:
             
                # The collision is head-on-body
                if new_head != enemy_snake.head:
                    snake.health = 0

                # The collision is head-on-head and I'm shorter
                elif snake.length < enemy_snake.length:
                    snake.health = 0
                    return

                # The collision is head-on-head and we're the same length
                elif snake.length == enemy_snake.length:
                    snake.health = 0
                    enemy_snake.health = 0
                    return

                # The collision is head-on-head and I'm longer (hell yeah, gotteem)
                else:
                    enemy_snake.health = 0

        # Update the coordinates of the rest of the body
        snake.body.insert(0, old_head)

        snake.health -= 1

        # Check if the new head square has some grub
        if new_head in self.food:
            self.food = [f for f in self.food if f != new_head]
            snake.health = 100
            self.add_food_flag += 1
            
        elif turn > 3:
            snake.body.pop(-1)


        elif turn > LOWER_LIMIT:
            snake.body.pop(-1)

        return


    # Check to see if a given move is valid, i.e. if it will run the snake off the board
    # Parameters:
    #       new_head:   [x, y] coordinates of square in question
    #
    def is_valid_move(self, new_head):
        if new_head[0] < 0 or new_head[1] < 0 or new_head[0] > (self.width - 1) or new_head[1] > (self.height - 1):
            return False
        else:
            return True


    # Serializes and prints the state of the board
    #
    def print(self):
        pprint ({
            'height': self.height,
            'width': self.width,
            'food': self.food,
            'snakes': [snake.serialize() for snake in self.snakes]
        })

    def serialize(self):
        return {
            'height': self.height,
            'width': self.width,
            'food': self.food,
            'snakes': [snake.serialize() for snake in self.snakes]
        }

    