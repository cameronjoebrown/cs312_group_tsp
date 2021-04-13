from TSPClasses import City
from TSPClasses import Scenario
from TSPClasses import TSPSolution
from typing import List
from abc import abstractmethod
import time
import math


class BaseSolver:
    def __init__(self, tspSolver, maxTime):
        super().__init__()

        self._results = {}
        self._tspSolver = tspSolver
        self._scenario = tspSolver._scenario
        self._cities = self.getScenario().getCities()
        self._cityCount = len(self._cities)
        self._maxTime = maxTime
        self._startTime = None
        self._endTime = None
        self._intermediateCount = 0
        self._total = 0
        self._pruned = 0

        self.setBSSF(None)
        self.setMaxConcurrentNodes(None)

    def solve(self):
        self._startTime = time.time()
        self.run()

        bssf = self.getBSSF()
        self._results['cost'] = bssf.cost if bssf is not None else math.inf
        self._results['time'] = self.getClampedTime()
        self._results['count'] = self._intermediateCount
        self._results['soln'] = bssf
        self._results['max'] = self.getMaxConcurrentNodes()
        self._results['total'] = self._total
        self._results['pruned'] = self._pruned

    @abstractmethod
    def run(self):
        pass

    def getBSSFRoute(self):
        return None if self.getBSSF() is None else self.getBSSF().route

    def getMaxTime(self):
        return self._maxTime

    def getResults(self):
        return self._results

    def getTSPSolver(self):
        return self._tspSolver

    def getScenario(self) -> Scenario:
        return self._scenario

    def getCities(self) -> List[City]:
        return self._cities

    def getCityCount(self) -> int:
        return self._cityCount

    def getCityAt(self, index) -> City:
        return self.getCities()[index]

    def getCityRange(self):
        return range(self.getCityCount())

    def setBSSFFromRoute(self, route):
        self.setBSSF(TSPSolution(route))

    def getBSSFCost(self) -> float:
        return math.inf if self.getBSSF() is None else self.getBSSF().cost

    def getBSSF(self) -> TSPSolution:
        return self._bssf

    def setBSSF(self, value):
        self._bssf = value

    def getMaxConcurrentNodes(self):
        return self._max

    def setMaxConcurrentNodes(self, value):
        self._max = value

    def incrementTotal(self, amount=1):
        self._total += amount

    def incrementPruned(self, amount=1):
        self._pruned += amount

    def incrementSolutionCount(self, amount=1):
        self._intermediateCount += amount

    def getTotalTime(self):
        return time.time() - self._startTime

    def getClampedTime(self):
        return min(self.getMaxTime(), self.getTotalTime())

    def exceededMaxTime(self):
        return self.getTotalTime() > self.getMaxTime()

    def tryUpdateMaxConcurrentNodes(self, new_value):
        updated_val = max(self.getMaxConcurrentNodes(), new_value)
        self.setMaxConcurrentNodes(updated_val)
