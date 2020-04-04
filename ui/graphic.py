import threading

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from project.ctrl.problemController import ProblemController
from project.model.problem.doubleSudoku import DoubleSudokuProblem
from project.model.state.permutationSet import PermutationSet

import numpy

class GraphicUI(QMainWindow):
    def __init__(self, controller: ProblemController):
        self.__child = threading.Thread()

        self.__controller = controller
        self.__problemRequirementText = "Generate a Matrix of pairs (I, J) such that:" \
                                        "\n\t- No two pairs are equal" \
                                        "\n\t- No two I's are equal on the same row or column" \
                                        "\n\t- No two J's are equal on the same row or column" \
                                        "\nWith the following algorithms:" \
                                        "\n\t- Evolutionary : Combines solutions creating new generations of solutions until a good one is found" \
                                        "\n\t- Hill Climbing : Looks for the best solution in a random search space" \
                                        "\n\t- Particle Swarm Optimisation : "

        QMainWindow.__init__(self)
        self.__centralWidget = QWidget(self)
        self.__gridLayout = QGridLayout(self)

        self.__titleLabel = QLabel("Solution here: ")
        self.__solutionLabel = QLabel("Give input below and start one of the algorithms.")
        self.__plotCanvas = FigureCanvas(Figure())
        self.__axes = self.__plotCanvas.figure.add_subplot()
        
        self.__getSizeLabel = QLabel("Give size of matrix: ")
        self.__getSizeEdit = QLineEdit("integer")

        self.__getPopulationLabel = QLabel("Give size of population: ")
        self.__getPopulationEdit = QLineEdit("integer")

        self.__showProgressButton = QPushButton("Show Progress", self)
        self.__stopAlgorithmButton = QPushButton("Stop Trying", self)

        self.__startEvolutionaryButton = QPushButton("Start Evolutionary", self)
        self.__startHillClimbingButton = QPushButton("Start Hill Climbing", self)
        self.__startPSOButton = QPushButton("Start PSO", self)
        self.__startACOButton = QPushButton("Start ACO", self)

        self.__initializeWindow()
        self.__initializeTexts()
        self.__initializeButtons()
        self.__initializeGrid()

    def __initializeWindow(self):
        self.setMinimumSize(500, 500)

        self.setCentralWidget(self.__centralWidget)
        self.__centralWidget.setLayout(self.__gridLayout)

    def __initializeTexts(self):
        self.setWindowTitle("Artificially Intelligent Methods Inspired from Nature")

        self.__titleLabel.setToolTip(self.__problemRequirementText)
        self.__solutionLabel.setToolTip(self.__problemRequirementText)

        self.__getSizeLabel.setToolTip("Give size of Matrix to generate")
        self.__getSizeLabel.setToolTip("Must be integer")
        self.__showProgressButton.setToolTip("Shows the best solution up to this point")

        self.__startEvolutionaryButton.setToolTip("Start solving the problem using the Evolutionary Algorithm")
        self.__startHillClimbingButton.setToolTip("Start solving the problem using the Hill Climbing Button")
        self.__stopAlgorithmButton.setToolTip("Stop all algorithms")

    def __initializeButtons(self):
        self.__showProgressButton.clicked.connect(self.showProgress)
        self.__stopAlgorithmButton.clicked.connect(self.stopAlgorithm)

        self.__startEvolutionaryButton.clicked.connect(self.startEvolutionary)
        self.__startHillClimbingButton.clicked.connect(self.startHillClimbing)
        self.__startPSOButton.clicked.connect(self.startPSO)
        self.__startACOButton.clicked.connect(self.startACO)

    def __initializeGrid(self):
        for column in range(0, 3):
            self.__gridLayout.setColumnStretch(column, 1)
        for row in range(0, 4):
            self.__gridLayout.setRowStretch(row, 1)
        self.__gridLayout.setRowStretch(1, 5)
        self.__gridLayout.setRowStretch(2, 20)

        self.__gridLayout.addWidget(self.__titleLabel, 0, 0, 1, 3)
        self.__gridLayout.addWidget(self.__solutionLabel, 1, 0, 1, 3)
        self.__gridLayout.addWidget(self.__plotCanvas, 2, 0, 1, 3)

        self.__gridLayout.addWidget(self.__getSizeLabel, 3, 0)
        self.__gridLayout.addWidget(self.__getSizeEdit, 3, 1)
        self.__gridLayout.addWidget(self.__showProgressButton, 3, 2)

        self.__gridLayout.addWidget(self.__getPopulationLabel, 4, 0)
        self.__gridLayout.addWidget(self.__getPopulationEdit, 4, 1)
        self.__gridLayout.addWidget(self.__stopAlgorithmButton, 4, 2)

        self.__gridLayout.addWidget(self.__startEvolutionaryButton, 5, 0)
        self.__gridLayout.addWidget(self.__startHillClimbingButton, 5, 1)
        self.__gridLayout.addWidget(self.__startPSOButton, 5, 2)

        self.__gridLayout.addWidget(self.__startACOButton, 6, 0)

    @pyqtSlot()
    def startEvolutionary(self):
        """
        Run Evolutionary Algorithm in new thread
        """
        if self.preRunChecks("Evolutionary"):
            self.__child = threading.Thread(target=self.__controller.evolutionary)
            self.__child.start()

    @pyqtSlot()
    def startHillClimbing(self):
        """
        Run Hill Climbing Algorithm in new thread
        """
        if self.preRunChecks("Hill Climbing"):
            self.__child = threading.Thread(target=self.__controller.hillClimbing)
            self.__child.start()

    @pyqtSlot()
    def startPSO(self):
        """
        Run Particle Swarm Optimisation Algorithm in new thread
        """
        if self.preRunChecks("Particle Swarm Optimisation"):
            self.__child = threading.Thread(target=self.__controller.pso)
            self.__child.start()

    @pyqtSlot()
    def startACO(self):
        """
        Run Ant Colony Optimisation Algorithm in new thread
        """
        if self.preRunChecks("Ant Colony Optimisation"):
            self.__child = threading.Thread(target=self.__controller.aco)
            self.__child.start()

    def preRunChecks(self, problemName: str):
        """
        Get problem variables (matrixSize, populationSize)
            if invalid show error message.
        Crete problem with given parameters.
        Print to solution text box start algorithm message.
        Set thread to run.
        :param problemName: string
        :return: boolean
            True if all checks are valid
            False otherwise
        """
        self.stopAlgorithm()
        try:
            matrixSize = int(self.__getSizeEdit.text())
            populationSize = int(self.__getPopulationEdit.text())
        except ValueError:
            self.__solutionLabel.setText("\"" + self.__getSizeEdit.text() + "\" or \" " +
                                         self.__getPopulationEdit.text() + "\"is not an integer")
            return False
        if matrixSize < 3:
            self.__solutionLabel.setText("Please give an integer larger or equal to 3.")
            return False

        problem = DoubleSudokuProblem(populationSize, matrixSize)
        self.__controller.setProblem(problem)
        self.__solutionLabel.setText("Started " + problemName + " ...")
        # thread attributes are true by default
        self.__child.continue_run = True
        return True

    @pyqtSlot()
    def showProgress(self):
        """
        Get progress of thread
        Print to TextBox
        """
        # self.__solutionLabel.setText("Please wait one moment")
        with self.__controller.lock:
            self.__axes.clear()
            self.__axes.set(title="Progress of Algorithm", xlabel="Generations", ylabel="Validity")
            if isinstance(self.__controller.solution, PermutationSet):
                self.__solutionLabel.setText("Solution at generation " + str(self.__controller.generationNumber) +
                                             " of validity " + str(self.__controller.attemptValidity) + " is:\n" +
                                             self.__controller.getProblem().toString(self.__controller.solution))
                average = numpy.average(self.__controller.validities)
                stdev = numpy.std(self.__controller.validities)

                self.__axes.plot(self.__controller.validities, color="red", linewidth=2)
                self.__axes.axhline(average, color="green", linewidth=1)
                self.__axes.axhline(average - stdev, color="blue", linewidth=1)
                self.__axes.axhline(average + stdev, color="blue", linewidth=1)
                self.__axes.set_ylim(bottom=0)
                self.__plotCanvas.draw()
            else: self.__solutionLabel.setText("Can't get any solution")
        # print("read solution")

    @pyqtSlot()
    def stopAlgorithm(self):
        """
        Stop Algorithm
        """
        if self.__child.is_alive():
            # tell thread to stop by setting thread attribute to false
            self.__child.continue_run = False
        self.__axes.clear()
        self.__axes.set(title="Progress of Algorithm", xlabel="Generations", ylabel="Validity")
        if isinstance(self.__controller.solution, PermutationSet):
            self.__solutionLabel.setText("Solution at generation " + str(self.__controller.generationNumber) +
                                         " of validity " + str(self.__controller.attemptValidity) + " is:\n" +
                                         self.__controller.getProblem().toString(self.__controller.solution))
            average = numpy.average(self.__controller.validities)
            stdev = numpy.std(self.__controller.validities)

            self.__axes.plot(self.__controller.validities, color="red", linewidth=3)
            self.__axes.axhline(average, color="green", linewidth=1)
            self.__axes.axhline(average - stdev, color="blue", linewidth=1)
            self.__axes.axhline(average + stdev, color="blue", linewidth=1)
            self.__axes.set_ylim(bottom=0)
            self.__plotCanvas.draw()
        else: self.__solutionLabel.setText(self.__problemRequirementText)

