import util

# import classes
from util import Board
from util import BCubed

# main method
if __name__ == "__main__":
    # initialize game variables

    # simulate game
    size = (1,2) # (cols, rows)
    start = (0,0) 
    end = (0, 1)
    voidSquares = None
    testBoard = Board((1,2), voidSquares, start, end)
    testBoard.displayBoard()
    
    game = BCubed(x = size[0], y = size[1], endState=end, startState=start)
    game.simulate()