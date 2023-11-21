from typing import List, Tuple, Dict, Any, Union, Optional, Iterable
import random

StateT = [str, str, Tuple[int, int]] #isStart, isEnd, position
Actions = Any

class BCubed:
    # initialize important variables
    def __init__(self, x = 4, y = 4, endState = (), startState = (0, 0), explorationProb: float = 0.2):
        self.grid = (x, y)
        self.visitedPositions = []
        self.actions = {}
        self.position = startState
        self.endState = endState
        self.void = []
        self.explorationProb = explorationProb
        

    
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
    def getValidActions(self) -> Dict[Actions]:
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

    """
    This function takes in the variables of the current game
    state and returns the next action to take. This function uses
    the epsilon-greedy algorithm, choosing a random action with
    probability = explorationProb. Otherwise, it will pick an 
    action from the list of valid actions, according to the 
    transition probability of each action.
    
    NOTE TO MAHATHI: in the pset, epsilon-greedy outputted the action given by
    the optimal policy with prob: 1 - explorationProb. So I'm not sure if this function 
    is right.

    input: self
    returns: action
    """
    def getAction(self) -> tuple:
        validActions = self.getValidActions()

        explorationProb = self.explorationProb
        options = ["exploit", "explore"]
        chosen_option = random.choices(options, weights=(1-explorationProb, explorationProb), k=1)

        if chosen_option[0] == "explore":
            action = random.choices(list(validActions.keys()))
            return action[0]
        elif chosen_option[0] == "exploit":
            """NOTE TO MAHATHI: regarding earlier note, should we change this to match the optimal policy??? 
            instead of using validActions?"""
            return random.choices(list(validActions.keys()), weights=list(validActions.values()), k=1)[0]
    
    def getLegalActions(self):
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
        
        return possible

    def policy():
        return action

    # add void squares
    def generateVoid(self):
        self.grid 

    def simulate(self):
