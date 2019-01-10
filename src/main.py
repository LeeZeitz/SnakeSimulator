from board import Board
from snake import Snake
from snakes.codesnake import CodeSnake

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

BOARD_HEIGHT = 15
BOARD_WIDTH = 15
NUMBER_OF_SNAKES = 2
NUMBER_OF_FOOD = 5
DELAY = 0.5


@socketio.on('subscribeToBoard')
def handleSubscribeToBoard(json):
    print ('received json: ' + str(json))
    emit('board', 'pen15')

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
        board.print()
        turn += 1
        emit('board', board.serialize())
        time.sleep(DELAY)

if __name__ == '__main__':

    
    socketio.run(app)

'''
    # Create NUMBER_OF_SNAKES snake objects in an array
    snakes = [Snake(x) for x in range(NUMBER_OF_SNAKES)]

    board = Board(BOARD_HEIGHT, BOARD_WIDTH, NUMBER_OF_FOOD, snakes)

    board.print()

    board.play()
'''