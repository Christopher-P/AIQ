#!/usr/bin/env python
""" generated source for module Agent """
# package: controllers.sampleMCTS
import core.game.Observation
import core.game.StateObservation
import core.player.AbstractPlayer
import ontology.Types
import tools.ElapsedCpuTimer
import java.util.ArrayList
import java.util.Random

# 
#  * Created with IntelliJ IDEA.
#  * User: ssamot
#  * Date: 14/11/13
#  * Time: 21:45
#  * This is a Java port from Tom Schaul's VGDL - https://github.com/schaul/py-vgdl
#

class Agent(AbstractPlayer):
    """ generated source for class Agent """
    NUM_ACTIONS = int()
    ROLLOUT_DEPTH = 10
    K = Math.sqrt(2)
    actions = []

    # 
    #      * Random generator for the agent.
    #      
    mctsPlayer = SingleMCTSPlayer()

    # 
    #      * Public constructor with state observation and time due.
    #      * @param so state observation of the current game.
    #      * @param elapsedTimer Timer for the controller creation.
    #      
    def __init__(self, so, elapsedTimer):
        """ generated source for method __init__ """
        super(Agent, self).__init__()
        # Get the actions in a static array.
        act = so.getAvailableActions()
        self.actions = [None]*len(act)
        i = 0
        while len(actions):
            self.actions[i] = act.get(i)
            i += 1
        len(actions)
        # Create the player.
        self.mctsPlayer = SingleMCTSPlayer(Random())

    # 
    #      * Picks an action. This function is called every game step to request an
    #      * action from the player.
    #      * @param stateObs Observation of the current state.
    #      * @param elapsedTimer Timer when the action returned is due.
    #      * @return An action for the current state
    #      
    def act(self, stateObs, elapsedTimer):
        """ generated source for method act """
        obs = stateObs.getFromAvatarSpritesPositions()
        grid = stateObs.getObservationGrid()
        # Set the state observation object as the new root of the tree.
        self.mctsPlayer.init(stateObs)
        # Determine the action using MCTS...
        action = self.mctsPlayer.run(elapsedTimer)
        # ... and return it.
        return self.actions[action]


