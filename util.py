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

        # (state, action) -> {nextState -> ct} for all nextState
        self.tCounts = {}
        # (state, action) -> {nextState -> totalReward} for all nextState
        self.rTotal = {}
        self.pi = {}  # Optimal policy for each state. state -> action

    
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

    """
    This function takes in the variables of the current game
    state and returns the next action to take (and also adds 
    it to visitedPositions). This function uses the epsilon-greedy 
    algorithm: with probability explorationProb, it will pick a 
    random action according to the transition probabilities.
    Otherwise, it will follow the optimal policy to return an action.

    input: self, state (tuple of coordinates, + other stuff if we want)
    returns: action
    """
    def getAction(self, state: tuple) -> tuple:
        validActions = self.getActions()

        explorationProb = self.explorationProb
        options = ["exploit", "explore"]
        chosen_option = random.choices(options, weights=(1-explorationProb, explorationProb), k=1)

        action = None
        if chosen_option[0] == "explore":
            """NOTE TO MAHATHI: should we use self.actions here instead of getActions()???"""
            action = random.choices(list(validActions.keys()), weights=list(validActions.values()), k=1)[0]
        elif chosen_option[0] == "exploit":
            action = self.pi[state]

        self.visitedPositions.append(action)  # add action to visitedPositions!
        return action

    """
    NOTE TO MAHATHI: I can work on this function later. 
    how similar do you think it should be to incorporateFeedback 
    and valueIteration?
    """
    def updatePi(self, state, action, reward: int, nextState):
        # update self.pi given (s, a, r, s')
        # similar to incorporateFeedback and valueIteration in mountaincar
        # update self.tCounts and self.rTotal


    """Not sure what this is. I think this might have resulted from working on the file at the same time as you. oops!"""
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
