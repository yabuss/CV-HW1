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
        self.input_image_path = ""
        self.input_image = QLabel()
        self.input_histogram = FigureCanvas(Figure(figsize=(5, 3)))
        self.target_image_path = ""
        self.target_image = QLabel()
        self.target_histogram = FigureCanvas(Figure(figsize=(5, 3)))
        self.result = QLabel()
        self.result_histogram = QLabel()
        self.initUI()

    def open_input_image(self):
        # This function is called when the user clicks File->Input Image.
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.input_image_path, _ = QFileDialog.getOpenFileName(self, "Select Input Image", "",
                                                               "PNG Files (*.png)", options=options)
        if self.input_image_path:
            image = QImage(self.input_image_path)
            self.input_image.setPixmap(QPixmap.fromImage(image))
            self.inputLoaded = True

    def open_target_image(self):
        # This function is called when the user clicks File->Target Image.
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.target_image_path, _ = QFileDialog.getOpenFileName(self, "Select Target Image", "",
                                                                "PNG Files (*.png)", options=options)
        if self.target_image_path:
            image = QImage(self.target_image_path)
            self.target_image.setPixmap(QPixmap.fromImage(image))
            self.targetLoaded = True

    def initUI(self):
        # Menu Actions

        # Opening the input image
        open_input_action = QAction('&Open Input', self)
        open_input_action.setShortcut('Ctrl+O')
        open_input_action.setStatusTip('Open the Input Image')
        open_input_action.triggered.connect(self.open_input_image)

        # Opening the target image
        open_target_action = QAction('&Open Target', self)
        open_target_action.setShortcut('Ctrl+T')
        open_target_action.setStatusTip('Open the Target Image')
        open_target_action.triggered.connect(self.open_target_image)

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

        # 'Calculate Histogram' button
        calculate_histogram = QAction('Calculate Histograms', self)
        calculate_histogram.setShortcut('Ctrl+C')
        calculate_histogram.triggered.connect(self.calculateHistogramClicked)

        # 'Equalize Histogram' button
        equalize_histogram = QAction('Equalize Histogram', self)
        equalize_histogram.setShortcut('Ctrl+H')
        equalize_histogram.triggered.connect(self.histogramButtonClicked)

        toolbar = self.addToolBar('Equalize Histogram')
        toolbar.addAction(calculate_histogram)
        toolbar.addAction(equalize_histogram)

        # Grid elements
        self.input_image = QLabel()
        self.input_image.setText("Input Image Placeholder")
        self.target_image = QLabel()
        self.target_image.setText("Target Image Placeholder")
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
        central_widget = QWidget()
        central_widget.setLayout(grid)
        self.setCentralWidget(central_widget)

        self.setWindowTitle('Python Histogram')
        self.showMaximized()
        self.show()

    def calculateHistogramClicked(self):
        if not self.inputLoaded and not self.targetLoaded:
            # Error: "First load input and target images" in MessageBox
            self.statusBar().showMessage("Error: First load input and target images")
            return NotImplementedError
        if not self.inputLoaded:
            # Error: "Load input image" in MessageBox
            self.statusBar().showMessage("Error: Load input image first")
            hist2 = self.calc_histogram(self.target_image_path)
            self.input_histogram = PlotCanvas(hist2, self)
            return NotImplementedError
        elif not self.targetLoaded:
            # Error: "Load target image" in MessageBox
            self.statusBar().showMessage("Error: Load target image first")
            hist1 = self.calc_histogram(self.input_image_path)
            self.input_histogram = PlotCanvas(hist1, self)
            return NotImplementedError
        # Calculate and display both images' histograms
        hist1 = self.calc_histogram(self.input_image_path)
        self.input_histogram = PlotCanvas(hist1, self)
        hist2 = self.calc_histogram(self.target_image_path)
        self.input_histogram = PlotCanvas(hist2, self)

    def histogramButtonClicked(self):
        if not self.inputLoaded and not self.targetLoaded:
            # Error: "First load input and target images" in MessageBox
            self.statusBar().showMessage("Error: First load input and target images")
            return NotImplementedError
        if not self.inputLoaded:
            # Error: "Load input image" in MessageBox
            self.statusBar().showMessage("Error: Load input image first")
            return NotImplementedError
        elif not self.targetLoaded:
            # Error: "Load target image" in MessageBox
            self.statusBar().showMessage("Error: Load target image first")
            return NotImplementedError

    def calc_histogram(self, image):
        # Calculate histogram
        img = cv2.imread(image, 1)
        R, C, B = img.shape
        hist = np.zeros([256, 1, B], dtype=np.uint8)
        for g in range(256):
            hist[g, 0, ...] = np.sum(np.sum(img == g, 0), 0)
        return hist

class PlotCanvas(FigureCanvas):
    def __init__(self, hist, parent, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot_histogram(hist)

    def plot_histogram(self, hist):
        # Plot histogram
        ax = self.figure.add_subplot(111)
        ax.plot(hist, 'r-')
        ax.set_title('PyQt Matplotlib Example')
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
