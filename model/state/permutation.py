from numpy import random

from project.model.exception.stateException import StateException
from project.model.state.State import State


class Permutation(State):
    def __init__(self, number: int = 0):
        self.__elements = [0] * number
        self.__size = number

    def getSize(self):
        return self.__size

    def setElements(self, elements):
        if len(elements) != self.__size:
            raise StateException("Too many elements in Permutation")
        for index in range(0, self.__size):
            self.__elements[index] = elements[index]

    def setElement(self, index, element):
        if index >= self.__size or index < 0:
            raise StateException("Index out of Range")
        self.__elements[index] = element

    def getElements(self):
        return self.__elements

    def getElement(self, index):
        if index >= self.__size or index < 0:
            raise StateException("Index out of Range")
        return self.__elements[index]

    def copy(self):
        copy = Permutation(self.__size)
        copy.setElements(self.getElements())
        return copy

    def solution(self):
        """
        Check if Permutation is a solution
        :return: boolean
            true if contains no 0s
            false otherwise
        """
        return self.__elements.count(0) == 0

    def is0(self):
        return self.__elements.count(0) != self.__size

    def expand(self):
        """
        Return list of Children of Permutation
        Returns list of copies of this Permutation
            with first 0 replaced
            by numbers from 1 to self.__size
        :return: list of Permutations
        """
        children = []
        index = self.__find0()
        if index >= self.__size: return children
        for change in range(1, self.__size + 1):
            child = Permutation(self.__size)
            child.setElements(self.getElements())
            child.setElement(index, change)
            children.append(child)
        return children

    def mutate(self, probability=10):
        """
        Mutate Permutation with given probability
        :param probability:
        :return boolean
            true if mutated
            false otherwise
        """
        if probability > 100 or probability < 0:
            raise StateException("Mutation of probability " + str(probability) + "not possible.")
        # round makes more mutations than wanted, so probability is divided by two
        #       (or simply taken from a higher 200% instead of 100%)
        # makes occasional heavy mutations (multiple mutations)
        #       (rarity depending on given probability)
        noMutations = round(probability / getRandomNumber(1, 200))
        self.scramble(noMutations)
        return noMutations > 0

    def combine(self, other):
        """
        Combine values of this Permutation with given Permutation
        :param other: Permutation
        :return: offspring of self and other
        """
        if not isinstance(other, Permutation):
            raise StateException("Cannot combine different types.")
        if self.__size != other.__size:
            raise StateException("Cannot combine Permutations of different size.")

        firstCut = int(getRandomNumber(0, int(self.__size / 2)))
        secondCut = firstCut + int(self.__size / 2)
        toReturn = Permutation(self.__size)
        for index in range(0, self.__size):
            if firstCut < index < secondCut:
                toReturn.__elements[index] = self.__elements[index]
            else:
                toReturn.__elements[index] = other.__elements[index]
        return toReturn

    def scramble(self, number: int):
        """
        Swap given number of elements with random elements.
        :param number: int
        """
        index = 0
        while number > 0:
            self.__swap(index, int(getRandomNumber(0, self.__size)))
            index += 1
            if index >= self.__size: index = 0
            number -= 1

    def __swap(self, first: int, second: int):
        """
        Swap elements at given indexes.
        :param first: int
        :param second: int
        """
        if first != second:
            (self.__elements[first], self.__elements[second]) = \
                (self.__elements[second], self.__elements[first])

    def __eq__(self, other):
        if not isinstance(other, Permutation): return False
        if self.__size != other.__size: return False
        for index in range(0, self.__size):
            if self.__elements[index] != other.__elements[index]: return False
        return True

    def __str__(self):
        string = "Permutation :"
        for elem in self.__elements:
            string += " " + str(elem)
        return string

    def __find0(self) -> int:
        """
        Return index of first 0 in elements
        :return: int
        """
        for index in range(0, self.__size):
            if self.__elements[index] == 0:
                return index
        return self.__size

    def makeRandom(self):
        for index in range(0, self.__size):
            self.__elements[index] = int(getRandomNumber(1, self.__size + 1))

    def makeRandomSolution(self):
        """
        Puts all elements in range [1, size] in Permutation in random order
        """
        elements = [0] * self.__size
        for number in range(1, self.__size + 1):
            index = int(getRandomNumber(0, self.__size))
            while True:
                if index >= self.__size: index = 0
                if elements[index] == 0:
                    elements[index] = number
                    break
                else:
                    index += 1
        self.__elements = elements

    def makeRandomVelocity(self):
        for index in range(0, self.__size):
            self.__elements[index] = int(getRandomNumber(- self.__size + 1, self.__size - 1))

    def reduceToBounds(self):
        for index in range(0, self.__size):
            if self.__elements[index] > self.__size:
                self.__elements[index] = self.__size
            elif self.__elements[index] < 1:
                self.__elements[index] = 1

    def outOfBounds(self):
        for index in range(0, self.__size):
            if self.__elements[index] > self.__size or \
                    self.__elements[index] < 1:
                return True
        return False

    def plus(self, other):
        toReturn = Permutation(self.__size)
        for index in range(0, self.__size):
            toReturn.__elements[index] = \
                self.__elements[index] + other.__elements[index]
        return toReturn

    def minus(self, other):
        toReturn = Permutation(self.__size)
        for index in range(0, self.__size):
            toReturn.__elements[index] = \
                self.__elements[index] - other.__elements[index]
        return toReturn

    def divideBy(self, number):
        for index in range(0, self.__size):
            self.__elements[index] = \
                int(self.__elements[index] / number)

    def makeSolution(self):
        for index in range(0, self.__size):
            while self.__elements[index] in self.__elements[:index]:
                self.__elements[index] += 1
                if self.__elements[index] > self.__size:
                    self.__elements[index] = 1

def getRandomNumber(first: float, second: float) -> float:
    """
    Return random int in range [first, second)
    :param first: float
    :param second: float
    :return: int
    """
    return int(random.uniform(first, second))
