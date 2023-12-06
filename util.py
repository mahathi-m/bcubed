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
        pygame.display.set_caption('B-Cubed!')

        # draw grid
        # TODO add different color scheme for start, end, and void squares
        #pygame.draw.rect(screen, (255,0,0), (10, 10, blockSize, blockSize))
        i = 0
        for col in range(self.cols):
            X = 50 + col * blockSize
            for row in range(self.rows):
                Y = 50 + row * blockSize
                color = (255,0,0)
                if (row, col) == (self.cols - 1, self.rows - 2): color = (0,255,0)
                pygame.draw.rect(screen, color, (X, Y, blockSize, blockSize), 2)
                i += 1

        # display grid
        timed = True
        i = 0
        while i < 10000:
            pygame.display.update()
            #time.sleep(2)
            i += 1
            timed = False
            pygame.display.flip()

        """
        # TODO: hi Mahathi dear. idk why the above commented-out code doesn't display. but this code (below) displays the grid!
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.flip()


        """

class BCubed:
    # initialize important variables
    def __init__(self, x, y, endState, startState, explorationProb: float = 0.2, board = Board()):
        self.grid = (x, y)
        self.visitedPositions = []
        self.actions = {}
        self.start = startState
        #print("start: {}".format(self.start))
        self.position = startState
        self.endState = endState
        #print("end: {}".format(self.endState))
        self.void = []
        self.explorationProb = explorationProb
        self.discount = 1  # for now
        self.numValidBlocks = x * y - 1 #for now
        self.finalPolicy = {}

        # (state, action) -> {nextState -> ct} for all nextState
        self.counts = defaultdict(lambda: defaultdict(int))
        # (state, action) -> ct
        self.totalCounts = defaultdict(int)
        # (state, action) -> {nextState -> totalReward} for all nextState
        self.rewards = defaultdict(lambda: defaultdict(float))

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
        """
        if (y - 1 > 0) and (x, y - 1) not in self.visitedPositions: # move north
            possible.append((x, y - 1))
        
        if (y + 1 < max_y) and (x, y + 1) not in self.visitedPositions: # move south
            possible.append((x, y + 1))
        
        if (x - 1 > 0) and (x - 1, y) not in self.visitedPositions: #move west
            possible.append((x - 1, y))

        if (x + 1 < max_x) and (x + 1, y) not in self.visitedPositions: # move east
            possible.append((x + 1, y))
        """
        up = (self.position[0], self.position[1] - 1)
        down = (self.position[0], self.position[1] + 1)
        right = (self.position[0] + 1, self.position[1])
        left = (self.position[0] - 1, self.position[1])
        possible.append(up)
        possible.append(down)
        possible.append(right)
        possible.append(left)
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
        if chosen_option[0] == "explore" or state not in self.pi:
            """NOTE TO MAHATHI: should we use self.actions here instead of getActions()???"""
            validActions = self.getActions()
            action = random.choices(list(validActions.keys()), weights=list(validActions.values()), k=1)[0]
        elif chosen_option[0] == "exploit":
            action = self.pi[state]

        #self.visitedPositions.add(action)  # add action to visitedPositions!
        return action


    """
    Updates self.pi after seeing a (s, a, r, s') data point
    """
    def updatePi(self, state, action, reward: float, nextState) -> None:
        self.counts[(state, action)][nextState] += 1
        self.totalCounts[(state, action)] += 1
        self.rewards[(state, action)][nextState] += reward

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

        #print('Running valueIteration...')
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
            #print(V)
            #print(newV)

            #print(policy)
            all_less = True
            for key in newV:
                if abs(newV[key] - V[key]) > 0.001:
                    all_less = False
                    break
            if all_less: break
            V = newV
        #print("new policy: {}".format(policy))
        #print("old policy: {}".format(self.pi))
        for key in policy.keys():
            self.pi[key] = policy[key]

    # define reward function to get score for particular state
    def outOfBounds(self, state) -> bool:
        if state[0] < 0  or state[0] >= self.grid[0]:
            return True
        
        if state[1] < 0 or state[1] >= self.grid[1]:
            return True
        
        return False
    
    def getScore(self, state) -> float:
        score = 0
        
        def outOfBounds(state) -> bool:
            if state[0] < 0  or state[0] >= self.grid[0]:
                return True
            
            if state[1] < 0 or state[1] >= self.grid[1]:
                return True
            
            return False

        
        #print(state)
        inVoid = state in self.void
        #print(inVoid)
        inVisited = state in self.visitedPositions
        #if inVisited: print(self.visitedPositions)
        #print(outOfBounds(state))
        if  inVoid or outOfBounds(state):
            score += -100
            self.position = self.endState
            return score
        
        if state == self.endState:
            score += 100
            score += self.numValidBlocks/abs((self.numValidBlocks - len(self.visitedPositions) + 0.01))
            #print(self.numValidBlocks)
            #print(self.visitedPositions)
            #print(abs((self.numValidBlocks - len(self.visitedPositions) + 0.01)))

        score += 10
        return score

   
   # add void squares


    # simulate a game of bcubed
    def simulate(self):
        totalRewards = defaultdict(list)  # The discounted rewards we get on each trial and matching policy 
        numIterations = 1000
        
        for i in range(numIterations):
            #print("iteration {}".format(i))
            gameReward = 0
            self.visitedPositions = []
            self.position = self.start
            while True:
                old_position = self.position
                self.visitedPositions.append(self.position)
                #("before get action")
                action = self.getAction(self.position)
                #print("action: {}".format(action))
                nextState = action
                reward = self.getScore(action)
                gameReward += reward
                self.updatePi(old_position, action, reward, nextState)
                
                
                if nextState == self.endState or self.position == self.endState: break
                #self.updatePi(self.position, action, reward, nextState) 
                self.position = nextState
            
            totalRewards[gameReward].append(self.pi)
            #print(gameReward)
        print(self.pi)  
        #print(totalRewards)  
        #print(totalRewards.keys())
        key = max(totalRewards.keys())
        print(key)
        print(totalRewards[key])
        return totalRewards
            
