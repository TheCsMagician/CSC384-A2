# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        ghost_pos = successorGameState.getGhostPositions()[0]
        food_list = newFood.asList()
        food_min = 9999
        ghost_min = 9999
        h = successorGameState.getScore()

        for i in food_list: 
            cost = util.manhattanDistance(newPos,i)
            if cost < food_min:
                food_min = cost
            if cost < 1:
                food_min += 100

        for i in newGhostStates:
            cost = util.manhattanDistance(newPos,i.getPosition())
            if cost < ghost_min:
                ghost_min = cost
            if cost < 2:
                ghost_min -= 200 
        
        if newPos == ghost_pos:
            return -10000
        
        return ghost_min/food_min + h

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
	

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        def max_agent(state, depth):
            minimax = -9999
            best_path = 0
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            actions = state.getLegalActions(0)
            
            for action in actions:
                pac_state = state.generateSuccessor(0, action)
                score = min_agent(pac_state,1,depth)
                if score > minimax:
                    minimax = score
                    best_path = action
            
            if depth == 0:
                return best_path
            return minimax

        def min_agent(state,ind,depth):
            mini = 9999
            if state.isLose() or state.isWin():
                return self.evaluationFunction(state)
            actions = state.getLegalActions(ind)
            for action in actions:
                gho_state = state.generateSuccessor(ind, action)
                if ind == state.getNumAgents() - 1:
                    if depth == self.depth-1:
                        score= self.evaluationFunction(gho_state)
                    else:
                        score = max_agent(gho_state, depth + 1)
                else:
                    score = min_agent(gho_state,ind+1,depth)
                if score < mini:
                    mini = score
            return mini
        return max_agent(gameState, 0)
		        
		
		    
		
		    


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def max_agent(state, depth,alpha,beta):
            minimax = -9999
            best_path = 0
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            actions = state.getLegalActions(0)
            
            for action in actions:
                pac_state = state.generateSuccessor(0, action)
                score = min_agent(pac_state,1,depth,alpha,beta)
                if score > minimax:
                    minimax = score
                    best_path = action

                if score >= beta:
                    return minimax
                if score > alpha:
                    alpha = score
            if depth == 0:
                return best_path
            return minimax

        def min_agent(state,ind,depth,alpha,beta):
            mini = 9999
            if state.isLose() or state.isWin():
                return self.evaluationFunction(state)
            actions = state.getLegalActions(ind)
            for action in actions:
                gho_state = state.generateSuccessor(ind, action)
                
                if ind == state.getNumAgents() - 1:
                    if depth == self.depth-1:
                        score = self.evaluationFunction(gho_state)
		    
                    else:
                        score = max_agent(gho_state, depth + 1,alpha,beta)
                else:
                    score = min_agent(gho_state,ind+1,depth,alpha,beta)
                
                if score < mini:
                    mini = score
                if score <= alpha:
                    return mini
                if score < beta:
                    beta = score
            return mini
        return max_agent(gameState, 0,-9999,9999)
   

        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def max_agent(state, depth):
            minimax = -9999
            best_path = 0
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            actions = state.getLegalActions(0)

            for action in actions:
                pac_state = state.generateSuccessor(0, action)
                score = min_agent(pac_state,1,depth,1)
                if score > minimax:
                    minimax = score
                    best_path = action
            if depth == 0:
                return best_path
            return minimax

        def min_agent(state,ind,depth,counter):
            total = 0
            if state.isLose() or state.isWin():
                return self.evaluationFunction(state)
            actions = state.getLegalActions(ind)
            for action in actions:
                gho_state = state.generateSuccessor(ind, action)
                if ind == state.getNumAgents() - 1:
                    if depth == self.depth-1:
                        score= self.evaluationFunction(gho_state)
                    else:
                        score = max_agent(gho_state, depth + 1)
                else:
                    score= min_agent(gho_state,ind+1,depth,counter+1)
                total+=score
            return total/counter
        
        return max_agent(gameState, 0)
        

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: The algorithm accounts for the fact that there is food capsule.
      The closer it is to the pacman the greather the score
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    ghost_pos = currentGameState.getGhostPositions()[0]
    food_list = newFood.asList()
    food_min = 9999
    ghost_min = 9999
    cap_min = 9999
    h = currentGameState.getScore()
    for i in food_list: 
        cost = util.manhattanDistance(newPos,i)
        if cost < food_min:
            food_min = cost
        if cost < 1:
            food_min += 100
    
    for i in newGhostStates:
        cost = util.manhattanDistance(newPos,i.getPosition())
        if cost < ghost_min:
            ghost_min = cost
        if cost < 2:
            ghost_min -= 200 
        if newScaredTimes[0] != 0 and cost < 5:
            ghost_min += 300
    
    for i in capsules:
        cost = util.manhattanDistance(newPos,i)
        if cost < cap_min:
            cap_min = cost
        if cost < 1 and ghost_min < 5:
            h += 200
    if cap_min == 9999:
        cap_min = 0

    if newPos == ghost_pos:
        return -10000
    
    return (ghost_min+cap_min)/food_min + h


# Abbreviation
better = betterEvaluationFunction

