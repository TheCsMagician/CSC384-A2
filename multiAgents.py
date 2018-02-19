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
        newWall = successorGameState.getWalls()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        #print(newGhostStates[0].getDirection())
        #print('\n')
        #print('curr {}, succ {}'.format(currentGameState.getScore(), successorGameState.getScore()))
        #print(newFood == newFood)
        #print(currentGameState.getCapsules())

        "*** YOUR CODE HERE ***"
        #current_capsules_pos = currentGameState.getCapsules()
        score = successorGameState.getScore()
        
        heuristic = 0
        
        curr_pos = currentGameState.getPacmanPosition()
        curr_food = currentGameState.getFood()

        
        curr_closest_ghost_dist = getClosestGhost(curr_pos, newGhostStates)[1]
        succ_closest_ghost_dist = getClosestGhost(newPos, newGhostStates)[1]
        is_closer_ghost = succ_closest_ghost_dist - curr_closest_ghost_dist
        
        
        curr_closest_food = getClosestFood(curr_pos, curr_food)
        curr_closest_food_dist = curr_closest_food[1]
        curr_closest_food_pos = curr_closest_food[0]

        succ_dist_to_closest_food = getDistPacman(newPos, curr_closest_food_pos)
        is_closer_food = succ_dist_to_closest_food - curr_closest_food_dist

        #print(is_closer_food)
        capsules_list = currentGameState.getCapsules()
        
        
        
        
        #print(is_closer)
        if  newScaredTimes[0] > 0 and newScaredTimes[0] > succ_closest_ghost_dist*2 and is_closer_ghost < 0:
            heuristic += 2 #* score
            #print('eat the ghost')
            #print(heuristic)
        
        elif succ_closest_ghost_dist < 1 and newScaredTimes[0] == 0:
            heuristic += -3 #* score
            #print(heuristic)
            #print('run away')
        
        if capsules_list != [] and newScaredTimes[0] == 0:
            closest_capsul = getClosestCapsule(curr_pos, capsules_list)
            
            closest_capsul_dist = closest_capsul[1]
            closest_capsul_pos = closest_capsul[0]
    
            succ_dist_to_closest_capsul = getDistPacman(newPos, closest_capsul_pos)
            is_closer_capsule = succ_dist_to_closest_capsul - closest_capsul_dist
            
            capsule_to_ghost_dist = getDistPacman(getClosestGhost(curr_pos, newGhostStates)[0], closest_capsul_pos)
            
            if is_closer_capsule < 0 and succ_dist_to_closest_capsul < 10\
            and capsule_to_ghost_dist < 20:
                heuristic += 2
                #print('eat the capsule')
            
            
        if  is_closer_food < 0:
            heuristic += 2 #* score
            #print(heuristic)
            #print('getting closer to food')
        elif newWall[newPos[0]][newPos[1]]:
            heuristic += -1 #* score
            #print('move away form the wall')
        #
        #print(heuristic)
        
        return heuristic + score



def getDistPacman(pacman_pos ,obj_pos):
    '''return distacne to object'''
    
    return  util.manhattanDistance(pacman_pos,obj_pos)

def getClosestFood(pacman_pos ,newFood):
    """
    return the coordiantes of the closest food , and the distance
    to it
    """
    curr_pos = pacman_pos
    dist_state_dic = {}
    food_list = newFood.asList()
    
    for f_pos in food_list:

        dist = util.manhattanDistance(curr_pos,f_pos)
        dist_state_dic[dist] = f_pos
        
    distances = dist_state_dic.keys()
    min_dist = min(distances)
    
    min_pos = dist_state_dic[min_dist]
    
    return min_pos, min_dist


def getClosestGhost(pacman_pos ,ghost_states):
    """
    return the coordiantes of the closest ghost state, and the distance
    to it
    """
    curr_pos = pacman_pos
    dist_state_dic = {}
    
    for g_state in ghost_states:
        ghost_pos = g_state.getPosition()
        dist = util.manhattanDistance(curr_pos,ghost_pos)
        dist_state_dic[dist] = ghost_pos
        
    distances = dist_state_dic.keys()
    min_dist = min(distances)
    
    min_pos = dist_state_dic[min_dist]
    
    return min_pos, min_dist

def getClosestCapsule(pacman_pos ,capsules_pos):
    """
    return the coordiantes of the closest capsul, and the distance
    to it
    """
    curr_pos = pacman_pos
    dist_pos_dic = {}
    
    for c_pos in capsules_pos:

        dist = util.manhattanDistance(curr_pos, c_pos)
        dist_pos_dic[dist] = c_pos
        
    distances = dist_pos_dic.keys()
    min_dist = min(distances)
    
    min_pos = dist_pos_dic[min_dist]
    
    return min_pos, min_dist
    
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
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

