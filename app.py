from PyQt5.QtWidgets import *
import sys
from tkinter import *
from tkinter import filedialog
# app = QApplication([])
# window = QWidget()
# layout = QVBoxLayout()
# layout.addWidget(QPushButton('Go'))
# layout.addWidget(QPushButton('Bye'))
# window.setLayout(layout)
# window.resize(800,400)
# window.show()
#
# app.exec_()
def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    print(filename)

root = Tk()
#geometry handles height&width of frame
root.geometry("600x400")
button1 = Button(text="Previous Data", command=browse_button)
folder_path = StringVar()
lbl1 = Label(master=root,textvariable=folder_path)
lbl1.grid(row=0, column=1)
button2 = Button(text="Browse", command=browse_button)
button1.grid(row=1, column=1)
button2.grid(row=10, column=1)

mainloop()