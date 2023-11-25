import util

# import classes
from util import Board

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
    
