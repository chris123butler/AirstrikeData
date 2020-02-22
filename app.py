from PyQt5.QtWidgets import *

app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
layout.addWidget(QPushButton('Go'))
layout.addWidget(QPushButton('Bye'))
window.setLayout(layout)
window.show()
app.exec_()