import sys
from sys import argv

from PyQt5 import QtWidgets

from project.ctrl.problemController import ProblemController
from project.model.problem.doubleSudoku import DoubleSudokuProblem
from project.ui.graphic import GraphicUI


class Main:
    def __init__(self):
        self.__application = QtWidgets.QApplication(argv)

        problem = DoubleSudokuProblem()
        self.__controller = ProblemController(problem)
        self.__ui = GraphicUI(self.__controller)

    def run(self):
        self.__ui.show()
        sys.exit(self.__application.exec_())



if __name__ == '__main__':
    main = Main()
    main.run()
