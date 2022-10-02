import queue

from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QImage, QPixmap
import WikiHandler
import plotwidget
import requests
import StyleSheet
from threading import Thread
import NLPHandler
from PyQt6.QtCore import pyqtSignal, QObject


class MainWindowUI(QtWidgets.QMainWindow):
    def __init__(self, wiki_queue):
        super(MainWindowUI, self).__init__()
        uic.loadUi("MainWindow.ui", self)

        self.wiki_queue = wiki_queue

        sc = plotwidget.MplCanvas(self, width=1, height=1, dpi=100)
        sc.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])

        self.verticalLayout_2.addWidget(sc)
        self.verticalLayout_2.addWidget(sc)

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
            pixmap = pixmap.scaledToHeight(64)

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