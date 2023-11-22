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
        self.discount = 1  # for now

        # (state, action) -> {nextState -> ct} for all nextState
        self.counts = {}
        # (state, action) -> ct
        self.totalCounts = {}
        # (state, action) -> {nextState -> totalReward} for all nextState
        self.rewards = {}

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
    returns: action (coordinate of next move)
    """
    def getAction(self, state: tuple) -> tuple:
        explorationProb = self.explorationProb
        options = ["exploit", "explore"]
        chosen_option = random.choices(options, weights=(1-explorationProb, explorationProb), k=1)

        action = None
        if chosen_option[0] == "explore":
            """NOTE TO MAHATHI: should we use self.actions here instead of getActions()???"""
            validActions = self.getActions()
            action = random.choices(list(validActions.keys()), weights=list(validActions.values()), k=1)[0]
        elif chosen_option[0] == "exploit":
            action = self.pi[state]

        self.visitedPositions.append(action)  # add action to visitedPositions!
        return action

    """
    NOTE TO MAHATHI: I can work on this function later. 
    how similar do you think it should be to incorporateFeedback 
    and valueIteration?
    
    Updates self.pi after seeing a (s, a, r, s') data point
    """
    def updatePi(self, state, action, reward: int, nextState) -> None:
        # similar to incorporateFeedback and valueIteration in mountaincar
        self.counts[(state, action)][nextState] += 1
        self.totalCounts[(state, action)] += 1
        self.rewards[(state, action)] += reward

        # Create dictionary mapping tuples of (state, action) to a list of (nextState, prob, reward) Tuples.
        succAndRewardProb = {}
        for s, a in self.counts.keys():
            succAndRewardProb[(s, a)] = []
            nextStates = self.counts[(s, a)]
            for next in nextStates:
                probability = nextStates[next] / self.totalCounts[(state, action)]
                reward = self.rewards[(s, a)][next]
                succAndRewardProb[(s, a)].append((next, probability, reward))

        # need to implement valueIteration to create a optimal policy
        self.pi = valueIteration(succAndRewardProb, self.discount)



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
