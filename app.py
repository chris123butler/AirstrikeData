# import the library
from appJar import gui

# handle button events
def press(button):
    if button == "Cancel":
        app.stop()
    else:
        # Existing logic
        if app.getEntry("Existing") != "Optional":
            exist = app.getEntry("Existing")
        else:
            exist = ""

        # Output logic
        if app.getEntry("Output") != "Select path...":
            out = app.getEntry("Output")
        else:
            out = ""
        print("Existing: " + exist + " | Output: " + out)


# create a GUI variable called app
app = gui("OIR Strike Collection", "450x200")
app.setBg("gold")
app.setFont(18)

app.addLabel("title", "Welcome to OIR Airstrike Data Collection")
app.setLabelBg("title", "green")
app.setLabelFg("title", "gold")

app.addLabelFileEntry("Existing")
app.setEntryDefault("Existing", "Optional")
app.addLabelDirectoryEntry("Output")
app.setEntryDefault("Output", "Select path...")

# link the buttons to the function called press
app.addButtons(["Go", "Cancel"], press)

# start the GUI
app.go()
