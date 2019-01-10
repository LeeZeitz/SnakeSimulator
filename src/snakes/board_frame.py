'''
The BoardFrame class stores the data from the board at each move request
'''

class BoardFrame:

	def __init__(self, data, id):
		
		print (data)
		self.id = id
		self.height = data.height
		self.width = data.width
		self.snakes = data.snakes
		self.foods = data.food
		self.ourSnake = [snake for snake in self.snakes if snake.id == self.id][0]
		self.ourLoc = self.ourSnake.body[0]
		print (self.ourSnake)


