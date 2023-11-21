from typing import List, Tuple, Dict, Any, Union, Optional, Iterable

StateT = [str, str, Tuple[int, int]] #isStart, isEnd, position
Actions = Any

class BCubed:
    # initialize important variables
    def __init__(self, x = 4, y = 4, endState = (), startState = (0, 0)):
        self.grid = (x, y)
        self.visitedPositions = []
        self.actions = {}
        self.position = startState
        self.endState = endState
        self.void = []
        

    
    # helper functions

    # policy
    """
    This function takes in the variables of the current game
    state and returns the possible actions that can be taken 
    from the current position mapped to the transition probability
    of moving to the square. 

    input: self
    returns: dict{action: transition probability}
    """
    def getActions(self) -> Dict[Actions]:
        actions = {} # direction: probability
        possible = []
        x = self.position[0]
        y = self.position[1]
        max_x = self.grid[0] - 1
        max_y = self.grid[1] - 1

        if (y - 1 > 0) and (x, y - 1) not in self.visitedPositions: # move north
            possible.append((x, y - 1))
        
        if (y + 1 < max_y) and (x, y + 1) not in self.visitedPositions: # move south
            possible.append((x, y + 1))
        
        if (x - 1 > 0) and (x - 1, y) not in self.visitedPositions: #move west
            possible.append((x - 1, y))

        if (x + 1 < max_x) and (x + 1, y) not in self.visitedPositions: # move east
            possible.append((x + 1, y))

        total = len(possible)
        for action in possible:
            actions[action] = (1 / total)
        
        return actions
    
    def policy():
        return action

    # add void squares
    def generateVoid(self):
        self.grid 

    def simulate(self):
