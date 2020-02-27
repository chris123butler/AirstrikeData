import tkinter as tk

# Global Variables
LARGE_FONT = ("Verdana", 12)
BUTTON_FONT = ("Verdana", 8)
FOLDER_PATH = ""


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
        frame = StartPage(container, self)
        self.frames[StartPage] = frame
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
        label = tk.Label(self, text="Airstrike Data Collection", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        prevButton = tk.Button(self, text="Use Existing Data", font=BUTTON_FONT)
        prevButton.pack(pady=10, padx=10)


# App initialization & execution
app = StrikeData()
app.title("OIR Airstrike Data Collection")
app.geometry("600x400")
app.mainloop()