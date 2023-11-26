from typing import List, Tuple, Dict, Any, Union, Optional, Iterable
import random
import pygame
import time   

from collections import defaultdict

# new types
StateT = [str, str, Tuple[int, int]] #isStart, isEnd, position
Action = Any

# global variables
blockSize = 50  # height/width of blocks in grid

# board class that contains all information regarding the current level being solved
"""
size: tuple holding (# of cols, # of rows)
voidSquares: list of coordinates represented as tuples that are considered to be in the void
start: start state coordinate pair 
end: end state coordinate pair
"""
class Board:
    def __init__(self, size = (0,0), voidSquares = [], start = (0,0), end = (0,0), numValidBlocks = 2):
        self.cols = size[0]
        self.rows = size[1]
        self.startState = start
        self.endState = end
        self.voidSquares = voidSquares
        self.numValidBlocks = numValidBlocks

    def displayBoard(self):
        pygame.display.init()

        # create screen
        sizeX = 100 + self.cols * blockSize
        sizeY = 100 + self.rows * blockSize
        screen = pygame.display.set_mode([sizeX, sizeY])

        # draw grid
        # TODO add different color scheme for start, end, and void squares
        #pygame.draw.rect(screen, (255,0,0), (10, 10, blockSize, blockSize))
        for col in range(self.cols):
            X = 50 + col * blockSize
            for row in range(self.rows):
                Y = 50 + row * blockSize
                pygame.draw.rect(screen, (255,0,0), (X, Y, blockSize, blockSize), 2)

        # display grid
        timed = True
        while timed:
            pygame.display.update()
            time.sleep(5)
            timed = False




class BCubed:
    # initialize important variables
    def __init__(self, x = 4, y = 4, endState = (), startState = (0, 0), explorationProb: float = 0.2, board = Board()):
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
    returns: dict --> {action: transition probability}
    """
    def getActions(self) -> Dict[Action, float]:
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
    how similar do you think it should be to valueIteration?
    
    Updates self.pi after seeing a (s, a, r, s') data point
    """
    def updatePi(self, state, action, reward: float, nextState) -> None:
        self.counts[(state, action)][nextState] += 1
        self.totalCounts[(state, action)] += 1
        self.rewards[(state, action)] += reward

        # Create dictionary mapping tuples of (state, action) to a list of (nextState, prob, reward) Tuples.
        succAndRewardProb = defaultdict(list)
        stateActions = defaultdict(set)
        for s, a in self.counts.keys():
            succAndRewardProb[(s, a)] = []
            stateActions[state].add(action)
            nextStates = self.counts[(s, a)]
            for next in nextStates:
                probability = nextStates[next] / self.totalCounts[(state, action)]
                reward = self.rewards[(s, a)][next]
                succAndRewardProb[(s, a)].append((next, probability, reward))

        # Return Q(state, action) based on V(state)
        def computeQ(V, state, action) -> float:
            neighbors = succAndRewardProb[(state, action)]
            result = 0
            for neighbor in neighbors:
                nextState = neighbor[0]
                prob = neighbor[1]
                reward = neighbor[2]
                result += prob * (reward + self.discount * V[nextState])
            return result

        print('Running valueIteration...')
        V = defaultdict(float)
        while True:
            newV = defaultdict(float)
            policy = {}
            for state in stateActions:
                newV[state] = float('-inf')
                actions = stateActions[state]
                for action in actions:
                    q = computeQ(V, state, action)
                    if q > newV[state]:
                        newV[state] = q
                        policy[state] = action

            all_less = True
            for key in newV:
                if abs(newV[key] - V[key]) > 0.001:
                    all_less = False
                    break
            if all_less: break
            V = newV

        self.pi = policy

    # define reward function to get score for particular state
    def getScore(self, state) -> float:
        score = 0
        if state in self.void:
            score += -100
        if state == self.endState:
            score += self.numValidBlocks/(self.numValidBlocks - len(self.visitedPositions) + 0.01)

        return score

   
   # add void squares
    

    # simulate a game of bcubed
    def simulate(board, self):
        totalRewards = []  # The discounted rewards we get on each trial
        numIterations = 100
        totalDiscount = 1
        totalReward = 0
        state = self.startState
        
        for i in range(numIterations):
            while state != self.endState:
                action = self.getAction(state)
                nextState = action
                reward = self.getScore(state)
                self.updatePi(state, action, reward, nextState)

        ## do something with self.pi?
        return totalRewards
            
