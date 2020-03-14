# import the library
from appJar import gui
from datetime import date
import pdf_extractor as ex
import webscrape as scr
import os

exist = "Optional"
out = "Select path..."

def launch(win):
    app.showSubWindow(win)


# handle button events
def press(button):
    if button == "Cancel":
        app.stop()
    else:
        # Existing logic
        if app.getEntry("Existing Data") != "":
            exist = app.getEntry("Existing Data")

        # Output logic
        today = date.today()
        d1 = today.strftime("%Y%m%d")
        if app.getEntry("Output") != "":
            out = app.getEntry("Output")

            out = out + "/" + d1 + ".csv"
        else:
            out = os.environ['USERPROFILE'] + "\Desktop\\" + d1 + ".csv"
            # TODO REMOVE DEBUG LINE
            print("[DEBUG] No output specified, defaulting to Desktop: " + out)

        urls = scr.url_scrape()
        data = ex.data_from_urls(urls, out)
        # TODO: REMOVE DEBUG LINE
        print(data)

        app.stop()


# create a GUI variable called app
app = gui("OIR Airstrike Collection", "450x200")
app.addLabel("title", "Airstrike Data Collection")
app.setBg("gold")
app.setFont(14)

app.startLabelFrame("File I/O")
app.setSticky("ew")

app.setLabelBg("title", "green")
app.setLabelFg("title", "white")

app.addLabelFileEntry("Existing Data")
app.setEntryDefault("Existing Data", exist)
app.addLabelDirectoryEntry("Output")
app.setEntryDefault("Output", out)

# link the buttons to the function called press
app.addButtons(["Go", "Cancel"], press)
app.stopLabelFrame()

# start the GUI
app.go()
