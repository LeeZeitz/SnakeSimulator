
# Snake object. Agent in the game
#
class Snake:

    def __init__(self):
        self.head = []
        self.body = []
        self.length = 3
        self.health = 100

    # Serializes and prints the state of the snake
    #
    def print(self):
        print ({
                    'head': self.head, 
                    'body': self.body, 
                    'length': self.length, 
                    'health': self.health    
                }
            )