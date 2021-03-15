#!/usr/bin/env python
""" generated source for module SingleMCTSPlayer """
# package: controllers.sampleMCTS
import core.game.StateObservation

import tools.ElapsedCpuTimer

import java.util.Random

# 
#  * Created with IntelliJ IDEA.
#  * User: Diego
#  * Date: 07/11/13
#  * Time: 17:13
#  
class SingleMCTSPlayer(object):
    """ generated source for class SingleMCTSPlayer """
    # 
    #      * Root of the tree.
    #      
    m_root = SingleTreeNode()

    # 
    #      * Random generator.
    #      
    m_rnd = Random()

    # 
    #      * Creates the MCTS player with a sampleRandom generator object.
    #      * @param a_rnd sampleRandom generator object.
    #      
    def __init__(self, a_rnd):
        """ generated source for method __init__ """
        self.m_rnd = a_rnd
        self.m_root = SingleTreeNode(a_rnd)

    # 
    #      * Inits the tree with the new observation state in the root.
    #      * @param a_gameState current state of the game.
    #      
    def init(self, a_gameState):
        """ generated source for method init """
        # Set the game observation to a newly root node.
        self.m_root = SingleTreeNode(self.m_rnd)
        self.m_root.state = a_gameState

    # 
    #      * Runs MCTS to decide the action to take. It does not reset the tree.
    #      * @param elapsedTimer Timer when the action returned is due.
    #      * @return the action to execute in the game.
    #      
    def run(self, elapsedTimer):
        """ generated source for method run """
        # Do the search within the available time.
        self.m_root.mctsSearch(elapsedTimer)
        # Determine the best action to take and return it.
        action = self.m_root.mostVisitedAction()
        # int action = m_root.bestAction();
        return action


