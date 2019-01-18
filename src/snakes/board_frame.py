'''
The BoardFrame class stores the data from the board at each move request
'''

import json

class BoardFrame:

	def __init__(self, data, id):

		data = json.dumps(data.serialize())
		data = json.loads(data)

		for snake in data['snakes']:
			snake['body'].insert(0, snake['head'])
			snake['coords'] = snake['body']

		self.id = id
		self.height = data['height']
		self.width = data['width']
		self.snakes = data['snakes']
		self.foods = data['food']
		self.ourSnake = [snake for snake in self.snakes if snake['id'] == self.id][0]
		self.ourLoc = self.ourSnake['body'][0]


