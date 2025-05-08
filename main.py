import sys
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import sqlite3
import datetime

TARGET_WORD_COUNT = 10  # per page, TODO: make it editable later

# Connect to database
con = sqlite3.connect('data.db')
cur = con.cursor()

# Font, idk if its compatible with all systems
sinhala_font = QFont("Sinhala MN", 20)

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
        self.central_widget.setStyleSheet("background-color: #FFF8E6;")

        self.date_label = QtWidgets.QLabel()
        self.date_label.setText(datetime.datetime.now().strftime("%A, %B %d"))
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.date_label.setStyleSheet("font-size: 20px; color: #000000; margin: 100px 0px 0px 0px; padding: 5px 0px 0px 0px;")
        self.date_label.setFont(sinhala_font)

        self.text_edit = QtWidgets.QTextEdit()
        self.text_edit.setPlaceholderText("Write your morning pages here...")
        self.text_edit.setStyleSheet("background-color: #FFF8E6; margin: 100px 200px 100px 0px; border: 0px transparent;")
        self.text_edit.setFont(sinhala_font)
        # self.text_edit.textChanged.connect(self.on_text_changed)

        self.page_number_label = QtWidgets.QLabel()
        self.page_number_label.setText("1/3")
        self.page_number_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.page_number_label.setStyleSheet("margin: 0px 15px 15px 0px;")
        self.page_number_label.setFont(sinhala_font)

    def layouts(self):
        self.setCentralWidget(self.central_widget)
        self.central_layout = QtWidgets.QHBoxLayout()
        self.central_layout.addWidget(self.text_edit)
        self.central_widget.setLayout(self.central_layout)

        self.left_layout = QtWidgets.QVBoxLayout()
        self.left_layout.addWidget(self.date_label)
        self.right_layout = QtWidgets.QVBoxLayout()
        self.right_layout.addWidget(self.text_edit)
        self.right_layout.addWidget(self.page_number_label)

        self.central_layout.addLayout(self.left_layout, 50)
        self.central_layout.addLayout(self.right_layout, 50)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:  # Exit full-screen mode on pressing Esc
            self.showMaximized()

    # def on_text_changed(self):
    #     text = self.text_edit.toPlainText()
    #     word_count = len(text.split()) - 1  # -1 to get an accurate count

    #     if word_count == TARGET_WORD_COUNT:
    #         self.text_edit.clear()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
