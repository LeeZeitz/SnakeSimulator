'''
Functions which support the snake's movements.
'''

import random
import copy

#Finds the closest food to the snake's current location.
#Parameters: Board - board_frame class instance.
def closestFood(board):
	maxDistance = 1000
	coords = []
	listFoods = []

	for food in board.foods:
		if areClosest(board, food):
			listFoods.append(food)
	
	listFoods.sort(key=lambda x: shortestPathLength(board.ourLoc,x))
	
	if listFoods:
		return listFoods[0]
	
	for food in board.foods:
		distance = shortestPathLength(board.ourLoc, food)
		
		if distance < maxDistance:
			maxDistance = distance
			coords = food

	return coords


# Returns true if the move will not kill us.
# Parameters: Board - board_frame class instance
#			  move  - Either a coordinate on the board, or a move direction,
#					  one of "up", "down", "right, "left".
def basic_safe(board, move):
	
	if isinstance(move, str):
		dest = getDest(board,move)
	else:
		dest = move

	danger = []
	
	# Find all the dangerous coordinates.
	for snake in board.snakes:
		coords = snake["coords"]
		
		danger = danger + coords
		#print (snake)
		#print(coords[0])
	#danger = danger + board.ourSnake['coords']
	#print (danger)
	
	# Return false if the move is off the board, or would result in moving into a dangerous coordinate.	
	if (dest in danger):
		return False
	elif (dest[1] > board.height - 1) or (dest[0] > board.width - 1) or (dest[0] < 0) or (dest[1] < 0):
		return False
	else:
		return True

# Returns true if the move will not result in a head-on collision.
# Parameters: Board - board_frame class instance
#			  move  - Either a coordinate on the board, or a move direction,
#					  one of "up", "down", "right, "left".
def safe(board, move):
	if isinstance(move, str):
		dest = getDest(board,move)		
	else:
		dest = move

	if not basic_safe(board, dest):
		return False
	elif headOnCollision(board, dest):
		return False
	else:
		return True

# Returns an ideal altrenate move if the attempted move was not ideal.
# If there are no ideal moves, finds the best safe move.
# Will try moves in random directions to reduce predictabillity.
# Parameters: Board 		- board_frame class instance
#			  attemptedMove - The unsafe attempted move direction.
#			  dest  		- The square we are trying to reach
#
def altMove(board, attemptedMove, dest):
	distX = dest[0] - board.ourLoc[0]
	distY = dest[1] - board.ourLoc[1]

	possibility = ["up", "down", "right", "left"]
	priority = []

	# Find the direction either than attemptedMove
	# which gets us to our destination. Add this move to the priority list
	# first. This move should be tried first.
	if distX < 0 and attemptedMove != "left":
			priority.append("left")
	elif distX > 0 and attemptedMove != "right":
			priority.append("right")
	elif distY < 0 and attemptedMove != "up":
			priority.append("up")
	elif distY > 0 and attemptedMove != "down":
			priority.append("down")

	# Randomly order the moves we are going to try.
	random.shuffle(possibility)
	
	# Add the randomly orderd moves to the priority list to test their safety.
	for direction in possibility:
		if direction not in priority and direction != attemptedMove:
			priority.append(direction)

	# Return the first ideal move, hopefully the first move in the priority list.
	for direction in priority:
		if safe(board, direction):
			return direction

	# No ideal moves, so check if there are non-ideal safe moves.
	priority.insert(0, attemptedMove)

	#print ("no_ideal")

	# Return the first safe move.
	for direction in priority:
		if safe(board, direction):
			return direction

	return "no_safe"

# Returns the direction to move towards the passed destination coordinante.
# Will not return a move which would result in turning back on ourselves.
# Parameters: Board 		- board_frame class instance
#			  dest  		- The square we are trying to reach
#
def findMove(board, dest):
	lastMove = ""

	distX = dest[0] - board.ourLoc[0]
	distY = dest[1] - board.ourLoc[1]

	rand = bool(random.getrandbits(1))

	# Randomly try Y or X direction first.
	# Avoid turning back on the square we just came from.
	if rand or (distY == 0):
		if distX < 0 and lastMove != "Moved right":
			nextMove = "left"
		elif distX > 0 and lastMove != "Moved left": 
			nextMove = "right"
		elif distY < 0 and lastMove != "Moved down":
			nextMove = "up"
		elif distY > 0 and lastMove != "Moved up":
			nextMove = "down"
	# Randomly try Y or X direction first.
	# Avoid turning back on the square we just came from.
	if not rand or (distX == 0):
		if distY < 0 and lastMove != "Moved down":
			nextMove = "up"
		elif distY > 0 and lastMove != "Moved up":
			nextMove = "down"
		elif distX < 0 and lastMove != "Moved right":
			nextMove = "left"
		elif distX > 0 and lastMove != "Moved left": 
			nextMove = "right"
	
	# This should not happen
	elif distY == 0 and distX == 0:
		nextMove = "up"

	return nextMove

# Returns true if moving to the destination square will result in a head on collision
# with a snake that is longer than us.
# Parameters: Board 		- board_frame class instance
#			  dest  		- The square we are trying to reach
#
def headOnCollision(board, dest):

	for snake in board.snakes:
		if snake['id'] == board.ourSnake['id']:
			continue

		head = snake["coords"][0]
		diffX = abs(head[0] - dest[0])
		diffY = abs(head[1] - dest[1])
		length = len(snake['coords'])

		if (diffX + diffY == 1 ) and (length >= len(board.ourSnake['coords'])):
			return True

	return False


# Returns the destination square we are trying to reach, based on our
# current location and the direction we are trying to move in. 
# Parameters: Board 		- board_frame class instance
#			  move  		- The direction we are trying to move in
#
def getDest(board, move):
	if move == "up":
		dest = [board.ourLoc[0], board.ourLoc[1] - 1]
	elif move == "down":
		dest = [board.ourLoc[0], board.ourLoc[1] + 1]
	elif move == "right":
		dest = [board.ourLoc[0] + 1, board.ourLoc[1]]
	elif move == "left":
		dest = [board.ourLoc[0] - 1, board.ourLoc[1]]
	# should never get here
	else:
		dest = [0,0]
	return dest

# Returns a safe destination to target at the beginning of the game
# Parameters: board 		- Board_frame instance
# 			  move 			- Move string
#
def scatter(board, move):
	head = board.ourLoc
	cone = [[]]
	if move == 'up':
		distFromWall = head[1]
		for x in range(1, distFromWall + 1):
			cone.append([])
			for y in range(2 * x + 1):
				ex = head[0] - x + y
				why = head[1] - x
				if not (ex < 0 or ex > board.width - 1 or why < 0 or why > board.height - 1):
					cone[x].append([head[0] - x + y, head[1] - x])

	elif move == 'right':
		distFromWall = board.width - head[0] - 1
		for x in range(1, distFromWall + 1):
			cone.append([])
			for y in range(2 * x + 1):
				ex = head[0] + x
				why = head[1] - x + y
				if not (ex < 0 or ex > board.width - 1 or why < 0 or why > board.height - 1):
					cone[x].append([ex, why])

	elif move == 'left':
		distFromWall = head[0]
		for x in range(1, distFromWall + 1):
			cone.append([])
			for y in range(2 * x + 1):
				ex = head[0] - x
				why = head[1] - x + y
				if not (ex < 0 or ex > board.width - 1 or why < 0 or why > board.height - 1):
					cone[x].append([ex, why])

	elif move == 'down':
		distFromWall = board.height - head[1] - 1
		for x in range(1, distFromWall + 1):
			cone.append([])
			for y in range(2 * x + 1):
				ex = head[0] - x + y
				why = head[1] + x
				if not (ex < 0 or ex > board.width - 1 or why < 0 or why > board.height - 1):
					cone[x].append([ex, why])
	return cone


# Returns if our snake has the shortest path to a destination square
# Parameters: board 		- board_frame instance
#			  dest 			- destination square (coordinate pair)
#
def areClosest(board, dest):
	ourDistance = abs(board.ourLoc[0] - dest[0]) + abs(board.ourLoc[1] - dest[1])

	for snake in board.snakes:
		distance = abs(dest[0] - snake["coords"][0][0]) + abs(dest[1] - snake["coords"][0][1])

		if distance < ourDistance:
			return False

	return True


# Returns number of moves to execute shortest path from source square to target square
# Parameters: src 		- source square (coordinate pair)
#			  dest 		- destination square (coordinate pair)
#
def shortestPathLength(src, dest):
	distX = dest[0] - src[0]
	distY = dest[1] - src[1]
	length = abs(distX) + abs(distY)
	return length


def shortestPath(src, dest):
	distX = dest[0] - src[0]
	distY = dest[1] - src[1]


# Returns true if a destination square is fully surrounded, with less squares than the length of our snek. False otherwise.
# Parameters: board 		- current board object
# 			  dest 			- destination square (pair of coordinates)
#
def isSurrounded(board, dest):
	ourLength = len(board['ourSnake']['coords'])

	return True


def weightedConeMove(board, considerFood):
	danger = []
	corners = [[0,0], [board.width - 1, 0], [0, board.height - 1], [board.height - 1, board.width - 1]]
	health = board.ourSnake['health']
	
	for snake in board.snakes:
		for coords in snake["coords"]:
			danger.append(coords)
		
	coneValLeft = 0
	cone = scatter(board, "left")
	for x in range (1, len(cone)):
		for coord in cone[x]:
				if (coord in corners):
					coneValLeft = coneValLeft + (100 / float(x))
				elif coord in danger:
					coneValLeft = coneValLeft + ( 100 / (float(x) ** 3) )
				elif coord not in board.foods:
					coneValLeft = coneValLeft - ( 100 / (float(x) ** 3) )
				elif not considerFood and (coord in board.foods):
					coneValLeft = coneValLeft + ( 100 / (float(x) ** 3) )
				else:
					coneValLeft = coneValLeft - ( (100 - float(health/1.2))*10 / (float(x) ** 3) )

	coneValRight = 0
	cone = scatter(board, "right")
	for x in range (1, len(cone)):
		for coord in cone[x]:
				if (coord in corners):
					coneValRight = coneValRight + (100 / float(x))
				elif coord in danger:
					coneValRight = coneValRight + ( 100 / (float(x) ** 3) )
				elif coord not in board.foods:
					coneValRight = coneValRight - ( 100 / (float(x) ** 3) )
				elif not considerFood and (coord in board.foods):
					coneValRight = coneValRight + ( 100 / (float(x) ** 3) )
				else: 
					coneValRight = coneValRight - ( (100 - float(health/1.2))*10 / (float(x) ** 3) )
	coneValDown = 0
	cone = scatter(board, "down")
	for x in range (1, len(cone)):
		for coord in cone[x]:
				if (coord in corners):
					coneValDown = coneValDown + (100 / float(x))
				elif coord in danger:
					coneValDown = coneValDown + ( 100 / (float(x) ** 3) )
				elif coord not in board.foods:
					coneValDown = coneValDown - ( 100 / (float(x) ** 3) )
				elif not considerFood and (coord in board.foods):
					coneValDown = coneValDown + ( 100 / (float(x) ** 3) )
				else: 
					coneValDown = coneValDown - ( (100 - float(health/1.2))*10 / (float(x) ** 3) )
				
	coneValUp = 0
	cone = scatter(board, "up")
	for x in range (1, len(cone)):
		for coord in cone[x]:
				if (coord in corners):
					coneValUp = coneValUp + (100 / float(x))
				elif coord in danger:
					coneValUp = coneValUp + ( 100 / (float(x) ** 3) )
				elif coord not in board.foods:
					coneValUp = coneValUp - ( 100 / (float(x) ** 3) )
				elif not considerFood and (coord in board.foods):
					coneValUp = coneValUp + ( 100 / (float(x) ** 3) )
				else:
					coneValUp = coneValUp - ( (100 - float(health/1.2))*10 / (float(x) ** 3) )
	
	temp = [coneValLeft, coneValRight, coneValUp, coneValDown]
	bestMove = min(temp)

	if bestMove == coneValLeft:
		return "left"
	elif bestMove == coneValRight:
		return "right"
	elif bestMove == coneValUp:
		return "up"
	elif bestMove == coneValDown:
		return "down"

# Simulate the game board after a move
def sim(board, move):
	newBoard = copy.deepcopy(board)
	newBoard.turn += 1
	newBoard['ourSnake'] = updateSnake(newBoard['ourSnake'], move)
	return newBoard


# Returns given snake's object with state updated according to given move
# Parameters: snake 		- snake object to make move
#			  move 			- move (string) the snake is to make
#
def updateSnake(snake, move):
	coords = snake['coords']

	for x in range(len(coords) - 1, 0, -1):
		coords[x] = coords[x - 1]

	if move == left:
		coords[0][0] = coords[1][0] - 1
		coords[0][1] = coords[1][1] 

	elif move == right:
		coords[0][0] = coords[1][0] + 1
		coords[0][1] = coords[1][1]

	elif move == up:
		coords[0][0] = coords[1][0]
		coords[0][1] = coords[1][1] - 1

	elif move == down:
		coords[0][0] = coords[1][0]
		coords[0][1] = coords[1][1] + 1

	return snake


# Returns true if a snake is dead, false if a snake is alive
# Parameters: snake 	- a snake object
# 			  board     - A board object
#
def isDead(snake, board):
	head = snake['coords'][0]
	if head[0] > board['width'] or head[0] < 0 or head[1] > board['height'] or head[1] < 0:
		# Snake died by running into the wall
		return True
	else:
		for snek in board['snakes']:
			if snek['id'] == snake['id']:
				for x in range(1, len(snake['coords'])):
					if snake['coords'][x] == head:
						# Snake died by running into itself
						return True

			elif snek['coords'][0] == head:
				if len(snek['coords']) >= len(snake['coords']):
					# Snake died by head on collision
					return True
				else:
					# Snake killed another snake in head on collision
					return False


			elif head in snek['coords']:
				# Snake died by running into another snake
				return True
		return False

def avoidSmallSpace(board):
	ourCoord = board.ourLoc
	moves = [ ["left" ,[ourCoord[0] - 1, ourCoord[1]]], 
			  ["right",[ourCoord[0] + 1, ourCoord[1]]],
			  ["up"   ,[ourCoord[0], ourCoord[1] - 1]],
			  ["down" ,[ourCoord[0], ourCoord[1] + 1]]]

	i = 0		
	
	while i < len(moves):

		if not safe(board, moves[i][1]):
			
			del moves[i]
			i = i - 1
		i = i + 1

	if len(moves) == 0:
		return [["down", 1], ["up", 1]]

	temp = []
	
	for move in moves:
		if move[0] == "left":
			thresh = build_thresh(board, "vertical", move[1]) 
			inArea = findPointOutsideThresh(board, thresh, move[0])
			if inArea:
				area = [inArea]
				recCalcArea(board,thresh,area,inArea)
				areaLeft = len(area) + len(thresh)
			else:
				areaLeft = len(thresh)
			
			temp.append(["left", areaLeft])

		elif move[0] == "right":
			thresh = build_thresh(board, "vertical", move[1]) 
			inArea = findPointOutsideThresh(board, thresh, move[0])
			if inArea:
				area = [inArea]
				recCalcArea(board,thresh,area,inArea)
				areaRight = len(area) + len(thresh)
			else:
				areaRight = len(thresh)

			temp.append(["right", areaRight])

		elif move[0] == "up":
			thresh = build_thresh(board, "horizontal", move[1])
			inArea = findPointOutsideThresh(board, thresh, move[0])
			if inArea:
				area = [inArea]
				recCalcArea(board,thresh,area,inArea)
				areaUp = len(area) + len(thresh)
			else:
				areaUp = len(thresh)

			temp.append(["up", areaUp])

		elif move[0] == "down":
			thresh = build_thresh(board, "horizontal", move[1])
			inArea = findPointOutsideThresh(board, thresh, move[0])
			if inArea:
				area = [inArea]
				recCalcArea(board,thresh,area,inArea)
				areaDown = len(area) + len(thresh)
			else:
				areaDown = len(thresh)

			temp.append(["down", areaDown])
	

	mMax = temp[0]
	mMin = temp[0]
	
	for move in temp:
		if move[1] > mMax[1]:
			mMax = move
		
		if move[1] < mMin[1]:
			mMin = move

	
	return [mMax, mMin]

def findPointOutsideThresh(board, thresh, move):
	if move == "left":
		for move in thresh:
			if safe(board, [move[0]-1, move[1]]):
				return [move[0]-1, move[1]]
	elif move == "right":
		for move in thresh:
			if safe(board, [move[0]+1, move[1]]):
				return [move[0]+1, move[1]]
	elif move == "up":
		for move in thresh:
			if safe(board, [move[0], move[1]-1]):
				return [move[0], move[1]-1]
	elif move == "down":
		for move in thresh:
			if safe(board, [move[0], move[1]+1]):
				return [move[0], move[1]+1]
	else:
		return false


def recCalcArea(board, thresh, area, move):
	moves = [[move[0] - 1, move[1]], 
			 [move[0] + 1, move[1]],
			 [move[0], move[1] - 1],
			 [move[0], move[1] + 1]]

	for newMove in moves:
		if safe(board, newMove) and (newMove not in area) and (newMove not in thresh):
			area.append(newMove)
			recCalcArea(board, thresh, area, newMove)  
	

def build_thresh(board, dir, move):
	thresh = []

	x = move[0]
	y = move[1] 

	thresh.append([x,y])

	if (dir == "horizontal"):
		l = move[0] - 1
		r = move[0] + 1
		while (safe(board, [l,y]) or safe(board, [r,y])):
			if safe(board, [l,y]):
				thresh.append([l,y])
				l = l - 1

			if safe(board, [r,y]):
				thresh.append([r,y])
				r = r + 1
	
	elif (dir == "vertical"):
		u = move[1] - 1
		d = move[1] + 1
		while (safe(board, [x,u]) or safe(board, [x,d])):
			if safe(board, [x,u]):
				thresh.append([x,u])
				u = u - 1

			if safe(board, [x,d]):
				thresh.append([x,d])
				d = d + 1

	return thresh