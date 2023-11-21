import util

# model-based monte carlo
class modelBasedMonteCarlo:
    def __init__(self, actions: list, discount: float, calcValIterEvery: int = 10000,
                 explorationProb: float = 0.2,) -> None:
        self.actions = actions  # list of coordinates that we can move to
        self.discount = discount
        self.calcValIterEvery = calcValIterEvery
        self.explorationProb = explorationProb
        self.numIters = 0

        """"# (state, action) -> {nextState -> ct} for all nextState
        self.tCounts = defaultdict(lambda: defaultdict(int))
        # (state, action) -> {nextState -> totalReward} for all nextState
        self.rTotal = defaultdict(lambda: defaultdict(float))"""

        self.pi = {} # Optimal policy for each state. state -> action

    # epsilon-greedy algorithm
    def getAction(self):

    def incorporateFeedback(self):

