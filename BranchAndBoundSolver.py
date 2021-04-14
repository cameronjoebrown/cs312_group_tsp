from branch_bound.ReducedCostMatrix import ReducedCostMatrix
from branch_bound.BranchNode import BranchNode
from queue import PriorityQueue
from copy import deepcopy
from BaseSolver import BaseSolver
from greedy.GreedySolver import GreedySolver
from random import randrange
import math


class BranchAndBoundSolver(BaseSolver):
    def __init__(self, tspSolver, maxNodes, maxTime):
        super().__init__(tspSolver, maxTime)
        self.nodeQueue = PriorityQueue(maxNodes)
        self.setMaxConcurrentNodes(0)
        self.tryUpdateMaxConcurrentNodes(self.nodeQueue.qsize())

    # Creates a route through cities, pruning as it goes
    # Time complexity:
    #   Initial BSSF is N^3
    #   Each Branch has N - depth subproblems, each N^2
    #   Each node being queued is log(queue size)
    #   Total Time complexity: O(N! * N^2)
    # Space complexity: q = size of queue, each node is N^2;
    #   O(q * N^2)
    def run(self):
        greedySolver = GreedySolver(self.getTSPSolver(), self.getMaxTime())
        greedySolver.solve()
        self.setBSSF(greedySolver.getBSSF())
        if self.exceededMaxTime():
            return

        startIndex = randrange(self.getCityCount())
        startCity = self.getCityAt(startIndex)
        startMatrix = ReducedCostMatrix(self.getScenario())
        startMatrix.reduce()

        rootNode = BranchNode(startMatrix, startCity, startIndex, None)
        self.incrementTotal()
        if rootNode.get_cost() < self.getBSSFCost():
            self.nodeQueue.put((self.getNodeKey(rootNode), rootNode))
            self.tryUpdateMaxConcurrentNodes(self.nodeQueue.qsize())

        while not self.nodeQueue.empty() and not self.exceededMaxTime():
            currentNode = self.nodeQueue.get()[1]

            if currentNode.get_cost() >= self.getBSSFCost():
                self.incrementPruned()
                continue

            if currentNode.get_depth() == self.getCityCount():
                loopCost = currentNode.get_city().costTo(startCity)
                if loopCost == math.inf or loopCost >= self.getBSSFCost():
                    continue

                route = currentNode.compute_path()
                self.setBSSFFromRoute(route)
                self.incrementSolutionCount()
                print('Solution (time: {0:.3f})'.format(self.getClampedTime()))
                continue

            currentNode.generate_child_nodes(self.getCities())
            self.incrementTotal(currentNode.get_child_count())

            for childNode in currentNode.get_children():
                if not self.nodeQueue.full() and childNode.get_cost() < self.getBSSFCost():
                    self.nodeQueue.put((self.getNodeKey(childNode), childNode))
                else:
                    self.incrementPruned()

            self.tryUpdateMaxConcurrentNodes(self.nodeQueue.qsize())

        self.incrementPruned(self.nodeQueue.qsize())
        print('Final (time: {0:.3f})'.format(self.getClampedTime()))

    def getNodeKey(self, branchNode):
        return branchNode.get_cost() / branchNode.get_depth()
