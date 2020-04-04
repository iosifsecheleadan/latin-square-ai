from project.model.exception.problemException import ProblemException
from project.model.problem.EvolutionaryProblem import EvolutionaryProblem
from project.model.state.particle import Particle
from project.model.state.permutation import Permutation
from project.model.state.permutationSet import PermutationSet, getRandomNumber

"""
Problem specification :
Generate an n by n Matrix such that
    in every cell is a unique pair of two numbers i, j
    any i or j must be in range [1, n]
    on every row or column no two numbers on position i are equal
    on every row or column no two numbers on position j are equal
"""


class DoubleSudokuProblem(EvolutionaryProblem):
    def __init__(self, size: int = 100, matrixSize: int = 3):
        """
        Initialize population of given size with matrixes of given matrixSize
        :param size:
        """
        self.__size = size
        self.__matrixSize = matrixSize
        self.__population = [PermutationSet(self.__matrixSize * 2, self.__matrixSize)] * size
        self.initializeRandomGeneration()

    def initializeRandomGeneration(self):
        for index in range(0, self.__size):
            allocate = PermutationSet(self.__matrixSize * 2, self.__matrixSize)
            allocate.makeRandom()
            self.__population[index] = allocate

    def initializeNullGeneration(self):
        self.__population = [PermutationSet(self.__matrixSize * 2, self.__matrixSize)] * self.__size

    def makeParticles(self):
        self.__population = [Particle(PermutationSet(
            self.__matrixSize * 2, self.__matrixSize))] * self.__size
        for index in range(0, self.__size):
            current = PermutationSet(self.__matrixSize * 2, self.__matrixSize)
            current.makeRandom()
            self.__population[index] = Particle(current)

    def validity(self, permutationSet: PermutationSet):
        """
        Return number of
            cells that are not unique +
            equal numbers on position i in columns or rows +
            equal numbers on position j in columns or rows
        :param permutationSet:
        :return: int
        """
        if permutationSet.getLength() / 2 != permutationSet.getSize():
            raise ProblemException("Matrix must be square.")
        val = 0
        matrixSize = permutationSet.getSize()
        # time complexity : O( 2(n-1) * 6(1+2+...+n-2) ) wheren n = no columns / rows in matrix (i.e. matrix degree)
        for d in range(0, matrixSize):
            for i in range(d, matrixSize):
                # FOR MATRIX ABOVE
                currentOnColumnAbove = permutationSet.getPermutation(d).getElement(i)  # element D, I
                currentOnRowAbove = permutationSet.getPermutation(i).getElement(d)  # element I, D
                # FOR MATRIX BELOW
                currentOnColumnBelow = permutationSet.getPermutation(d + matrixSize).getElement(i)
                currentOnRowBelow = permutationSet.getPermutation(i + matrixSize).getElement(d)
                for j in range(d + 1, matrixSize):
                    if j > i:
                        # FOR MATRIX ABOVE
                        # check element above diagonal with elements on same row
                        if currentOnColumnAbove == permutationSet.getPermutation(d).getElement(
                            j): val += 1  # D, I == D, J
                        # check element below diagonal with elements on same column
                        if currentOnRowAbove == permutationSet.getPermutation(j).getElement(d): val += 1  # I, D == J, D
                        # FOR MATRIX BELOW
                        # check element above diagonal with elements on same row
                        if currentOnColumnBelow == permutationSet.getPermutation(d + matrixSize).getElement(
                            j): val += 1  # D, I == D, J
                        # check element below diagonal with elements on same column
                        if currentOnRowBelow == permutationSet.getPermutation(j + matrixSize).getElement(
                            d): val += 1  # I, D == J, D
                    if j > d:
                        # FOR MATRIX ABOVE
                        # check element above diagonal with elements on same column
                        if currentOnColumnAbove == permutationSet.getPermutation(j).getElement(
                            i): val += 1  # D, I == J, I
                        # check element below diagonal with elements on same row
                        if currentOnRowAbove == permutationSet.getPermutation(i).getElement(j): val += 1  # I, D == I, J
                        # FOR MATRIX BELOW
                        # check element above diagonal with elements on same column
                        if currentOnColumnBelow == permutationSet.getPermutation(j + matrixSize).getElement(
                            i): val += 1  # D, I == J, I
                        # check element below diagonal with elements on same row
                        if currentOnRowBelow == permutationSet.getPermutation(i + matrixSize).getElement(
                            j): val += 1  # I, D == I, J
        # check for I,J pair duplicates
        # time complexity : O ( 1+2+...+(n*n -1) ) where n = no columns / rows in matrix (i.e. matrix degree)
        for i1 in range(0, matrixSize):
            for j1 in range(0, matrixSize):
                # ((i1, j1), (j1 + max, i1))
                first = permutationSet.getPermutation(i1).getElement(j1)
                second = permutationSet.getPermutation(j1 + matrixSize).getElement(i1)
                for i2 in range(i1, matrixSize):
                    for j2 in range(0, matrixSize):
                        # ((i2, j2), (j2 + max, i2))
                        if i1 != i2 or j1 != j2:
                            if first == permutationSet.getPermutation(i2).getElement(j2) and \
                                    second == permutationSet.getPermutation(j2 + matrixSize).getElement(i2):
                                # punish duplicates more as they are harder to correct
                                val += matrixSize

        return val

    def combination(self):
        """
        Combines every solution in the population with another random solution
        """
        initialSize = len(self.__population)
        for index in range(0, initialSize):
            random = int(getRandomNumber(0, initialSize))
            current = self.__population[index]
            self.__population.append(
                current.combine(self.__population[random]))

    def mutation(self, probability: int = 10):
        """
        Apply mutation to whole population, with given probability
        :param probability: int
        """
        for solution in self.__population:
            solution.mutate(probability)

    def survivalSelection(self):
        """
        Assumes population has been ordered by validity
        ( doubleSudokuProblem.orderByValidity() )
        Remove all beyond initial size
        """
        self.__population = self.__population[:self.__size]

    def orderByValidity(self):
        """
        Order population by validity
        """
        self.__population.sort(
            key=lambda child: self.validity(child))
        '''
        children = self.__population
        children.sort(key=lambda child: self.validity(child))
        self.__population = []
        self.__population = children
        '''

    def setNeighborhood(self, current: PermutationSet):
        # empty population
        self.__population = []
        visitedIndexes = []
        index = int(getRandomNumber(0, self.__matrixSize * 2))
        while self.__size > len(self.__population):
            if len(visitedIndexes) >= self.__matrixSize * 2: raise ProblemException(
                "Too big population. Too small matrix")
            while index in visitedIndexes:
                index = int(getRandomNumber(0, self.__matrixSize * 2))
            visitedIndexes.append(index)
            # make one permutation of given permutationSet 0
            next = PermutationSet(self.__matrixSize * 2, self.__matrixSize)
            toCopy = current.getPermutations()
            next.setPermutations(toCopy)
            next.setPermutation(index, Permutation(self.__matrixSize))
            # add expansion of given permutationSet to population
            expansion = next.expand()
            self.__population.extend(expansion)
            current.setPermutations(self.__population[int(getRandomNumber(0, len(self.__population)))].getPermutations())
            # current = self.__population[int(getRandomNumber(0, len(self.__population)))]
            self.__population = self.__population[:self.__size]

    def psoNextStep(self, noNeighborhoods: int = 5):
        # sort population
        self.__population.sort(
            key=lambda child: self.validity(child.getCurrent()))

        # find best for each neighborhood
        best = [PermutationSet(self.__matrixSize * 2, self.__matrixSize)] * noNeighborhoods
        for index in range(0, noNeighborhoods):
            best[index] = self.__population[
                int(index * self.__size / noNeighborhoods)].getCurrent()

        # perform particle operations on each particle
        for index in range(0, noNeighborhoods - 1):
            for particleIndex in range(
                    int(index * self.__size / noNeighborhoods),
                    int((index + 1) * self.__size / noNeighborhoods)):

                currentParticle = self.__population[particleIndex]
                currentParticle.changeVelocity(best[index])
                currentParticle.applyVelocity()

                if self.validity(currentParticle.getCurrent()) < \
                        self.validity(currentParticle.getPersonalBest()):
                    currentParticle.setPersonalBest()
                # currentParticle.setCurrentToBest()

    def getBestParticle(self):
        return sorted(self.__population,
                      key=lambda child: self.validity(child.getPersonalBest()))[0]

    def acoNextStep(self, pheromoneMatrix):
        for permIndex in range(0, self.__matrixSize * 2):
            for itemIndex in range(0, self.__matrixSize):
                summ = 0
                for freqIndex in range(0, self.__matrixSize):
                    summ += pheromoneMatrix[permIndex][itemIndex][freqIndex]
                # sum is now total of probabilities for all possibilities of next step

                for ant in self.__population:
                    # set next step of ant randomly
                    # depending on probability
                    next = getRandomNumber(0, summ)
                    for freqIndex in range(0, self.__matrixSize):
                        next -= pheromoneMatrix[permIndex][itemIndex][freqIndex]
                        if next < 0:
                            ant.getPermutation(permIndex).setElement(itemIndex, freqIndex + 1)
                            break
                    if next >= 0:   # should never happen
                        ant.getPermutation(permIndex).setElement(itemIndex, self.__matrixSize)
                    ant.makeSolution()

    def updatePheromone(self, pheromoneMatrix):
        # add solutions to pheromoneMatrix
        for ant in self.__population:
            currentValidity = self.validity(ant)
            for permIndex in range(0, self.__matrixSize * 2):
                for itemIndex in range(0, self.__matrixSize):
                    antChoice = ant.getPermutation(permIndex).getElement(itemIndex)
                    pheromoneMatrix[permIndex][itemIndex][antChoice - 1] += (1 / (currentValidity+1) )
                    # (antChoice - 1) because elements go from 1 to 3, while indexes go from 0 to 2
        # dry up pheromone trace (by half) # or some other constant
        for permIndex in range(0, self.__matrixSize * 2):
            for itemIndex in range(0, self.__matrixSize):
                for freqIndex in range(0, self.__matrixSize):
                    toDivideBy = round(pheromoneMatrix[permIndex][itemIndex][freqIndex] * (9 / 10), 64)
                    if toDivideBy > 0:
                        pheromoneMatrix[permIndex][itemIndex][freqIndex] /= toDivideBy   # or some other constant
        return pheromoneMatrix

    def getPheromoneSolution(self):
        """
        Returns a list that contains
            lists that contain
                frequency vectors for all values possible in the matrix
        :return: list
        """
        return [ [ [1] * self.__matrixSize
                   for i in range(0, self.__matrixSize) ]
                 for i in range(0, self.__matrixSize *2) ]

    def getBest(self):
        """
        Return the most valid element in population
        """
        return sorted(self.__population,
                      key=lambda child: self.validity(child))[0]

    def getRandom(self):
        return self.__population[int(getRandomNumber(0, self.__size))]

    def getFirst(self):
        return self.__population[0]

    def getRandomPermutationSet(self):
        permutationSet = PermutationSet(self.__matrixSize * 2, self.__matrixSize)
        permutationSet.makeRandom()
        return permutationSet

    def toString(self, permutationSet: PermutationSet):
        if permutationSet.getLength() / 2 != permutationSet.getSize():
            raise ProblemException("Matrix must be square.")
        matrixSize = permutationSet.getSize()
        toReturn = ""
        for i in range(0, matrixSize):
            for j in range(0, matrixSize):
                toReturn += "(" + str(permutationSet.getPermutation(i).getElement(j)) + ", "
                toReturn += str(permutationSet.getPermutation(j + matrixSize).getElement(i)) + ") "
            toReturn += "\n"
        return toReturn
