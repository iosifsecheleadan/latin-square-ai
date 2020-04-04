from project.model.state.State import State


class Particle(State):
    def __init__(self, state: State):
        self.__current = state.copy()
        self.__best = state.copy()
        state.makeRandomVelocity()
        self.__velocity = state.copy()

    def changeVelocity(self, neighborhoodBest: State):
        nextVelocity = self.__velocity.copy()
        nextVelocity.randomize()

        cognitive = self.__best.minus(self.__current)
        cognitive.randomize()
        nextVelocity = nextVelocity.plus(cognitive)

        social = neighborhoodBest.minus(self.__current)
        social.randomize()
        nextVelocity = nextVelocity.plus(social)
        '''
        average = []
        if (not nextVelocity.is0()) : average.append(nextVelocity)
        if (not cognitive.is0()): average.append(cognitive)
        if (not social.is0()): average.append(social)
        nextVelocity = nextVelocity.average(average)
        '''
        self.__velocity = nextVelocity.copy()

    def applyVelocity(self):
        self.__current = self.__current.plus(self.__velocity)
        #if self.__current.outOfBounds(): self.setCurrentToBest()
        self.__current.reduceToBounds()

    def getCurrent(self):
        return self.__current.copy()

    def setCurrentToBest(self):
        self.__current = self.__best.copy()

    def getPersonalBest(self):
        return self.__best.copy()

    def setPersonalBest(self):
        self.__best = self.__current.copy()
