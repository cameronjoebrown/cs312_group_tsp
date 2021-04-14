from ReducedCostMatrix import ReducedCostMatrix
from TSPClasses import City
from copy import deepcopy
from typing import List
import math


class BranchNode:
    def __init__(self, matrix: ReducedCostMatrix, city: City, cityIndex: int, parent):
        super().__init__()

        self.depth = 1 if parent is None else parent.get_depth() + 1
        self.matrix = matrix
        self.children = []
        self.cityIndex = cityIndex
        self.city = city
        self.parent = parent

    def __lt__(self, other):
        return self.get_cost() < other.get_cost()

    # Recursively traverses tree to compute route from a particular node
    # Time complexity: O(N)
    # Space complexity: Fills an array with nodes in the computed route: O(N)
    def compute_path(self) -> List[City]:
        if self.get_parent() is None:
            return [self.get_city()]

        parent = self.get_parent()
        path = parent.compute_path()
        path.append(self.get_city())
        return path

    # Creates child nodes the current city has a valid path to
    # Time complexity: A for loop with O(N^2) operations within; O(N^3)
    # Space complexity: N children each using N^2; O(N^3)
    def generate_child_nodes(self, cities: List[City]):
        fromIndex = self.get_city_index()
        for toIndex in range(self.get_rcm().get_col_count()):

            cost = self.get_rcm().get_value_at(fromIndex, toIndex)
            if cost < math.inf:
                rcm = deepcopy(self.get_rcm())
                rcm.select(fromIndex, toIndex)
                rcm.reduce()

                child = BranchNode(rcm, cities[toIndex], toIndex, self)
                self.children.append(child)

    def get_depth(self) -> int:
        return self.depth

    def get_city_index(self) -> int:
        return self.cityIndex

    def get_rcm(self) -> ReducedCostMatrix:
        return self.matrix

    def get_parent(self):
        return self.parent

    def get_city(self) -> City:
        return self.city

    def get_cost(self) -> float:
        return self.get_rcm().get_cost()

    def get_children(self):
        return self.children

    def get_child_count(self) -> int:
        return len(self.get_children())
