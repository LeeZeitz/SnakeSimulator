from board import Board
from snake import Snake
from snakes.codesnake import CodeSnake
from multiprocessing import Pool

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time
import pymongo
from pprint import pprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, ping_timeout=100000)

BOARD_HEIGHT = 15
BOARD_WIDTH = 15
NUMBER_OF_SNAKES = 4
NUMBER_OF_FOOD = 5
DELAY = 0.25

db = ''
games_col = ''

@socketio.on('message')
def handleMessage(json):
    print('received message: ' + str(json))

@socketio.on('startGame')
def handleStartGame(json):
    print ('received game json: ' + str(json))

    '''
    BOARD_HEIGHT = json['board_height']
    BOARD_WIDTH = json['board_width']
    NUMBER_OF_SNAKES = json['number_of_snakes']
    NUMBER_OF_FOOD = json['number_of_food']
    '''

    # Create NUMBER_OF_SNAKES snake objects in an array
    snakes = [CodeSnake(x) for x in range(NUMBER_OF_SNAKES)]
    board = Board(BOARD_HEIGHT, BOARD_WIDTH, NUMBER_OF_FOOD, snakes)
    board.print()
    turn = 0
    # While there is more than one snake on the board, keep stepping forward
    while len([snake for snake in board.snakes if snake.health > 0]) > 1:
        board.step(turn)
        #board.print()
        print (turn)
        turn += 1
        emit('board', board.serialize())
        time.sleep(DELAY)

def simulate_game(game_number):
    
    print (game_number)

    # Create NUMBER_OF_SNAKES snake objects in an array
    snakes = [CodeSnake(x) for x in range(NUMBER_OF_SNAKES)]

    board = Board(BOARD_HEIGHT, BOARD_WIDTH, NUMBER_OF_FOOD, snakes)

    # Play the game
    game = board.play()

    # Write game data to database
    games_col.insert_one(game)  



    return game


if __name__ == '__main__':

    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['snek_db']

    games_col = db['games']

    #socketio.run(app)

    with Pool(3) as p:
        print (p.map(simulate_game, [x for x in range(100)]))

        #games_col.insert_one(game)


