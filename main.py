import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton, QGroupBox, QAction, QFileDialog, qApp, QLineEdit, QTextEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import cv2


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()

        # You can define other things in here
        self.inputLoaded = False
        self.targetLoaded = False
        self.title = 'Histogram Equalization'
        self.input_image = QLabel()
        self.input_histogram = QLabel()
        self.target_image = QLabel()
        self.target_histogram = QLabel()
        self.result = QLabel()
        self.result_histogram = QLabel()
        self.initUI()

    def openInputImage(self):
        # This function is called when the user clicks File->Input Image.
        return NotImplementedError

    def openTargetImage(self):
        # This function is called when the user clicks File->Target Image.
        return NotImplementedError

    def initUI(self):
        # Menu Actions

        # Opening the input image
        open_input_action = QAction('&Open Input', self)
        open_input_action.setShortcut('Ctrl+O')
        open_input_action.setStatusTip('Open the Input Image')
        open_input_action.triggered.connect(self.openInputImage)

        # Opening the target image
        open_target_action = QAction('&Open Target', self)
        open_target_action.setShortcut('Ctrl+T')
        open_target_action.setStatusTip('Open the Target Image')
        open_target_action.triggered.connect(self.openTargetImage)

        # Exiting the program from menu
        exit_act = QAction('&Exit', self)
        exit_act.setShortcut('Ctrl+E')
        exit_act.setStatusTip('Exit application')
        exit_act.triggered.connect(qApp.quit)

        menu = self.menuBar()
        file_menu = menu.addMenu('&File')
        file_menu.addAction(open_input_action)
        file_menu.addAction(open_target_action)
        file_menu.addAction(exit_act)

        # Histogram button
        equalize_histogram = QAction('Equalize Histogram', self)
        equalize_histogram.setShortcut('Ctrl+H')
        equalize_histogram.triggered.connect(self.histogramButtonClicked)

        toolbar = self.addToolBar('Equalize Histogram')
        toolbar.addAction(equalize_histogram)

        image1 = QImage("color1.png")
        image2 = QImage("color2.png")

        self.input_image = QLabel()
        self.input_histogram = QLabel()
        self.input_histogram.setText("Input Histogram Placeholder")
        self.input_image.setPixmap(QPixmap.fromImage(image1))
        self.target_image = QLabel()
        self.target_histogram = QLabel()
        self.target_image.setPixmap(QPixmap.fromImage(image2))
        self.target_histogram.setText("Target Histogram Placeholder")
        self.result = QLabel()
        self.result_histogram = QLabel()

        grid = QGridLayout(self)
        grid.setSpacing(10)

        grid.addWidget(self.input_image, 0, 0)
        grid.addWidget(self.input_histogram, 1, 0)

        grid.addWidget(self.target_image, 0, 1)
        grid.addWidget(self.target_histogram, 1, 1)

        grid.addWidget(self.result, 0, 2)
        grid.addWidget(self.result_histogram, 1, 2)
        self.result_histogram.setText("Asasasa")
        central_widget = QWidget()
        central_widget.setLayout(grid)
        self.setCentralWidget(central_widget)

        self.setWindowTitle('Python Histogram')
        self.showMaximized()
        self.show()

    def histogramButtonClicked(self):
        if not self.inputLoaded and not self.targetLoaded:
            # Error: "First load input and target images" in MessageBox
            return NotImplementedError
        if not self.inputLoaded:
            # Error: "Load input image" in MessageBox
            return NotImplementedError
        elif not self.targetLoaded:
            # Error: "Load target image" in MessageBox
            return NotImplementedError

    def calcHistogram(self, I):
        # Calculate histogram
        return NotImplementedError


class PlotCanvas(FigureCanvas):
    def __init__(self, hist, parent=None, width=5, height=4, dpi=100):
        # Init Canvas
        self.plotHistogram(hist)

    def plotHistogram(self, hist):
        return NotImplementedError
        # Plot histogram

        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
