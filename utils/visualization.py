from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt5.QtCore import Qt
import sys


class Annotator(QWidget):
    def __init__(self, image_path):
        super().__init__()
        self.setWindowTitle("车道线标注工具")
        self.image = QPixmap(image_path)
        self.label = QLabel()

    def showWindow(self):
        scaled_image = self.image.scaled(400, 300, Qt.KeepAspectRatio)
        self.label.setPixmap(scaled_image)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Annotator(r"..\data\images\road.png")
    # window.show()
    window.showWindow()
    sys.exit(app.exec_())
