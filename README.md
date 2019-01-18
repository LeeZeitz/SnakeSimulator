# SnakeSimulator
This is an engine designed to simulate games of battlesnake locally. 

*Disclaimer: Since this is a Python program, it will only work with snakes implemented in Python. As of writing this, there is no http option, it's all done through Python files.*

The main purpose of this project is to allow for a lot of useful game data to be generated to train a new snake on. There is, however, a super simple React front end and Flask server implemented that provide a real-time visualization of the simulated games. 

## Data
The engine writes all the moves made by each snake in the game to a Mongo database called 'snek_db' in a column called 'games' in the following format:

 ```python 
  {
    'all_moves': [moves1, moves2, moves3, ...],
    'states':    [state1, state2, state3, ...]
  }
 ```
  
Each movesN in the all_moves list is a list of the move made by each snake at a given board state. 
Each stateN in the states list is of the form:
```python
    {
      'height': BOARD_HEIGHT,
      'width':  BOARD_WIDTH,
      'food':   FOOD,
      'snakes': SNAKES
    }
```
where height and width specify the dimensions of the game board, food is a list of coordinates of each of the food present on the board in that state, and snakes is a list of each of the snakes on the board, serialized as specified in each individual snake (more on that later).
 
This project should work out of the box if you follow the installation instructions provided (if there are none, there will be), all you have to do is implement your snake!

## Snake Methods
There are only two methods your snake needs to own for this simulator to work.

The first is the 'move' method. This method should take a board object and return a move. The rest of the snake logic can be wherever you like, but the 'move' method must be implemented to receive a board object and return some move. The move format is just a string, one of 'up', 'down', 'left', or 'right'.

The second method you must implement is the 'serialize' method. This is used by the simulation engine to dump the snake's state at each move into a database for further review. If you don't want any data to be saved about a specific snake for some reason, you still have to implement this method, but you can make it return nothing meaningful if you so choose.
