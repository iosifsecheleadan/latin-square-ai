from sys import maxsize

from project.model.exception.stateException import StateException
from project.model.state.State import State
from project.model.state.permutation import Permutation, getRandomNumber

class PermutationSet(State):
    def __init__(self, number: int = 0, size: int = 0):
        """
        Initializes Set of Permutations
            with given number of Permutations
                of given size
        :param number: int
        :param size: int
        """
        self.__length = number
        self.__size = size
        self.__permutations = [Permutation(size)] * number

                # OPERATIONS ABOUT SELF

    def getLength(self):
        return self.__length

    def getSize(self):
        return self.__size

    def getBest(self):
        return self.__bestSet, self.__bestValidity

    def setBest(self, newSet, validity):
        if validity < self.__bestValidity:
            self.__bestValidity = validity
            self.__bestSet = newSet
        else: raise StateException("New validity is not better than old validity")

    def setPermutations(self, permutations):
        if len(permutations) != self.__length:
            raise StateException("Too many elements in PermutationSet.")
        for index in range(0, self.__length):
            current = permutations[index]
            self.setPermutation(index, current)

    def setPermutation(self, index: int, permutation: Permutation):
        if index >= self.__length or index < 0:
            raise StateException("Index out of Range")
        self.__permutations[index] = permutation

    def getPermutations(self):
        return self.__permutations

    def getPermutation(self, index: int):
        if index >= self.__length or index < 0:
            raise StateException("Index out of Range")
        return self.__permutations[index]

    def copy(self):
        copy = PermutationSet(self.__length, self.__size)
        for index in range(0, self.__length):
            copy.__permutations[index] = self.__permutations[index].copy()
        return copy

    def __str__(self):
        string = "Permutation Set : "
        for perm in self.__permutations:
            string += "\n" + str(perm)
        return string

            # FUNCTIONS REGARDING SELF

    def solution(self):
        """
        Check if PermutationSet is a solution
        :return: boolean
            true if all Permutations are solutions
            false otherwise
        """
        for permutation in self.__permutations:
            if not permutation.solution(): return False
        return True

    def is0(self):
        for permutation in self.__permutations:
            if not permutation.is0(): return False
        return True

    def expand(self):
        """
        Return list of Children of PermutationSet
        Return list of copies of this PermutationSet
            with first empty Permutation replaced
            by expanded Permutation
        :return: list of PermutationSet
        """
        children = []
        index = self.__find0()
        if index >= self.__length: return children
        permutation = self.getPermutation(index)
        changes = permutation.expand()
        i = 0
        while i < len(changes):
            if not changes[i].solution():
                changes.extend(changes[i].expand())
                changes.pop(i)
            else: i += 1
        for change in changes:
            child = PermutationSet(self.__length, self.__size)
            child.setPermutations(self.getPermutations())
            child.setPermutation(index, change)
            children.append(child)
        return children

    def mutate(self, probability: int = 10):
        """
        Mutate PermutationSet with given probability
        :return boolean
            true if mutated
            false otherwise
        """
        if probability > 100 or probability < 0:
            raise StateException("Mutation of probability " + str(probability) + "not possible.")
        # round makes more mutations than wanted, so probability is divided by two
        #       (or simply taken from a higher percentage - 200% instead of 100%)
        # makes occasional heavy mutations (multiple mutations)
        #       (rarity depending on given probability)
        noMutations = round(probability / getRandomNumber(1, 200))
        self.scramble(noMutations, probability)
        return noMutations > 0

    def randomize(self, severity: int = 20):
        """
        Scrambles ( .scramble(number, probability) ) given percentage of PermutationSet
        :param severity: int
        :return: boolean
            true if scrambled
            false otherwise
        """
        noMutations = int(self.__length * severity / 100)
        self.scramble(noMutations, severity)
        return noMutations > 0

    def scramble(self, number: int, probability: int = 10):
        """
        Swap given number of Permutations with random Permutations.
        Apply mutations on given number of Permutations with given probability level.
        :param number: int
        :param probability: int
        """
        index = 0
        while number > 0:
            self.__swap(index, int(getRandomNumber(0, self.__length)))
            self.__permutations[int(getRandomNumber(0, self.__length))].mutate(probability)
            index += 1
            if index >= self.__length: index = 0
            number -= 1

    def makeRandom(self):
        for index in range(0, self.__length):
            permutation = Permutation(self.__size)
            permutation.makeRandom()
            self.__permutations[index] = permutation

    def makeRandomSolution(self):
        for index in range(0, self.__length):
            permutation = Permutation(self.__size)
            permutation.makeRandomSolution()
            self.__permutations[index] = permutation

    def makeRandomVelocity(self):
        for index in range(0, self.__length):
            permutation = Permutation(self.__size)
            permutation.makeRandomVelocity()
            self.__permutations[index] = permutation

    def reduceToBounds(self):
        for permutation in self.__permutations:
            permutation.reduceToBounds()

    def outOfBounds(self):
        for permutation in self.__permutations:
            if permutation.outOfBounds(): return True
        return False

            # FUNCTIONS REGARDING SELF AND OTHER

    def __eq__(self, other):
        if not isinstance(other, PermutationSet): return False
        if self.__length != other.__length: return False
        if self.__size != other.__size: return False
        for index in range(0, self.__length):
            if self.__permutations[index] != other.__permutations[index]: return False
        return True

    def combine(self, other):
        """
        Combine values of this PermutationSet with given PermutationSet
        :param other: PermutationSet
        :return: PermutationSet
        """
        if not isinstance(other, PermutationSet):
            raise StateException("Cannot combine different types")
        if self.__length != other.__length or self.__size != other.__size:
            raise StateException("Cannot combine PermutationSets of different length or size")

        firstCut = int(getRandomNumber(0, int(self.__length / 2)))
        secondCut = firstCut + int(self.__length / 2)
        toReturn = PermutationSet(self.__length, self.__size)
        for index in range(0, self.__length):
            if firstCut < index < secondCut:
                toReturn.__permutations[index] = self.__permutations[index]
            else:
                # toReturn.__permutations[index] = other.__permutations[index]
                toReturn.__permutations[index] = \
                    self.__permutations[index].combine(other.__permutations[index])

        return toReturn

    def plus(self, other):
        if not isinstance(other, PermutationSet):
            raise StateException("Cannot add different types")
        if self.__length != other.__length or self.__size != other.__size:
            raise StateException("Cannot add PermutationSets of different length or size")

        toReturn = PermutationSet(self.__length, self.__size)
        for index in range(0, self.__length):
            toReturn.__permutations[index] = \
                self.__permutations[index].plus(other.__permutations[index])

        return toReturn

    def minus(self, other):
        if not isinstance(other, PermutationSet):
            raise StateException("Cannot subtract different types")
        if self.__length != other.__length or self.__size != other.__size:
            raise StateException("Cannot subtract PermutationSets of different length or size")

        toReturn = PermutationSet(self.__length, self.__size)
        for index in range(0, self.__length):
            toReturn.__permutations[index] = \
                self.__permutations[index].minus(other.__permutations[index])

        return toReturn

            # FUNCTIONS REGARDING ONLY OTHER(S)

    def average(self, others: list):
        total = PermutationSet(self.__length, self.__size)
        number = 0

        for other in others:
            if not isinstance(other, PermutationSet):
                raise StateException("Cannot subtract different types")
            if self.__length != other.__length or self.__size != other.__size:
                raise StateException("Cannot subtract PermutationSets of different length or size")

            total = total.plus(other)
            number += 1

        for index in range(0, self.__length):
            total.__permutations[index].divideBy(number)

        return total

            # PRIVATE METHODS

    def __swap(self, first: int, second: int):
        """
        Swap Permutations at given indexes.
        :param first: int
        :param second: int
        """
        if first != second:
            (self.__permutations[first], self.__permutations[second]) = \
                (self.__permutations[second], self.__permutations[first])

    def __find0(self):
        """
        Return index of first Permutation in PermutationSet that is not a solution.
        :return: int
        """
        for index in range(0, self.__length):
            if not self.__permutations[index].solution():
                return index
        return self.__length

    def makeSolution(self):
        for perm in self.__permutations:
            perm.makeSolution()
