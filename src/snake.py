
# Snake object. Agent in the game
#
class Snake:

    def __init__(self, id):
        self.id = id
        self.head = []
        self.body = []
        self.length = 3
        self.health = 100

    def move(self, board):
        self.health -= 1
        return 'up'

    # Returns a serialized version of the snake
    #
    def serialize(self):
        return ({
                    'id': self.id,
                    'head': self.head, 
                    'body': self.body, 
                    'length': self.length, 
                    'health': self.health    
                })

    # Serializes and prints the state of the snake
    #
    def print(self):
        print (self.serialize())