from project.model.problem.Problem import Problem
from project.model.state.State import State


class EvolutionaryProblem(Problem):
    def nextGeneration(self):
        self.combination()
        self.mutation()
        self.orderByValidity()
        self.survivalSelection()

    def combination(self):
        pass

    def mutation(self):
        pass

    def survivalSelection(self):
        pass

    def toString(self, state: State):
        pass

    def initializeRandomGeneration(self):
        pass

    def initializeNullGeneration(self):
        pass

    def getRandom(self):
        pass

    def makeParticles(self):
        pass

    def psoNextStep(self, noNeighborhoods: int = 20):
        pass

    def acoNextStep(self, pheromoneSolution):
        pass

    def updatePheromone(self, pheromoneSolution):
        pass

    def getPheromoneSolution(self):
        pass


