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
    def __init__(self, wiki_queue, metrics_queue_1):
        super(MainWindowUI, self).__init__()
        uic.loadUi("MainWindow.ui", self)
        self.setWindowTitle("Application Name")

        self.total = 5
        self.ydata = []
        self.xdata = []

        self.wiki_queue = wiki_queue
        self.metrics_queue_1 = metrics_queue_1
        self.usedWikis = []

        # Add graph widgets to the left and a spacer to the right
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



        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        # Grab new data
        if self.metrics_queue_1.empty():
            return

        total_words, important_words = self.metrics_queue_1.get()

        print(total_words)
        print(important_words)

        if len(self.ydata) + 1 > self.total:
            # TODO PLEASE WORK
            self.ydata = self.ydata[1:] + [important_words / total_words]
            self.xdata = [self.xdata[self.total-1]] + self.xdata[1:]
        else:
            self.ydata = self.ydata + [important_words / total_words]
            self.xdata = self.xdata + [len(self.ydata)]

        self.canvas1.axes.cla()  # Clear the canvas.
        self.canvas1.axes.plot(self.xdata, self.ydata, 'r')
        # Trigger the canvas to update and redraw.
        self.canvas1.draw()

    def print_button_pressed(self):
        while not self.wiki_queue.empty():
            wikiData = self.wiki_queue.get()
            if wikiData[0] not in self.usedWikis:
                self.usedWikis.append(wikiData[0])
                source_widget = SourceUI(wikiData)
                self.verticalLayout.insertWidget(0, source_widget)


class SourceUI(QtWidgets.QWidget):
    def __init__(self, pair, language='en'):
        super(SourceUI, self).__init__()
        uic.loadUi("SourceEntry.ui", self)

        height = 150

        self.setFixedHeight(height)

        page, image_source = pair

        # Set Image if available
        if len(image_source) > 0:
            image = QImage()
            image.loadFromData(requests.get(image_source).content)

            pixmap = QPixmap(image)

            # this value will need to coordinate with the ui file
            pixmap = pixmap.scaledToHeight(height, mode=Qt.TransformationMode.SmoothTransformation)

            self.label.setText("")
            self.label.setPixmap(pixmap)

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
    metrics_queue_1 = queue.Queue()

    window = MainWindowUI(wiki_queue, metrics_queue_1)
    thread = NLPHandler.AThread(wiki_queue, metrics_queue_1)

    thread.add_source.connect(window.print_button_pressed)
    thread.start()

    window.show()
    app.exec()


if __name__ == "__main__":
    main()