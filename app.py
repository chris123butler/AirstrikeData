# import the library
from appJar import gui
from datetime import date
import pdf_extractor as ex
import webscrape as scr

exist = "Optional"
out = "Select path..."

# handle button events
def press(button):
    if button == "Cancel":
        app.stop()
    else:
        # Existing logic
        if app.getEntry("Existing Data") != "Optional":
            exist = app.getEntry("Existing Data")
        else:
            exist = ""

        # Output logic
        if app.getEntry("Output") != "Select path...":
            out = app.getEntry("Output")
            today = date.today()
            d1 = today.strftime("%Y%m%d")
            out = out + "/" + d1 + ".csv"
        else:
            # TODO: FORCE USER INPUT
            out = ""

        urls = scr.url_scrape()
        data = ex.data_from_urls(urls, out)
        # TODO: REMOVE DEBUG LINE
        print(data)

        app.stop()




# create a GUI variable called app
app = gui("OIR Airstrike Collection", "450x200")
app.setBg("gold")
app.setFont(14)

app.addLabel("title", "Airstrike Data Collection")
app.setLabelBg("title", "green")
app.setLabelFg("title", "gold")

app.addLabelFileEntry("Existing Data")
app.setEntryDefault("Existing Data", exist)
app.addLabelDirectoryEntry("Output")
app.setEntryDefault("Output", out)

# link the buttons to the function called press
app.addButtons(["Go", "Cancel"], press)

# start the GUI
app.go()
