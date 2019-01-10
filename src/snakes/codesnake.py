from . board_frame import BoardFrame
from . snake_util import closestFood, weightedConeMove, findMove, safe, altMove, avoidSmallSpace

HEAD_IMAGE_PATH = './media/snake_head.jpg'

# Snake object. Agent in the game
#
class CodeSnake:

    def __init__(self, id):
        self.id = id
        self.head = []
        self.body = []
        self.length = 3
        self.health = 100

        with open(HEAD_IMAGE_PATH, 'rb') as f:
            image_data = f.read()

        self.head_image = image_data


    def move(self, data):

        board = BoardFrame(data, self.id)

        if board.foods:
            dest = closestFood(board)
        else:
            if (board.ourLoc == [board.width-1,board.height-1]):
                dest = [0,0]
            else:
                dest = [board.width-1,board.height-1]

        if (board.ourSnake['health'] > 25):
            if board.ourSnake['health'] > 55:
                coneMove = weightedConeMove(board, False)
            
            else:
                #Go towards the closest food, otherwise go towards a corner of the board. 
                coneMove = weightedConeMove(board, True)
            
            spaceMove = avoidSmallSpace(board)

            if (spaceMove[1][1] < board.ourSnake['length'] or not safe(board,coneMove)):
                move = spaceMove[0][0]
                whichMove = "space"
            else:
                
                move = coneMove
                whichMove = "cone"
        
        else:
            move = findMove(board, dest)
            whichMove = "backup"

        #Find altrenate safe move if the desired move was not ideal.
        # TODO: maybe should be a while loop? Call alt move until it's actually ideal?
        if not safe(board, move):
            move = altMove(board, move, dest)
            whichMove = "alt"
            print("alt")
        
        #	print ("move: " + move)

        # Catch errors and display in taunt to debug.
        if move == "no_safe":
            print ("ERROR!")
            return{
                "move": "up",
                "taunt": "ERROR!"
            }

        else:
            return {
                "move": move,
                "taunt": whichMove
            }
	


    # Returns a serialized version of the snake
    #
    def serialize(self):
        return ({
                    'id': self.id,
                    'head': self.head, 
                    'body': self.body, 
                    'length': self.length, 
                    'health': self.health,
                    'head_image': self.head_image   
                })


    # Serializes and prints the state of the snake
    #
    def print(self):
        print (self.serialize())