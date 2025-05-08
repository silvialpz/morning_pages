import sys
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt

TARGET_WORD_COUNT = 50


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Artist's Way")
        self.showMaximized()
        self.showFullScreen()

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        # Central widget is like content container in web dev
        self.central_widget = QtWidgets.QWidget()
        self.text_edit = QtWidgets.QTextEdit()
        self.text_edit.setPlaceholderText("Write your morning pages here...")

    def layouts(self):
        self.setCentralWidget(self.central_widget)
        self.central_layout = QtWidgets.QVBoxLayout()
        self.central_layout.addWidget(self.text_edit)
        self.central_widget.setLayout(self.central_layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:  # Exit full-screen mode on pressing Esc
            self.showNormal()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
