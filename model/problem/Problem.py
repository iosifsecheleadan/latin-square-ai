from project.model.state.State import State


class Problem:
    def validity(self, state: State):
        pass

    def orderByValidity(self):
        pass

    def getBest(self):
        pass

    def setNeighborhood(self, current: State):
        pass

    def toString(self, state: State):
        pass
