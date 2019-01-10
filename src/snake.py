import base64

HEAD_IMAGE_PATH = './media/snake_head.jpg'

# Snake object. Agent in the game
#
class Snake:

    def __init__(self, id):
        self.id = id
        self.head = []
        self.body = []
        self.length = 3
        self.health = 100

        with open(HEAD_IMAGE_PATH, 'rb') as f:
            image_data = f.read()

        self.head_image = image_data

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
                    'health': self.health ,
                    'head_image': self.head_image   
                })

    # Serializes and prints the state of the snake
    #
    def print(self):
        print (self.serialize())