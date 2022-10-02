from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QImage, QPixmap
import WikiHandler
import requests

class MainWindowUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindowUI, self).__init__()
        uic.loadUi("MainWindow.ui", self)
        self.pushButton.clicked.connect(self.print_button_pressed)

    def print_button_pressed(self):
        source_widget = SourceUI("Ford")
        self.verticalLayout.addWidget(source_widget)



class SourceUI(QtWidgets.QWidget):
    def __init__(self, term, language='en'):
        super(SourceUI, self).__init__()
        uic.loadUi("SourceEntry.ui", self)

        page, image_source = WikiHandler.get_first_wiki(term, language)

        # Set Image if available
        if len(image_source) > 0:
            image = QImage()
            image.loadFromData(requests.get(image_source).content)

            pixmap = QPixmap(image)

            pixmap = pixmap.scaledToHeight(64) # this value will need to coordinate with the ui file

            self.label.setText("")
            self.label.setPixmap(pixmap)
            print("attempted to set picture")


        # Set text in the text browser to the summary of the article (for now)
        self.textBrowser.setText(page.summary)


        # Set up the slot for signal/slot for the deleting push button
        #self.pushButton




def main():
    # Set up asynchronous processes here

    app = QtWidgets.QApplication([])
    window = MainWindowUI()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()

