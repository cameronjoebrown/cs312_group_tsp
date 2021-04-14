#!/usr/bin/python3

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))




import time
import numpy as np
from TSPClasses import *
import heapq
import itertools
import copy
from GreedySolver import GreedySolver
from BranchAndBoundSolver import BranchAndBoundSolver



class TSPSolver:
	def __init__( self, gui_view ):
		self._scenario = None

	def setupWithScenario( self, scenario ):
		self._scenario = scenario


	''' <summary>
		This is the entry point for the default solver
		which just finds a valid random tour.  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of solution, 
		time spent to find solution, number of permutations tried during search, the 
		solution found, and three null values for fields not used for this 
		algorithm</returns> 
	'''
	
	def defaultRandomTour( self, time_allowance=60.0 ):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		foundTour = False
		count = 0
		bssf = None
		start_time = time.time()
		while not foundTour and time.time()-start_time < time_allowance:
			# create a random permutation
			perm = np.random.permutation( ncities )
			route = []
			# Now build the route using the random permutation
			for i in range( ncities ):
				route.append( cities[ perm[i] ] )
			bssf = TSPSolution(route)
			count += 1
			if bssf.cost < np.inf:
				# Found a valid route
				foundTour = True
		end_time = time.time()
		results['cost'] = bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results


	''' <summary>
		This is the entry point for the greedy solver, which you must implement for 
		the group project (but it is probably a good idea to just do it for the branch-and
		bound project as a way to get your feet wet).  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found, the best
		solution found, and three null values for fields not used for this 
		algorithm</returns> 
	'''

	# Additional comments within GreedySolver.py
	# Time complexity: O(N^3)
	# Space complexity: O(N)
	def greedy(self, time_allowance=60.0):
		solver = GreedySolver(self, time_allowance)
		solver.solve()
		return solver.getResults()
	
	
	
	''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints: 
		max queue size, total number of states created, and number of pruned states.</returns> 
	'''
		
	# More detailed comments within BranchAndBoundSolver.py
    	# Time complexity: O(N! * N^2)
    	# Space complexity: q = size of queue; O(q * N^2)
    	def branchAndBound(self, time_allowance=60.0):
        	maxNodes = 100000
        	solver = BranchAndBoundSolver(self, maxNodes, time_allowance)
        	solver.solve()
        	return solver.getResults()



	''' <summary>
		This is the entry point for the algorithm you'll write for your group project.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found during search, the 
		best solution found.  You may use the other three field however you like.
		algorithm</returns> 
	'''

	def createInitialLoop(self, start_node):
		second_node = self.findNearestNodeToNode(start_node, self.unvisitedCities)
		third_node = self.findNearestNodeToTwoNodes(start_node, second_node, self.unvisitedCities)
		return [start_node, second_node, third_node]

	def findNearestNodeToNode(self, current_node, nodes):
		nearestNode = None
		distance = math.inf
		for n in nodes:
			if (n != current_node):
				if (current_node.costTo(n) < distance):
					distance = current_node.costTo(n)
					nearestNode = n
		return nearestNode

	def findNearestNodeToTwoNodes(self, node1, node2, nodes):
		nearestNode = None
		distance = math.inf
		for n in nodes:
			if (n != node1) and (n != node2):
				if (node2.costTo(n) + n.costTo(node1) < distance):
					distance = node2.costTo(n) + n.costTo(node1)
					nearestNode = n
		return nearestNode

	def findNearestNodeToRoute(self, route):
		nearestNode = None
		bestInsertionIndex = None
		CurrentLowestInsertionCost = math.inf
		for i in range(0,len(route)):
			if (i == len(route) - 1):
				i2 = 0
			else:
				i2 = i + 1
			currEdge = route[i].costTo(route[i2])
			for j in self.unvisitedCities:
				costOfInsertion = (route[i].costTo(j) + j.costTo(route[i2])) - currEdge
				if (costOfInsertion < CurrentLowestInsertionCost):
					CurrentLowestInsertionCost = costOfInsertion
					nearestNode = j
					bestInsertionIndex = i + 1
		return nearestNode, bestInsertionIndex

	def insertNode(self, route, new_node, index):
		route.insert(index, new_node)
		return route

	def routeLength(self, route):
		length = 0
		for i in range(0, len(route) - 1):
			length += route[i].costTo(route[i+1])
		length += route[i].costTo(route[0])
		return length

	def printRoute(self, route):
		string = ""
		for i in route:
			string += i._name + " "
		print(string)

	def printEdges(self, route):
		for i in range(0, len(route) - 1):
			print(route[i]._name, " to ", route[i+1]._name, ": ", route[i].costTo(route[i+1]))
		print(route[-1]._name, " to ", route[0]._name, ": ", route[-1].costTo(route[0]))


		
	def fancy( self,time_allowance=60.0 ):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		foundTour = False
		count = 0
		bssf = None
		start_time = time.time()

		# perm = np.random.permutation( ncities )
		# start_node = cities[perm[0]] #randomly selects a node to be the first node
		start_node = cities[2]

		self.unvisitedCities = set(cities)
		self.visitedCities = set()

		route = self.createInitialLoop(start_node) #creates the initial loop which only has three nodes
		# print("The initial route is")
		# self.printRoute(route)
		# self.printEdges(route)
		# print()

		for city in route:
			self.visitedCities.add(city)
			self.unvisitedCities.remove(city)
		
		while not foundTour and time.time()-start_time < time_allowance:
			
			nearestUnvisitedNode, index = self.findNearestNodeToRoute(route)
			route = self.insertNode(route, nearestUnvisitedNode, index)
			self.visitedCities.add(nearestUnvisitedNode)
			self.unvisitedCities.remove(nearestUnvisitedNode)	

			# print("New route:")
			# self.printRoute(route)
			# self.printEdges(route)
			# print()		
			
			if (len(route) == ncities):
				# Found a valid route
				foundTour = True
			count += 1
			bssf = TSPSolution(route)
			# if (count > 3):
			# 	break

	


		foundTour = True
		bssf = TSPSolution(route)

		# print("Found solution:")
		# self.printRoute(route)
		# print("Length: ", bssf.cost)
		# print(route[0]._name, " to ", route[1]._name, ": ", route[0].costTo(route[1]))
		# print(route[1]._name, " to ", route[2]._name, ": ", route[1].costTo(route[2]))
		# print(route[2]._name, " to ", route[0]._name, ": ", route[2].costTo(route[0]))
		# print()

		end_time = time.time()
		results['cost'] = bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results
		



