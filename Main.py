import queue

from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QImage, QPixmap
import WikiHandler
import plotwidget
import requests
import StyleSheet
from threading import Thread
import NLPHandler
import random
from PyQt6.QtCore import Qt, QTimer


class MainWindowUI(QtWidgets.QMainWindow):
    def __init__(self, wiki_queue):
        super(MainWindowUI, self).__init__()
        uic.loadUi("MainWindow.ui", self)

        self.wiki_queue = wiki_queue

        self.verticalLayout.addStretch()

        self.canvas1 = plotwidget.MplCanvas(self, width=5, height=5, dpi=100)
        self.canvas1.setMinimumWidth(325)
        self.canvas1.setMinimumHeight(200)
        self.canvas2 = plotwidget.MplCanvas(self, width=5, height=5, dpi=100)
        self.canvas2.setMinimumWidth(325)
        self.canvas2.setMinimumHeight(200)

        self.verticalLayout_2.addWidget(self.canvas1)
        self.verticalLayout_2.addWidget(self.canvas2)
        self.verticalLayout_2.addStretch()


        n_data = 50
        self.xdata = list(range(n_data))
        self.ydata = [random.randint(0, 10) for i in range(n_data)]
        self.update_plot()

        self.show()

        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        # Drop off the first y element, append a new one.
        self.ydata = self.ydata[1:] + [random.randint(0, 10)]
        self.canvas1.axes.cla()  # Clear the canvas.
        self.canvas1.axes.plot(self.xdata, self.ydata, 'r')
        # Trigger the canvas to update and redraw.
        self.canvas1.draw()
        self.canvas2.axes.cla()  # Clear the canvas.
        self.canvas2.axes.plot(self.xdata, self.ydata, 'r')
        # Trigger the canvas to update and redraw.
        self.canvas2.draw()

    def print_button_pressed(self):
        while not self.wiki_queue.empty():
            source_widget = SourceUI(self.wiki_queue.get())
            self.verticalLayout.insertWidget(0, source_widget)


class SourceUI(QtWidgets.QWidget):
    def __init__(self, pair, language='en'):
        super(SourceUI, self).__init__()
        uic.loadUi("SourceEntry.ui", self)

        self.setFixedHeight(150)

        page, image_source = pair

        # Set Image if available
        if len(image_source) > 0:
            image = QImage()
            image.loadFromData(requests.get(image_source).content)

            pixmap = QPixmap(image)

            # this value will need to coordinate with the ui file
            pixmap = pixmap.scaledToHeight(64, mode=Qt.TransformationMode.SmoothTransformation)

            self.label.setText("")
            self.label.setPixmap(pixmap)
            print("attempted to set picture")

        # Set text in the text browser to the summary of the article (for now)
        self.textBrowser.setText(page.summary)

        # Set up the slot for signal/slot for the deleting push button
        self.stopButton.clicked.connect(self.delete_widget_func)

    def delete_widget_func(self):
        self.setParent(None)


def main():
    # Set up asynchronous processes here

    app = QtWidgets.QApplication([])
    app.setStyleSheet(StyleSheet.StyleSheet)

    wiki_queue = queue.Queue()

    window = MainWindowUI(wiki_queue)
    thread = NLPHandler.AThread(wiki_queue)

    thread.add_source.connect(window.print_button_pressed)
    thread.start()

    print("Did we get here???")
    window.show()

    #window.custom_signal.add_source.emit()

    app.exec()


if __name__ == "__main__":
    main()