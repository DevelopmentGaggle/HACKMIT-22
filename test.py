import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget
from PyQt6.QtGui import QPixmap, QImage
import requests
import WikiHandler
from bing_image_urls import bing_image_urls

class Example(QWidget):

    def __init__(self):
        super().__init__()

        page, image_source = WikiHandler.get_first_wiki("Franklin")
        #image_source = "https://upload.wikimedia.org/wikipedia/commons/6/6d/2016-06-06_09_38_36_View_south_along_U.S._Route_220_%28Main_Street%29_just_south_of_Pine_Street_in_Franklin%2C_Pendleton_County%2C_West_Virginia.jpg"
        #image_source = "https://upload.wikimedia.org/wikipedia/commons/1/1c/Boethius.consolation.philosophy.jpg"

        image = QImage()

        url = bing_image_urls(page.title, limit=1)[0]

        image.loadFromData(requests.get(url).content)

        #print(page.title)

        pixmap = QPixmap(image)

        pixmap = pixmap.scaledToHeight(64)

        self.im = pixmap
        self.label = QLabel()
        self.label.setPixmap(self.im)

        self.grid = QGridLayout()
        self.grid.addWidget(self.label, 1, 1)
        self.setLayout(self.grid)

        self.setGeometry(50, 50, 320, 200)
        self.setWindowTitle("PyQT show image")
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())