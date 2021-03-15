#!/usr/bin/env python
""" generated source for module SingleTreeNode """
# package: controllers.sampleMCTS
import core.game.StateObservation

import ontology.Types

import tools.ElapsedCpuTimer

import tools.Utils

import java.util.Random

class SingleTreeNode(object):
    """ generated source for class SingleTreeNode """
    HUGE_NEGATIVE = -10000000.0
    HUGE_POSITIVE = 10000000.0
    epsilon = 1e-6
    egreedyEpsilon = 0.05
    state = StateObservation()
    parent = SingleTreeNode()
    children = []
    totValue = float()
    nVisits = int()
    m_rnd = Random()
    m_depth = int()
    lastBounds = [None]*
    curBounds = [None]*

    @overloaded
    def __init__(self, rnd):
        """ generated source for method __init__ """
        self.__init__(None, None, rnd)

    @__init__.register(object, StateObservation, SingleTreeNode, Random)
    def __init___0(self, state, parent, rnd):
        """ generated source for method __init___0 """
        self.state = state
        self.parent = parent
        self.m_rnd = rnd
        self.children = [None]*Agent.NUM_ACTIONS
        self.totValue = 0.0
        if parent != None:
            self.m_depth = parent.m_depth + 1
        else:
            self.m_depth = 0

    def mctsSearch(self, elapsedTimer):
        """ generated source for method mctsSearch """
        self.lastBounds[0] = self.curBounds[0]
        self.lastBounds[1] = self.curBounds[1]
        remaining = elapsedTimer.remainingTimeMillis()
        # int numIters = 0;
        while remaining > 10:
            backUp(selected, delta)
            remaining = elapsedTimer.remainingTimeMillis()
            # numIters++;
        # print "-- " + numIters + " --";

    def treePolicy(self):
        """ generated source for method treePolicy """
        cur = self
        while not cur.state.isGameOver() and cur.m_depth < Agent.ROLLOUT_DEPTH:
            if cur.notFullyExpanded():
                return cur.expand()
            else:
                # SingleTreeNode next = cur.egreedy();
                cur = next
        return cur

    def expand(self):
        """ generated source for method expand """
        bestAction = 0
        bestValue = -1
        i = 0
        while len(children):
            if x > bestValue and self.children[i] == None:
                bestAction = i
                bestValue = x
            i += 1
        nextState = self.state.copy()
        nextState.advance(Agent.actions[bestAction])
        tn = SingleTreeNode(nextState, self, self.m_rnd)
        self.children[bestAction] = tn
        return tn

    def uct(self):
        """ generated source for method uct """
        selected = None
        bestValue = -Double.MAX_VALUE
        for child in self.children:
            #  small sampleRandom numbers: break ties in unexpanded nodes
            if uctValue > bestValue:
                selected = child
                bestValue = uctValue
        if selected == None:
            raise RuntimeException(len(length))
        return selected

    def egreedy(self):
        """ generated source for method egreedy """
        selected = None
        if self.m_rnd.nextDouble() < self.egreedyEpsilon:
            # Choose randomly
            selected = self.children[selectedIdx]
        else:
            # pick the best Q.
            for child in self.children:
                #  small sampleRandom numbers: break ties in unexpanded nodes
                if hvVal > bestValue:
                    selected = child
                    bestValue = hvVal
        if selected == None:
            raise RuntimeException(len(length))
        return selected

    def rollOut(self):
        """ generated source for method rollOut """
        rollerState = self.state.copy()
        thisDepth = self.m_depth
        while not finishRollout(rollerState, thisDepth):
            rollerState.advance(Agent.actions[action])
            thisDepth += 1
        delta = value(rollerState)
        if delta < self.curBounds[0]:
            self.curBounds[0] = delta
        if delta > self.curBounds[1]:
            self.curBounds[1] = delta
        normDelta = Utils.normalise(delta, self.lastBounds[0], self.lastBounds[1])
        return normDelta

    def value(self, a_gameState):
        """ generated source for method value """
        gameOver = a_gameState.isGameOver()
        win = a_gameState.getGameWinner()
        rawScore = a_gameState.getGameScore()
        if gameOver and win == Types.WINNER.PLAYER_LOSES:
            return self.HUGE_NEGATIVE
        if gameOver and win == Types.WINNER.PLAYER_WINS:
            return self.HUGE_POSITIVE
        return rawScore

    def finishRollout(self, rollerState, depth):
        """ generated source for method finishRollout """
        if depth >= Agent.ROLLOUT_DEPTH:
            # rollout end condition.
            return True
        if rollerState.isGameOver():
            # end of game
            return True
        return False

    def backUp(self, node, result):
        """ generated source for method backUp """
        n = node
        while n != None:
            n.nVisits += 1
            n.totValue += result
            n = n.parent

    def mostVisitedAction(self):
        """ generated source for method mostVisitedAction """
        selected = -1
        bestValue = -Double.MAX_VALUE
        allEqual = True
        first = -1
        i = 0
        while len(children):
            if self.children[i] != None:
                if first == -1:
                    first = self.children[i].nVisits
                elif first != self.children[i].nVisits:
                    allEqual = False
                if self.children[i].nVisits + self.m_rnd.nextDouble() * self.epsilon > bestValue:
                    bestValue = self.children[i].nVisits
                    selected = i
            i += 1
        if selected == -1:
            print "Unexpected selection!"
            selected = 0
        elif allEqual:
            selected = bestAction()
        return selected

    def bestAction(self):
        """ generated source for method bestAction """
        selected = -1
        bestValue = -Double.MAX_VALUE
        i = 0
        while len(children):
            if self.children[i] != None and self.children[i].totValue + self.m_rnd.nextDouble() * self.epsilon > bestValue:
                bestValue = self.children[i].totValue
                selected = i
            i += 1
        if selected == -1:
            print "Unexpected selection!"
            selected = 0
        return selected

    def notFullyExpanded(self):
        """ generated source for method notFullyExpanded """
        for tn in children:
            if tn == None:
                return True
        return False


