import tkinter as tk
from tkinter.ttk import *

# Global Variables
LARGE_FONT = ("Verdana", 12)
BUTTON_FONT = ("Verdana", 10)
EXISTING_PATH = ""
OUTPUT_PATH = ""


# Main Program Class
class StrikeData(tk.Tk):
    # Initialization method
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, ProgressPage, CompletePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # Method used to show a frame in the open window
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Initial page utilized on program start
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Airstrike Data Collection - Page 1", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="TO PAGE 2", font=BUTTON_FONT, command=lambda: controller.show_frame(ProgressPage))
        button1.pack()

# Progress Frame containing Progress Bar (TODO)
class ProgressPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Airstrike Data Collection - Page 2", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="TO PAGE 1", font=BUTTON_FONT,
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="TO END PAGE", font=BUTTON_FONT,
                            command=lambda: controller.show_frame(CompletePage))
        button2.pack()


class CompletePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="[COMPLETE] Airstrike Data Collection", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="TO PAGE 1", font=BUTTON_FONT,
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()


# App initialization & execution
app = StrikeData()
app.title("OIR Airstrike Data Collection")
app.geometry("600x400")
app.mainloop()