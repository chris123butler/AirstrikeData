# import the library
from appJar import gui
from datetime import date
import pdf_extractor as ex
import PyPDF2
import webscrape as scr
import os

exist = "Optional"
out = "Select path..."
app = gui("OIR Airstrike Collection", "450x250")
total_urls = 1
curr_url = 0


def increment_progress_bar(length):
    global curr_url
    app.setMeter("prog", curr_url/length * 100)
    curr_url += 1


def create_dict():
    data = {'Release Number': [],
            'URL': [],
            'Report Date': [],
            'Strike Date': [],
            'Number of Strikes': [],
            'Country': [],
            'Location': [],
            'Targeted': [],
            'Unit': [],
            'Number of Units': [],
            'Detroyed': [],
            'Flagged': [],
            'Initials': []}
    return data


def execute():
    if app.getEntry("Existing Data") != "":
        exist = app.getEntry("Existing Data")

    # Output logic
    today = date.today()
    d1 = today.strftime("%Y%m%d")
    if app.getEntry("Output") != "":
        out = app.getEntry("Output")
    else:
        out = os.path.normpath(os.path.expanduser("~/Desktop/"))

    # TODO: REMOVE DEBUG URLS ARRAY
    urls = scr.url_scrape()

    if os.path.exists(out):
        global total_urls
        total_urls = len(urls)
        out = os.path.normpath(out + "/" + d1 + ".csv")
        data = create_dict()
        for url in urls:
            ex.data_from_url(url, data)
            app.after(100, increment_progress_bar(total_urls))
        data = ex.fill_empty_values(data)
        ex.create_and_save_dataframe(data, out)
        #data = ex.data_from_urls(urls, out)
        #print(data)
    else:
        print("[ERROR] Cannot save output file to path: " + out)


# handle button events
def press(button):
    if button == "Close":
        app.stop()
    else:
        execute()


# create a GUI variable called app

app.addStatusbar(fields=1)
app.setStatusbar("NOTICE: Program will freeze during execution.", 0)
app.setStatusFont(8)
app.addLabel("title", "Airstrike Data Collection")
app.setBg("gold")
app.setFont(14)

app.startLabelFrame("File I/O")
# Stretch label frame to left and right, responsive
app.setSticky("ew")

app.setLabelBg("title", "green")
app.setLabelFg("title", "white")

app.addLabelFileEntry("Existing Data")
app.setEntryDefault("Existing Data", exist)
app.addLabelDirectoryEntry("Output")
app.setEntryDefault("Output", out)
app.stopLabelFrame()

# link the buttons to the function called press
app.addButtons(["Go", "Close"], press)

app.addLabel("Progress")
app.addMeter("prog")
app.setMeterFill("prog", "green")

# start the GUI
app.go()
