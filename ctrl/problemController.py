import threading

from project.ctrl.Controller import Controller
from project.model.exception.problemException import ProblemException
from project.model.problem.EvolutionaryProblem import EvolutionaryProblem
from project.model.problem.Problem import Problem
from project.model.state.State import State


class ProblemController(Controller):
    def __init__(self, problem: Problem):
        self.__problem = problem
        self.lock = threading.Lock()
        self.solution = State()
        self.generationNumber = -1
        self.attemptValidity = -1
        self.validities = []

    def setProblem(self, problem: Problem):
        self.__problem = problem

    def getProblem(self):
        return self.__problem

    def evolutionary(self):
        self.__saveSolution("No algorithm is running", -1, -1)

        if not isinstance(self.__problem, EvolutionaryProblem):
            raise ProblemException("Cannot perform Evolutionary Algorithm on non Evolutionary Problem")
        number = 0
        self.validities = []

        thread = threading.current_thread()
        # do while thread attribute is not set to false
        while getattr(thread, "continue_run", True):
            number += 1
            self.__problem.nextGeneration()

            current = self.__problem.getBest()
            validity = self.__problem.validity(current)
            wait = self.__saveSolution(current, number, validity)
            if validity == 0: return

    def hillClimbing(self):
        self.__saveSolution("No algorithm is running", -1, -1)

        if not isinstance(self.__problem, EvolutionaryProblem):
            raise ProblemException("Cannot perform Hill Climbing Algorithm on non Problem")
        current = self.__problem.getRandomPermutationSet()
        number = 0
        self.validities = []

        thread = threading.current_thread()
        # do while thread attribute is not set to false
        while getattr(thread, "continue_run", True):
            number += 1
            self.__problem.setNeighborhood(current=current)

            current = self.__problem.getBest()
            validity = self.__problem.validity(current)
            wait = self.__saveSolution(current, number, validity)
            if validity == 0: return

    def pso(self):
        self.__saveSolution("No algoritm is running", -1, -1)

        if not isinstance(self.__problem, EvolutionaryProblem):
            raise ProblemException("Cannot perform Particle Swarm Optimisation Algorithm on non Problem")
        self.__problem.makeParticles()
        number = 0
        self.validities = []

        thread = threading.current_thread()
        # do while thread attribute is not set to false
        while getattr(thread, "continue_run", True):
            number += 1
            self.__problem.psoNextStep()

            current = self.__problem.getBestParticle().getPersonalBest()
            validity = self.__problem.validity(current)
            wait = self.__saveSolution(current, number, validity)
            if validity == 0: return

    def aco(self):
        self.__saveSolution("No algorithm is running", -1, -1)

        if not isinstance(self.__problem, EvolutionaryProblem):
            raise ProblemException("Cannot perform Anc Colony Optimisation Algorithm on non Problem")
        # self.__problem.initializeNullGeneration()
        # or without initializeNullGeneration to avoid same solution everywhere
        number = 0
        self.validities = []

        thread = threading.current_thread()
        # do while attribute is not set to false
        pheromoneMatrix = self.__problem.getPheromoneSolution()
        while getattr(thread, "continue_run", True):
            number += 1
            self.__problem.acoNextStep(pheromoneMatrix)
            self.__problem.updatePheromone(pheromoneMatrix)

            current = self.__problem.getBest()
            validity = self.__problem.validity(current)
            wait = self.__saveSolution(current, number, validity)
            if validity == 0: return

    def __saveSolution(self, solution, generation, validity):
        with self.lock:
            self.solution = solution
            self.generationNumber = generation
            self.attemptValidity = validity
            self.validities.append(validity)
            return True
        #print("saved solution")
