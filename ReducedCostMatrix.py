import math
import numpy


class ReducedCostMatrix:
    def __init__(self, scenario):
        super().__init__()

        cities = scenario.getCities()
        citiesLength = len(cities)

        self.cost = 0.0
        self.length = citiesLength
        self.values = numpy.empty((self.length, self.length))

        for row in range(self.length):
            for col in range(self.length):
                self.values[row, col] = cities[row].costTo(cities[col])

    # Simply marks a city as visited and increments the cost
    # Time complexity: O(N)
    # Space complexity: No additional space needed
    def select(self, rowIndex, columnIndex):
        self.cost += self.values[rowIndex, columnIndex]
        self.values[columnIndex, rowIndex] = math.inf
        for i in range(self.length):
            self.values[i, columnIndex] = math.inf
            self.values[rowIndex, i] = math.inf

    # Performs row and column reductions and increments cost
    # Time complexity: Two nested for loops, O(N^2)
    # Space complexity: No additional space needed
    def reduce(self):
        for row in range(self.length):
            minValue = math.inf
            for column in range(self.length):
                if self.values[row, column] < minValue:
                    minValue = self.values[row, column]
            if minValue == math.inf:
                continue

            self.cost += minValue
            for column in range(self.length):
                self.values[row, column] -= minValue

        for column in range(self.length):
            minValue = math.inf
            for row in range(self.length):
                if self.values[row, column] < minValue:
                    minValue = self.values[row, column]
            if minValue == math.inf:
                continue

            self.cost += minValue
            for row in range(self.length):
                self.values[row, column] -= minValue

    def get_cost(self) -> float:
        return self.cost

    def get_row_count(self) -> int:
        return self.length

    def get_col_count(self) -> int:
        return self.length

    def get_value_at(self, row, col) -> float:
        return self.values[row, col]

    def print(self, label="RCM"):
        print('{}: {}'.format(label, self.get_cost()))
        print(self.values)
        print('')
