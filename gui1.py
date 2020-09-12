#load PyQt
from PyQt5.QtWidgets import QApplication, QLabel

#requirement of Qt: Every GUI app must have exactly one instance of QApplication. Many parts of Qt don't work until you have executed this:
app = QApplication([])

label = QLabel('Hello World!')

label.show()

app.exec_()