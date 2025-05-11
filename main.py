import sys
import re
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import sqlite3
import datetime

from PyQt6.QtGui import QPainter, QPen, QColor


TARGET_WORD_COUNT = 258  # per page, TODO: make it editable later (258 based on 3 pages of A4 paper)

# Connect to database
con = sqlite3.connect('data.db')
cur = con.cursor()

# Font, idk if its compatible with all systems
sinhala_font = QFont("Sinhala MN", 20)

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Artist's Way")
        self.showFullScreen()

        self.page_1 = ""
        self.page_2 = ""
        self.page_3 = ""

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        # Central widget is like content container in web dev
        # self.central_widget = QtWidgets.QWidget()
        # self.central_widget.setStyleSheet("background-color: #000; padding: 0px; margin: 0px;")
        self.setStyleSheet("background-color: #FFF8E6; padding: 0px; margin: 0px;")

        self.date_label = QtWidgets.QLabel()
        self.date_label.setText(datetime.datetime.now().strftime("%A,  %B %d"))
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.date_label.setStyleSheet("background-color: transparent; font-size: 20px; color: #000000; margin: 100px 0px 0px 0px; padding: 5px 0px 0px 0px;")
        self.date_label.setFont(sinhala_font)

        self.text_edit = QtWidgets.QTextEdit()
        self.text_edit.setPlaceholderText("Write your morning pages here...")
        self.text_edit.setStyleSheet("background-color: transparent; margin: 100px 200px 100px 0px; border: 0px transparent; color: #000000; padding: 5px 0px 0px 0px;")
        self.text_edit.setFont(sinhala_font)
        self.text_edit.textChanged.connect(self.on_text_changed)

        self.page_number_label = QtWidgets.QLabel()
        self.page_number_label.setText("1/3")
        self.page_number_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.page_number_label.setStyleSheet("margin: 15px; color: #000000; ")
        self.page_number_label.setFont(sinhala_font)

    def layouts(self):
        # self.setCentralWidget(self.central_widget)
        self.central_layout = QtWidgets.QHBoxLayout()
        # self.central_widget.setLayout(self.central_layout)

        self.left_layout = QtWidgets.QHBoxLayout()
        self.left_layout.addStretch()
        self.left_layout.addWidget(self.date_label)

        self.right_layout = QtWidgets.QVBoxLayout()
        self.right_layout.addWidget(self.text_edit)
        self.right_layout.addWidget(self.page_number_label)

        self.central_layout.addLayout(self.left_layout, 50)
        self.central_layout.addLayout(self.right_layout, 50)

        self.setLayout(self.central_layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:  # Exit full-screen mode on pressing Esc
            self.showMaximized()

    def on_text_changed(self):
        text = self.text_edit.toPlainText()
        word_count = text.count(" ")

        # What is going to happen her is that we will flip the page two times, to have three morning pages.
        if word_count == TARGET_WORD_COUNT and self.page_1 == "":
            self.page_1 = text
            self.page_number_label.setText("2/3")
            self.text_edit.clear()
            self.update()
        elif word_count == TARGET_WORD_COUNT and self.page_2 == "":
            self.page_2 = text
            self.page_number_label.setText("3/3")
            self.text_edit.clear()
            self.update()
        elif word_count == TARGET_WORD_COUNT and self.page_3 == "":
            self.page_3 = text
            self.text_edit.clear()
            self.text_edit.setEnabled(False)
            self.text_edit.setPlaceholderText("You've completed your morning pages!")
            self.page_number_label.setText("")  
            try:
                query = "INSERT INTO 'morning_pages' (date, entry) VALUES(?, ?)"
                cur.execute(query, (datetime.datetime.now().strftime("%Y-%m-%d"), self.page_1 + self.page_2 + self.page_3))
                con.commit()

            except sqlite3.Error as e:
                print(f"Error inserting data: {e}")

    def paintEvent(self, event):
        # Rectangles to the left are graphical reperesentations of the pages
        if self.page_1 != "" and self.page_2 == "":
            qp = QPainter(self)
            qp.setBrush(QColor("#FFF6DF"))
            qp.setPen(QPen(QColor('transparent'), 0))
            qp.drawRect(0, 0, 60, self.size().height())
            qp.end()
        elif self.page_2 != "" and self.page_3 == "":
            qp = QPainter(self)
            qp.setBrush(QColor("#FFF4D5"))
            qp.setPen(QPen(QColor('transparent'), 0))
            qp.drawRect(0, 0, 60, self.size().height())

            qp.setBrush(QColor("#FFF6DF"))
            qp.setPen(QPen(QColor('transparent'), 0))
            qp.drawRect(60, 0, 60, self.size().height())
            qp.end()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
