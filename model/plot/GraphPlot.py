import matplotlib.pyplot as matplot
from ipykernel.pylab.backend_inline import FigureCanvas


class GraphError(Exception):
    pass


class GraphPlot:
    def __init__(self, title, xAxisName, yAxisName, color, width):
        try :
            self.width = int(width)
            self.color = str(color)
            self.yAxisName = str(yAxisName)
            self.xAxisName = str(xAxisName)
            self.title = str(title)
        except ValueError : raise GraphError("Invalid Values.")

    def setTitle(self, title):
        if type(title) != str : raise GraphError("String expected")
        self.title = title

    def setColor(self, color):
        if type(color) != str : raise GraphError("String expected.")
        self.color = color

    def setWidth(self, width):
        if type(width) != int : raise GraphError("Not valid width.")
        self.width = width

    def setXAxisName(self, name):
        if type(name) != int :raise GraphError("String expected.")
        self.xAxisName = name

    def setYAxisName(self, name):
        if type(name) != int :raise GraphError("String expected.")
        self.yAxisName = name

    def plotLine(self, xArray, yArray, low=0, high="size"):
        if high == "size" : high=len(yArray)
        figure = matplot.figure()
        axes = figure.add_subplot()

        axes.set(title=self.title, xlabel=self.xAxisName, ylabel=self.yAxisName)
        axes.set_ylim(low, high)

        axes.plot(xArray, yArray, color=self.color, linewidth=self.width)
        matplot.show()
        '''canvas = FigureCanvas(figure)
        canvas.draw()
        return canvas'''


    def plotLine(self, yArray, low=0, high="size"):
        if high == "size" : high=len(yArray)
        xArray = []
        for i in range(len(yArray)) : xArray.append(i)
        figure = matplot.figure()
        axes = figure.add_subplot()

        axes.set(title=self.title, xlabel=self.xAxisName, ylabel=self.yAxisName)
        axes.set_ylim(low, high)

        axes.plot(xArray, yArray, color=self.color, linewidth=self.width)
        canvas = FigureCanvas(figure)
        canvas.draw()
        return canvas
