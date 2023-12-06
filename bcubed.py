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
    end = (1, 0)
    voidSquares = None
    testBoard = Board((2,2), voidSquares, start, end)
    testBoard.displayBoard()
    
    #game = BCubed(x = size[0], y = size[1], endState=end, startState=start)

    #rewards = game.simulate()
    #print(len(rewards) / 100)

    new_game = BCubed(x=2, y=2, endState=(1,0), startState=(0,0))
    
    rewards = new_game.simulate()
    #print(len(rewards) / 100)