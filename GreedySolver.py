from BaseSolver import BaseSolver
from random import randrange
import math


# Time complexity: O(N)
# Space complexity: O(1)
def getRouteCost(route):
    cost = 0
    routeLength = len(route)

    for i in range(1, routeLength):
        previous = route[i - 1]
        current = route[i]
        cost += previous.costTo(current)

    cost += route[routeLength - 1].costTo(route[0])
    return cost


class GreedySolver(BaseSolver):
    def __init__(self, tspSolver, maxTime):
        super().__init__(tspSolver, maxTime)

    # Time complexity: A for loop (N) with (N^2) on each iteration -> O(N^3)
    # Space complexity: O(N)
    def run(self):
        defaultResults = self.getTSPSolver().defaultRandomTour()
        route = defaultResults['soln'].route
        self.setBSSFFromRoute(route)
        bestCost = self.getBSSFCost()

        startIndex = randrange(self.getCityCount())

        for i in self.getCityRange():
            if self.exceededMaxTime():
                return

            original = (startIndex + i) % self.getCityCount()
            current = original
            visited = {current}
            route = [self.getCityAt(current)]

            solution = self.greedySolve(original, current, visited, route)
            if solution is None:
                continue

            solutionCost = getRouteCost(solution)
            if solutionCost < bestCost:
                self.setBSSFFromRoute(solution)
                self.incrementSolutionCount()
                bestCost = solutionCost

    # Time complexity: Recurse at most O(N) times each being O(N) -> O(N^2)
    # Space complexity: Set and route arrays up to 2N -> O(N)
    def greedySolve(self, original, current, visited, route):
        if len(visited) == self.getCityCount():
            originalCity = self.getCityAt(original)
            costToOriginal = self.getCityAt(current).costTo(originalCity)
            return None if costToOriginal == math.inf else route

        target = self.getNextCity(current, visited)
        if target is None:
            return None
        else:
            visited.add(target)
            route.append(self.getCityAt(target))
            return self.greedySolve(original, target, visited, route)

    # Time complexity: O(N)
    # Space complexity: O(1)
    def getNextCity(self, source, visited):
        minCost = math.inf
        minIndex = None

        for i in self.getCityRange():
            if i in visited:
                continue

            target = self.getCityAt(i)
            costToCity = self.getCityAt(source).costTo(target)
            if costToCity < minCost:
                minCost = costToCity
                minIndex = i

        return minIndex
